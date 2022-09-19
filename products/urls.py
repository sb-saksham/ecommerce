from django.urls import path, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='all_products'),
    re_path(r'products/(?P<slug>[-\w]+)/$', views.ProductDetail.as_view(), name='each_product'),
]