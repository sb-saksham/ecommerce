from django.db import models
from django.conf import settings
from utils import unique_order_id
from django.db.models.signals import pre_save

User = settings.AUTH_USER_MODEL

sizes_choices = (
    ('large', 'L'),
    ('medium', 'M'),
    ('small', 'S'),
    ('extra_large', 'XL'),
)
selling_options = (
    ('us', "Sell to Us(Team Style'em.com)"),
    ('other_user', "Put on Sale for anybody(Sell to any User)"),
)


class ImagesOfClothes(models.Model):
    image = models.ImageField(upload_to="usedClothes/recycling_clothes")


class Clothes(models.Model):
    images = models.ForeignKey(to=ImagesOfClothes, related_name='cloth_related', on_delete=models.CASCADE, null=True, blank=True)
    apparel_type = models.CharField(max_length=35)  # i.e., t-shirt,jeans,etc.....
    size = models.CharField(max_length=12, choices=sizes_choices, null=True, blank=True)
    cloth_type = models.CharField(max_length=35, null=True, blank=True)  # ~ kosa,silk,etc....)

    def __str__(self):
        return self.apparel_type


class RecycleOrder(models.Model):
    order_id = models.CharField(max_length=8, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    sell_to = models.CharField(max_length=25, choices=selling_options)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    received = models.BooleanField(default=False)


def recycle_order_pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id(instance)
    return instance.order_id


pre_save.connect(recycle_order_pre_save_order_id_receiver, sender=RecycleOrder)