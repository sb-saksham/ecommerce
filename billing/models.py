from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillingManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            """
                Logged-in user checkout
                Remembers the payment stuff
            """
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            """
                Guest user checkout
                Auto reloads payment stuff
            """
            guest_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_obj.email)
        else:
            obj = None
            created = False
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_no = models.CharField(max_length=10, default=1111111111, null=True, blank=True)
    # customer_id = Payment gateway id

    objects = BillingManager()

    def __str__(self):
        return self.email


# def billing_profile_created_reciever(sender, instance, created, *args, **kwargs):
#     if created:
#         print('Send the id to Payment gateway')
#         instance.customer_id = Newid
#         instance.save()


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)