from django.db import models
from billing.models import BillingProfile

address_type_choices = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=address_type_choices)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, default='Raipur')
    state = models.CharField(max_length=120, default='Chhatisgarh')
    country = models.CharField(max_length=120, default='India')
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.billing_profile

    def get_address(self):
        return "{line1} {line2}, {city} {postal}, {state}, {country}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            country=self.country,
            state=self.state,
            postal=self.postal_code
        )
