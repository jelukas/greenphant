from django.core.management.base import BaseCommand, CommandError
from elearning.models import Video
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
class Command(BaseCommand):
    args = '<old_video_path orignal_video_path converted_video_path_mp4  converted_video_path_webm>'
    help = 'Actualizamos el Video'

    def handle(self, *args, **options):
        self.stdout.write(args[0])
        video = Video.objects.get(original_video_file=args[1])
        video.original_video_file = args[0]
        video.converted_video_file_mp4 = args[2]
        video.converted_video_file_webm = args[3]
        video.save()
        user = User.objects.get(pk=video.get_owner_id())
        user.email_user(_('One of Your video is ready'), _('You video is Ready'), from_email='trainingme@trainingme.net')
        self.stdout.write('Actualizado el Video '+ str(video.id))