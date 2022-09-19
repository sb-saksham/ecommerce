"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views
from cart.views import cart_api_update_view
from addresses.views import checkout_address_view, checkout_address_use_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('accounts.passwords.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('renting/', include('renting.urls')),
    path('account/', include("accounts.urls"), name='accounts'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('api/cart/', cart_api_update_view, name='cart-api'),
    path('search/', include('search.urls')),
    path('recycle/', include('usedClothes.urls')),
    path('checkout/address/create/', checkout_address_view, name='checkout_address_create'),
    path('checkout/address/use/', checkout_address_use_view, name='checkout_address_use_view'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
