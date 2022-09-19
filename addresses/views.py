from django.shortcuts import redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from billing.models import BillingProfile
from .models import Address


def checkout_address_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.method == 'POST':
        form1 = AddressForm(request.POST)
        address_type = request.POST.get('address_type', 'shipping')
        if form1.is_valid():
            instance = form1.save(commit=False)
            billing_profile, billing_profile_is_created = BillingProfile.objects.new_or_get(request)
            if billing_profile is not None:
                instance.billing_profile = billing_profile
                instance.address_type = request.POST.get('address_type', 'shipping')
                instance.save()
                request.session[address_type + "_address_id"] = instance.id
            if is_safe_url(redirect_path, request.get_host()) and redirect_path is not None:
                return redirect(redirect_path)
    else:
        return redirect('cart:checkout')


def checkout_address_use_view(request):
    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == 'POST':
            shipping_address_id = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_is_created = BillingProfile.objects.new_or_get(request)
            if shipping_address_id is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=float(shipping_address_id))
                if qs.exists():
                    request.session[address_type + "_address_id"] = float(shipping_address_id)
                if is_safe_url(redirect_path, request.get_host()) and redirect_path is not None:
                    return redirect(redirect_path)
    return redirect('cart:checkout')
