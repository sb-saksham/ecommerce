from django.db import models
from products.models import Product
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from utils import unique_order_id
from billing.models import BillingProfile

status_choices = [
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('cod', 'Cash On Delivery'),
    ('delivered', 'Delivered'),
    ('refunded', 'Refunded'),
    ('order_complete', 'Order Complete'),
]

User = get_user_model()


class RentingOrder(models.Model):
    # user = models.ForeignKey(User)
    order_id = models.CharField(max_length=8, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, related_name="get_renting_order")  # for this Billing_profile
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=40, choices=status_choices)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    total_days_on_rent = models.IntegerField(null=True, blank=True)
    total_days_out = models.IntegerField(null=True, blank=True)  # +2 days, 1 for delivery and 1 for receiving
    total_cost = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

    def update_total_days_on_rent(self, start, end):
        total_days_on_rent = int(end.day - start.day)
        self.total_days_on_rent = total_days_on_rent
        self.start = start
        self.end = end

        nf_total_cost = self.product.per_day_renting_price * self.total_days_on_rent
        f_total_cost = format(nf_total_cost, '2f')
        self.total_cost = f_total_cost

        self.total_days_out = self.total_days_on_rent + 2

        self.status = 'created'

        self.save()


def renting_order_pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id(instance)
    return instance.order_id


pre_save.connect(renting_order_pre_save_order_id_receiver, sender=RentingOrder)
