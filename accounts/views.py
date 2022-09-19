from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.http import is_safe_url
from ecommerce.mixins import RequestFormAttachMixin, NextUrlMixin
from . import forms
from django.views.generic.edit import FormMixin
from django.views.generic import CreateView, DetailView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import GuestEmail, EmailActivation
from django.contrib import messages
from .signals import user_logged_in


User = settings.AUTH_USER_MODEL


class AccountsHome(DetailView, LoginRequiredMixin):
    template_name = 'accounts/home.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        return self.request.user


class AccountsEmailActivation(FormMixin, View):
    success_url = '/account/login/'
    form_class = forms.ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your account has been activated!")
                return redirect('accounts:login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    link = reverse("password-reset")
                    message = """Your email has already been activated. Do you want to <a href="{link}">reset your password ?<a/>
                    """.format(link=link)
                    messages.success(request, mark_safe(message))
                    return redirect('accounts:login')
        context = {'form': self.get_form}
        return render(request, 'accounts/email_activation.html', context=context)

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return form.form_valid()
        else:
            return form.form_invalid()

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        email_act_obj = EmailActivation.objects.email_exists(email).first()
        user = email_act_obj.user
        new_obj = EmailActivation.objects.create(email=email, user=user)
        new_obj.send_activation()
        return super(AccountsEmailActivation, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'accounts/email_activation.html', context=context)


class RegisterView(CreateView):
    form_class = forms.RegisterForm
    model = User
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('renting_object_create_url') is not None:
            context['redirected_from_renting'] = 'true'
        return context

    def get_success_url(self):
        redirect_url = self.request.session.get('renting_object_create_url', None)
        url = '/products/products/'
        if redirect_url is not None:
            url = '/accounts/login/'
        return url


class GuestRegister(CreateView):
    form_class = forms.GuestForm
    model = GuestEmail
    template_name = 'accounts/guest_form.html'
    success_url = '/products/products/'


def guest_page(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.method == 'POST':
        form1 = forms.GuestForm(request.POST)
        if form1.is_valid():
            email = form1.cleaned_data.get('email')
            new_guest_email = GuestEmail.objects.create(email=email)
            request.session['guest_email_id'] = new_guest_email.id
            if is_safe_url(redirect_path, request.get_host()) and redirect_path is not None:
                return redirect(redirect_path)
            else:
                return redirect('accounts:register')
    else:
        return redirect('accounts:register')


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = forms.LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


def guest_create(request):
    if request.method == 'POST':
        guest_form = forms.GuestForm(request.POST)
        if guest_form.is_valid():
            email = guest_form.cleaned_data.get('email')
            guest_object = GuestEmail.objects.create(email=email)
            request.session['guest_email_id'] = guest_object.id
            if request.session.get('renting_object_create_url') is not None:
                return redirect(request.session['renting_object_create_url'])
            else:
                redirect('/')
    guest_form = forms.GuestForm()
    context = {'form': guest_form}
    return render(request, 'accounts/guest_form.html', context=context)