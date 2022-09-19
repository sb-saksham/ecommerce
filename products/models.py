import random
import os
from django.shortcuts import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from .utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(per_day_renting_price__icontains=query) | Q(slug__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):  # Product.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, p_id):
        qs = self.get_queryset().filter(id=p_id)  # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=2000)
    slug = models.SlugField(unique=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    description = models.CharField(max_length=264)
    price = models.IntegerField(blank=False, default=0)
    picture = models.ImageField(upload_to='products/product_image/', blank=True, null=True)
    per_day_renting_price = models.DecimalField(default=0.0, null=True, blank=True, max_digits=20, decimal_places=2)

    objects = ProductManager()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("products:each_product", kwargs={"slug": self.slug})


def product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_slug, sender=Product)