from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import LoginView, RegisterView, guest_page, guest_create, AccountsHome, AccountsEmailActivation

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', AccountsHome.as_view(), name="home"),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('guest/', guest_page, name='guest'),
    path('guest/create/', guest_create, name='guest_create'),
    re_path(r'^user/activate/(?P<key>[0-9A-Za-z]+)/$', AccountsEmailActivation.as_view(), name='email-activation'),
    path('user/reactivate/', AccountsEmailActivation.as_view(), name='resend-activation'),
]
