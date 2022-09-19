from django.contrib import admin
from .models import RecycleOrder, ImagesOfClothes, Clothes

admin.site.register(Clothes)
admin.site.register(RecycleOrder)
admin.site.register(ImagesOfClothes)

