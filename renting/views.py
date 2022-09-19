from cart.models import Cart
from django.shortcuts import render, redirect
from datetime import date
from products.models import Product
from .models import RentingOrder
from billing.models import BillingProfile
from .forms import RentingOrderForm


def rent_initiate(request):
    product_id = request.GET.get('id')
    if request.method == 'GET':
        if not request.user.is_authenticated:
            request.session['renting_object_create_url'] = request.build_absolute_uri()
            return redirect('/accounts/signup/')
        renting_form = RentingOrderForm()
        qs = Product.objects.filter(id=product_id)
        product_detail = None
        if qs.exists():
            product_detail = qs.first()
        context = {'product_detail': product_detail, 'form': renting_form}
        return render(request, 'renting/rent_form.html', context=context)


def rent_status(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        qs = Product.objects.filter(id=product_id)
        if qs.exists():
            product_detail = qs.first()
        else:
            product_detail = None
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        renting_form = RentingOrderForm(request.POST)
        if renting_form.is_valid():
            start = renting_form.cleaned_data.get('start')
            end = renting_form.cleaned_data.get('end')
            renting_order, is_obj_created = RentingOrder.objects.get_or_create(
                        billing_profile=billing_profile,
                        product=product_detail,
            )
            renting_order.update_total_days_on_rent(
                start=start,
                end=end,
            )
            renting_order.save()
            cart_obj, is_created = Cart.objects.new_or_get(request)
            day_counter = int(end.day) - date.today().day
            context = {'renting_order': renting_order, 'today': day_counter, 'cart': cart_obj}
            return render(request, 'renting/rent_status.html', context=context)
        elif request.POST.get('renting_order_id') is not None:
            renting_order = RentingOrder.objects.get(order_id=request.POST.get('renting_order_id'))
            return render(request, 'renting/rent_status.html', context={'renting_order': renting_order})
        else:

            # add here link to error file or redirect with error message to renting page

            raise ValueError("Incorrect Values are entered")
    return redirect('/renting/renting/')


def rent_edit_view(request):
    if request.method == "POST":
        renting_form = RentingOrderForm(request.POST)
        if renting_form.is_valid():
            start = renting_form.cleaned_data.get('start')
            end = renting_form.cleaned_data.get('end')
            renting_order_id = request.POST.get('renting_order')
            renting_order = RentingOrder.objects.get(order_id=renting_order_id)
            renting_order.update_total_days_on_rent(start=start, end=end)
            renting_order.save()

    return redirect('/renting/renting/')


def rent_tracking(request):
    billing_profile, is_created = BillingProfile.objects.new_or_get(request)
    renting_orders = billing_profile.get_renting_order.all()
    cart_obj, cart_is_created = Cart.objects.new_or_get(request)
    context = {'renting_orders': renting_orders, 'cart': cart_obj}
    return render(request, 'renting/rent_status.html', context=context)
