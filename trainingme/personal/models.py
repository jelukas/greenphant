from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries import CountryField
import os
from django.utils.translation import ugettext as _
from django_countries.countries import COUNTRIES

# We add the most used countries first
COUNTRIES = list(COUNTRIES)
COUNTRIES.insert(0,('MX', _(u'Mexico')))
COUNTRIES.insert(0,('CL', _(u'Chile')))
COUNTRIES.insert(0,('US', _(u'United States')))
COUNTRIES.insert(0,('GB', _(u'United Kingdom')))
COUNTRIES.insert(0,('ES', _(u'Spain')))
COUNTRIES = tuple(COUNTRIES)

#Profile where save the personal details of the user
class Profile(models.Model):
    user = models.OneToOneField(User,unique=True,related_name='personal_profile')
    description = models.TextField(blank=False)
    subtitle = models.CharField(max_length=100,blank=False)
    image = models.ImageField(upload_to='profile_images',blank=True)
    country = CountryField(choices=COUNTRIES)
    state = models.CharField(max_length=250,blank=True)
    address = models.CharField(max_length=250,blank=True)
    phone_number = models.CharField(max_length=250,blank=True)
    website = models.CharField(max_length=250,blank=True)
    twitter_user = models.CharField(max_length=50,blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    googleplus_url = models.URLField(blank=True)
    is_first_login = models.BooleanField(default=False,editable=True)

    def __unicode__(self):
        return "%s's profile" % self.user


# -------- Signals -----------

# Create the user profile when create the User is created.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,description = _('Change your description'),is_first_login = True)

post_save.connect(create_user_profile, sender=User, dispatch_uid='users-profile-creation-signal')
