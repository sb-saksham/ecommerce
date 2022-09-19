from django.http import JsonResponse
from hashlib import sha512, sha256
from django.shortcuts import render, redirect
from .models import Cart
from renting.models import RentingOrder
from addresses.forms import AddressForm
from addresses.models import Address
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.context_processors import csrf
from ecommerce.mixins import RequestFormAttachMixin


MERCHANT_KEY = 'rjQUPktU'
SALT = 'e5iIg1jwi8'


def cart_api_update_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "url": x.get_absolute_url(),
        "id": x.id,
        "message": x.message,
        "price": x.price,
    } for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "cart/cart_index.html", context={'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get("product_id", None)
    if product_id is not None:
        try:
            product_obj = Product.objects.filter(id=product_id).first()
        except Product.DoesNotExist:
            print("The product is gone...")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj not in cart_obj.products.all():
            cart_obj.products.add(product_obj)
            added = True
        else:
            cart_obj.products.remove(product_obj)
            added = False
        # if len(cart_obj.renting_order.all())!= 0:
        request.session['cart_items'] = cart_obj.products.count()  # + cart_obj.renting_order.count()
        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "count": cart_obj.products.count()  # + cart_obj.renting_order.count()
            }
            return JsonResponse(json_data)
    return redirect("cart:home")


def checkout_done_view(request):
    return render(request, 'cart/checkout_done_view.html')


def renting_add(request):
    if request.method == 'POST':
        renting_order_id = request.POST.get('renting_order', None)
        if renting_order_id is not None:
            try:
                renting_order_obj = RentingOrder.objects.filter(order_id=renting_order_id).first()
                print(renting_order_obj)
                print("1.renting Object accessed")
            except RentingOrder.DoesNotExist:
                print("The Object is not there...")
                return redirect("cart:home")
            cart_obj, new_obj_created = Cart.objects.new_or_get(request)
            print("2.Cart obj accessed")
            if cart_obj.renting_order is None or cart_obj.renting_order != renting_order_obj:
                cart_obj.renting_order = renting_order_obj
                added = True
                print("Object added")
            else:
                cart_obj.renting_order = None
                added = False
                print("Not added")
            request.session['cart_items'] = cart_obj.products.count() + 1
            cart_obj.save()
    return redirect('cart:home')


def checkout(request):
    cart_obj, created_cart = Cart.objects.new_or_get(request)
    order_obj = None
    if created_cart and cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm(request)
    guest_form = GuestForm()
    address_form = AddressForm()
    shipping_address_id = request.session.get('shipping_address_id')
    billing_address_id = request.session.get('billing_address_id')
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request=request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, created_order_obj = Order.objects.new_or_get(billing_profile=billing_profile, cart_obj=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', None)
        if payment_method == 'cod':
            return redirect('cart:cdv')
        elif payment_method == 'other':
            order = order_obj
            key = MERCHANT_KEY
            salt = SALT
            PAYU_BASE_URL = "https://test.payu.in/_payment"
            posted = {
                'amount': float(order.total),
                'email': order.billing_profile.user.email,
                'phone': order.billing_profile.phone_no,
                'firstname': order.billing_profile.user.get_short_name(),
            }
            Productinfo = [{"paymentParts": [{
                "name": "abc",
                "description": "abcd",
                "value": "500",
                "isRequired": "true",
                "settlementEvent": "EmailConfirmation",
            },
            {
                "name": "xyz",
                "description": "wxyz",
                "value": "1500",
                "isRequired": "false",
                "settlementEvent": "EmailConfirmation",
            }]},
            {"paymentIdentifiers":[{
                "field": "CompletionDate",
                "value": "31/10/2012",
            },
                {
                    "field": "TxnId",
                    "value": "abced",

                }]}]
            posted['productinfo'] = "My products"
            posted['furl'] = "http://127.0.0.1:8000/cart/checkout/failed/"
            posted['surl'] = "http://127.0.0.1:8000/cart/checkout/success/"
            # Merchant Key and Salt provided by the PayU.
            for i in request.POST:
                posted[i] = request.POST[i]
            hash_object = sha256(b'randint(0,20)')
            txnid = hash_object.hexdigest()[0:20]
            posted['txnid'] = txnid.lower()
            hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|||||"
            posted['key'] = key
            hash_string = ''
            hashVarsSeq = hashSequence.split('|')
            for i in hashVarsSeq:
                try:
                    hash_string += str(posted[i])
                except Exception:
                    hash_string += ''
                hash_string += '|'
            hash_string += salt
            print("The hash string is", hash_string)
            hashh = sha512(hash_string.encode('utf-8')).hexdigest().lower()
            action = PAYU_BASE_URL
            if posted.get("key") is None and posted.get("txnid") is None and posted.get("productinfo") is None and posted.get("firstname") is None and posted.get("email") is None:
                return render('cart/current_datetime.html', {"posted": posted, "hashh": hashh,
                                                                   "MERCHANT_KEY": MERCHANT_KEY,
                                                                   "txnid": txnid,
                                                                   "hash_string": hash_string,
                                                                   "action": "."})
            else:
                return render('cart/current_datetime.html', {"posted": posted, "hashh": hashh,
                                                                   "MERCHANT_KEY": MERCHANT_KEY,
                                                                   "txnid": txnid,
                                                                   "hash_string": hash_string,
                                                                   "action": action})
    context = {
        'billing_profile': billing_profile,
        'order': order_obj,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        }

    return render(request, "cart/cart_checkout.html", context=context)


@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "GQs7yium"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = sha512(retHashSeq.encode()).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render('cart/status.html', {"txnid": txnid, "status": status, "amount": amount})


@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = ""

    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key

    hashh = sha512(retHashSeq.encode()).hexdigest().lower()

    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render("cart/status.html", c)

