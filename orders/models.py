from django.db import models
from django.db.models.signals import pre_save, post_save
from cart.models import Cart
from utils import unique_order_id
from addresses.models import Address
from math import fsum
from billing.models import BillingProfile

status_choices = [
    ('created', 'Created'),
    ('delivered', 'Delivered'),
    ('dispatched', 'Dispatched'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
]


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile,
                                        cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True

        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)#user
    order_id = models.CharField(max_length=8, blank=True)
    shipping_address = models.ForeignKey(Address, null=True, blank=True,
                                         related_name='shipping_address',
                                         on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, null=True, blank=True,
                                         related_name='billing_address',
                                         on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_choices, default='created')
    shipping_total = models.DecimalField(default=50.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def check_done(self):
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        billing_profile = self.billing_profile
        total = self.total
        if shipping_address and billing_address and billing_profile and total > 0.00:
            return True
        return False

    def mark_done(self):
        if self.check_done():
            self.status = 'paid'
            self.cart.renting_order.status = 'cod'
            self.save()
        return self.status

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        n_total = fsum([cart_total, shipping_total])
        formatted_total = format(n_total, '2f')
        self.total = formatted_total
        self.save()


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id(instance)
    order_qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if order_qs.exists():
        order_qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order_total(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order_total, sender=Order)

