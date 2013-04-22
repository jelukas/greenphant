from django.core.management.base import BaseCommand, CommandError
from elearning.models import Course
from django.contrib.auth.models import User
from social_auth.db.django_models import UserSocialAuth
from urllib2 import urlopen, HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

class Command(BaseCommand):
    args = '<course_id>'
    help = 'Matriculamos a todos los usuarios'

    def handle(self, *args, **options):
        users_social_auths = UserSocialAuth.objects.all()
        for users_social_auth in users_social_auths:
            profile = users_social_auth.user.get_profile()
            if not profile.image:
                if users_social_auth.provider == 'google-oauth2' :
                    pass
                elif users_social_auth.provider == 'twitter':
                    pass
                elif users_social_auth.provider == 'facebook':
                    pass
        self.stdout.write('Fotos Sociales Cogidas')
