from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save



#Billing where save the billing details of the user

class Billing(models.Model):
    user = models.OneToOneField(User,unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    paypal_account = models.EmailField(blank=True)
    name = models.CharField(max_length=250,blank=True)
    surname = models.CharField(max_length=250,blank=True)
    id_number = models.CharField(max_length=250,blank=True)

    def __unicode__(self):
        return "%s's billing details" % self.user


# -------- Signals -----------

# Create the user Billing Details when create the User is created.
def create_user_billing(sender, instance, created, **kwargs):
    if created:
        Billing.objects.create(user=instance,balance = 0)

post_save.connect(create_user_billing, sender=User, dispatch_uid="users-billing-creation-signal")
