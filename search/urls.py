from django.urls import path
from .views import SearchQuery

app_name = "search"

urlpatterns = [
    path('', SearchQuery.as_view(), name='query'),
]
