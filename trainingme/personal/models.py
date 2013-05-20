from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries import CountryField
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django_countries.countries import COUNTRIES
from statistics.models import Interest



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

    def had_filled_poll(self):
        filled = False
        if Interest.objects.filter(user_id=self.user.id).count():
            filled = True
        return filled

    def get_unread_received_messages(self):
        return self.user.messages_received.filter(is_read=False)

    def count_unread_received_messages(self):
        return self.user.messages_received.filter(is_read=False).count()

    def is_completed(self):
        completed = True
        if not self.description:
            completed = False
        if not self.subtitle:
            completed = False
        if not self.country:
            completed = False
        if not self.state:
            completed = False
        if not self.user.first_name:
            completed = False
        if not self.user.last_name:
            completed = False
        return completed


class Message(models.Model):
    from_user = models.ForeignKey(User,verbose_name=_('From User'),related_name='messages_sent')
    to_user = models.ForeignKey(User,verbose_name=_('To User'),related_name='messages_received')
    subject = models.CharField(max_length=200)
    message = models.TextField(_('Message'),max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False,editable=True)

    def __unicode__(self):
        return unicode(self.from_user)

    def get_url(self):
        return reverse('personal.views.list_messages')

    class META:
        ordering = ['created_at']



# -------- Signals -----------

# Create the user profile when create the User is created.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,description = _('Change your description'),is_first_login = True)

post_save.connect(create_user_profile, sender=User, dispatch_uid='users-profile-creation-signal')


# Email Message
def send_email_message(sender, instance, created, **kwargs):
    if created:
        message = instance
        if message.to_user.email:
            ctx_dict = { 'message': message }
            email_message = render_to_string('personal/email/mail.html',ctx_dict)
            if not message.subject:
                subject = _('TrainingMe.net - New Message')
            else:
                subject = message.subject
            msg = EmailMessage(subject, email_message, settings.DEFAULT_FROM_EMAIL, [message.to_user.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

post_save.connect(send_email_message, sender=Message, dispatch_uid='send-email-message-signal')


#Get the avatars from Social Auth
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from social_auth.backends import google
from social_auth.signals import socialauth_registered, pre_update

def social_extra_values(sender, user, response, details, **kwargs):
    result = False

    if "id" in response:
        from urllib2 import urlopen, HTTPError
        from django.template.defaultfilters import slugify
        from django.core.files.base import ContentFile

        try:
            url = None
            if sender == FacebookBackend:
                url = "http://graph.facebook.com/%s/picture?type=large"\
                      % response["id"]
            elif sender == google.GoogleOAuth2Backend and "picture" in response:
                url = response["picture"]
            elif sender == TwitterBackend:
                url = response["profile_image_url"]

            if url:
                profile = user.get_profile()
                if not profile.image:
                    avatar = urlopen(url)
                    profile.image.save(slugify(user.username + " social") + '.jpg',
                        ContentFile(avatar.read()))
                    profile.save()

        except HTTPError:
            pass

        result = True

    return result

socialauth_registered.connect(social_extra_values, sender=None)
pre_update.connect(social_extra_values, sender=None)