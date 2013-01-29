from django.core.management.base import BaseCommand, CommandError
from elearning.models import Video
from datetime import datetime
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
"""
For the cron: each 2 minutes or to put in the Convert Bash Script
*/2 * * * * root cd /home/luks/Escritorio/django/estable/greenphant/trainingme/ && /home/luks/Escritorio/django/estable/bin/python /home/luks/Escritorio/django/estable/greenphant/trainingme/manage.py prueba

"""

class Command(BaseCommand):
    #args = '<orignal_video_path converted_video_path>'
    #help = 'Actualizamos el Video'

    def handle(self, *args, **options):
#       self.stdout.write(args[0])
#       video = Video.objects.get(original_video_file=args[0])
#       video.original_video_file = args[0]
#       video.converted_video_file = args[1]
#       video.save()
#        self.stdout.write('prueba')
        user = User.objects.get(pk=3)
        user.email_user(_('One of Your video is ready'), _('You video is Ready'), from_email='trainingme@trainingme.net')
