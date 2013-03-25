# -*- encoding: utf-8 -*-
from django.utils.encoding import smart_unicode
from django.core.management.base import BaseCommand, CommandError
from elearning.models import Video
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from ...utils.videoutils import get_video_length


class Command(BaseCommand):
    args = '<old_video_path orignal_video_path converted_video_path_mp4  converted_video_path_webm>'
    help = 'Actualizamos el Video'

    def handle(self, *args, **options):
        video = Video.objects.get(original_video_file=smart_unicode(args[1]))
        video.original_video_file = smart_unicode(args[0])
        video.converted_video_file_mp4 = smart_unicode(args[2])
        video.converted_video_file_webm = smart_unicode(args[3])
        path = video.converted_video_file_mp4.path
        seconds = get_video_length(path)
        video.duration = seconds
        video.save()
        user = User.objects.get(pk=video.get_owner_id())
        user.email_user(_('One of Your video is ready'), _('Your video is Ready'), from_email='trainingme@trainingme.net')
        self.stdout.write('Actualizado el Video '+ str(video.id))