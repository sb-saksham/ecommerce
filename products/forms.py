from django import forms
from .models import Product


class ProductOnRentCart(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['on_rent']
