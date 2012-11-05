from django.db import models
from django.contrib.auth.models import User
from elearning.models import Course
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _


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


#Withdraw : That are the withdraws records.
class Withdraw(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='withdraws')
    datetime = models.DateTimeField(blank=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2,verbose_name=_('Amount'),blank=False)
    #Paypal account where the  payment was send:
    sent_to = models.CharField(blank=False,max_length=255)


#ORDERS
class Order(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='orders')
    course = models.ForeignKey(Course,verbose_name=_('Course'),related_name='orders')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2,verbose_name=_('Amount'),blank=False)
    is_refund = models.BooleanField(blank=False)
    #This is the date when the amount of this order is sent to the Seller balance.
    datetime_cleared = models.DateTimeField(blank=True,null=True)

    def get_seller(self):
        return self.course.user

    def get_buyer(self):
        return self.user




# -------- Signals -----------

# Create the user Billing Details when create the User is created.
def create_user_billing(sender, instance, created, **kwargs):
    if created:
        Billing.objects.create(user=instance,balance = 0)

post_save.connect(create_user_billing, sender=User, dispatch_uid="users-billing-creation-signal")
