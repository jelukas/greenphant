from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from elearning.models import Video
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from ...utils.videoutils import get_video_length



class Command(BaseCommand):
    help = 'Calculamos la duracion de todos los videos y actualizamos en la database'

    def handle(self, *args, **options):
        videos = Video.objects.all()
        for video in videos:
            if video.converted_video_file_mp4:
                path = video.converted_video_file_mp4.path
                seconds = get_video_length(path)
                video.duration = seconds
                video.save()

        self.stdout.write('update duration de videos realizado')