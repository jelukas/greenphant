from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from elearning.models import Enrollment, TesterSheet
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

"""
Esto debe ejecutarse en una tarea del cron de madrugada todos los dias.
Para ello usamos el script BASH tester_checking.sh
"""
class Command(BaseCommand):
    help = 'Comprobamos que los Testers hayan rellenado la ficha de evaluacion del curso despues de 30 dias'

    def handle(self, *args, **options):
        now = datetime.now()
        enrrollments = Enrollment.objects.filter(tester = True, active = True, start_date__lte= now - timedelta(days=30),)
        for enrrollment in enrrollments:
            if TesterSheet.objects.filter(user_id = enrrollment.user_id, course_id = enrrollment.course_id):
                enrrollment.tester = False
                enrrollment.save()
            else:
                enrrollment.active = False
                enrrollment.save()
                self.send_mail_bad_tester(enrrollment.user, enrrollment.course)
        self.stdout.write('Checking de Testers Realizado')

    def send_mail_bad_tester(self,tester,course):
            ctx_dict = {'tester': tester,'course': course}
            #Send Email to the Teacher
            message = render_to_string('elearning/email/unenroll_bad_tester.html',ctx_dict)
            subject = _('TrainingMe.net - You have been unenrolled in the course')
            msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [tester.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()