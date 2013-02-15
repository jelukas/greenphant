from django.core.management.base import BaseCommand, CommandError
from elearning.models import Course
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<course_id>'
    help = 'Matriculamos a todos los usuarios'

    def handle(self, *args, **options):
        users = User.objects.all()
        course = Course.objects.get(pk=args[0])
        for user in users:
            course.enrroll_user(user.id)
        self.stdout.write('Automraticulacion realizada')
