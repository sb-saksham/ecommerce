from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import GuestEmail
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, EmailActivation


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Full Name', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
            (
                None, {
                    'classes': ('wide',),
                    'fields': ('email', 'password1', 'password2')}
            ),
        )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    class Meta:
        model=User


admin.site.register(User, UserAdmin)
admin.site.register(EmailActivation)
# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)


class GuestModelAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuestModelAdmin)