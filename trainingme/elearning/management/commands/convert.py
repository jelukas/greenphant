from django.core.management.base import BaseCommand, CommandError
from elearning.models import Video

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
        self.stdout.write('Actualizado el Video '+ str(video.id))