from django.urls import path,re_path
from .views import sell_home

app_name = "usedClothes"

urlpatterns = [
    path('sell/', sell_home, name='sell_home'),
]