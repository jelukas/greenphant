from django.db import models
from django.contrib.auth.models import User
from elearning.models import Course
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from datetime import datetime

#Billing where save the financial details of the user
class Billing(models.Model):
    user = models.OneToOneField(User,unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    paypal_account = models.EmailField(blank=True)
    name = models.CharField(max_length=250,blank=True)
    surname = models.CharField(max_length=250,blank=True)
    id_number = models.CharField(max_length=250,blank=True)

    def __unicode__(self):
        return "%s's financial details" % self.user


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
    #Paypal Transaction ID
    paypal_txn_id = models.CharField(max_length=255)

    def get_seller(self):
        return self.course.user

    def get_buyer(self):
        return self.user

    def clear_amount(self):
        self.datetime_cleared = datetime.now()
        self.save()
        self.user.billing.balance = self.user.billing.balance + self.amount
        self.user.billing.save()

    def __unicode__(self):
        return str(self.created_at) + ' -- ' + self.course.title + ' -- ' + self.user.username + ' -- ' + str(self.datetime_cleared)



# -------- Signals -----------

# Create the user Billing Details when create the User is created.
def create_user_billing(sender, instance, created, **kwargs):
    if created:
        Billing.objects.create(user=instance,balance = 0)

post_save.connect(create_user_billing, sender=User, dispatch_uid="users-financial-creation-signal")


# On save a new withdraw , the balance must down with the amount
def reduce_balance(sender, instance, created, **kwargs):
    if created:
        billing = Billing.objects.get(user_id=instance.user.id)
        billing.balance = billing.balance - instance.amount
        billing.save()

post_save.connect(reduce_balance, sender=Withdraw, dispatch_uid="new-withdraw-reduce-balance-signal")
