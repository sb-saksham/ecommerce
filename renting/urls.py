from django.urls import path
from .views import rent_initiate, rent_edit_view, rent_status, rent_tracking

app_name = 'renting'

urlpatterns = [
    path('initiate/', rent_initiate, name='rent_initiate'),
    path('rent/', rent_status, name='rent_status'),
    path('edit/', rent_edit_view, name='rent_edit'),
    path('renting/', rent_tracking, name="renting_for_user"),
]
