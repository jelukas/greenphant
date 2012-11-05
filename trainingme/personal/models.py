from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries import CountryField
import os



#Profile where save the personal details of the user
class Profile(models.Model):
    user = models.OneToOneField(User,unique=True,related_name='personal_profile')
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='profile_images',blank=True)
    country = CountryField()
    state = models.CharField(max_length=250,blank=True)
    address = models.CharField(max_length=250,blank=True)
    phone_number = models.CharField(max_length=250,blank=True)
    address = models.CharField(max_length=250,blank=True)
    website = models.CharField(max_length=250,blank=True)
    is_first_login = models.BooleanField(default=False,editable=True)

    def __unicode__(self):
        return "%s's profile" % self.user


# -------- Signals -----------

# Create the user profile when create the User is created.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,description = "Change your description",is_first_login = True)

post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profile-creation-signal")
