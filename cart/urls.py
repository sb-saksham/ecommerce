from django.urls import path
from .views import cart_view, cart_update, checkout, checkout_done_view, renting_add, failure, success

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='home'),
    path('checkout/failed/', failure, name='failed'),
    path('update/', cart_update, name="update"),
    path('checkout/', checkout, name="checkout"),
    path('add/renting/', renting_add, name="update_renting"),
    path('checkout/success/', success, name="success"),
    path('checkout/success/us', checkout_done_view, name="cdv"),
]