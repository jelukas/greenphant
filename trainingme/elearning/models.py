import os
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.db.models import Max
from django.db.models import F
from django.db.models import Avg
from django.utils.encoding import smart_unicode
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage
from validatedfile import ValidatedFileField


#Category of the Courses Model
class Category(models.Model):
    name = models.CharField(_('Name'),blank=False,max_length=245)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name.encode('utf8')


#Status of the Courses Model
""" There are 5: (building, checking, evaluation period, published,forzen) """
class Status(models.Model):
    name = models.CharField(_('Status'),blank=False,max_length=245)

    class Meta:
        verbose_name_plural = _('statuses')

    def __unicode__(self):
        return self.name.encode('utf8')


#Course model
class Course(models.Model):
    slug = models.SlugField(max_length=75,unique=True)
    user = models.ForeignKey(User,related_name='courses')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    price = models.DecimalField(_('price'),blank=False,max_digits=20,decimal_places=2)
    title = models.CharField(_('title'),blank=False,max_length=40)
    LANGUAGE_CHOICES = (
        ('es-es','spanish (Spain)'),
        ('es-la','spanish (Latin)'),
        ('en','english'),
        ('ge','german'),
        ('pt','portuguese'),
        ('fr','french'),
        ('it','italian'),
        ('ch','chinese'),
        ('ru','russian'),
        ('hi','hindi'),
    )
    language = models.CharField(choices=LANGUAGE_CHOICES,default='es-es',blank=False,max_length=100)
    image = models.ImageField(_('Featured Image'),upload_to='course_images',blank=True)
    short_description = models.TextField(_('Short Description'),blank=False,max_length=160)
    large_description = models.TextField(_('Presentation'),blank=False)
    video = models.CharField(max_length=50,blank=True) #Youtube video URL
    published_at = models.DateTimeField(null=True,blank=True)
    download_allowed = models.BooleanField(_('Download Allowed'))
    status = models.ForeignKey(Status,related_name='courses')
    category = models.ForeignKey(Category,related_name='courses',verbose_name=_('Category'))

    class Meta:
        ordering = ['-created_at',]

    def __unicode__(self):
        return self.title

    def get_owner_email(self):
        return self.user.email

    def get_owner_id(self):
        return self.user.id

    def get_absolute_url(self):
        return "/elearning/course/%s/" % self.slug


    @property
    def get_scoring(self):
        score = self.votes.all().aggregate(Avg('rating'))
        return score['rating__avg']

    @property
    def social_amount(self):
        amount = (self.price*10)/100
        return  amount

    def enrroll_user(self,user_id):
        try:
            enrroll = Enrollment.objects.get(course_id = self.id,user_id = user_id)
        except ObjectDoesNotExist:
            enrroll = Enrollment.objects.create(user_id=user_id, course_id=self.id, start_date = datetime.now())
            enrroll.save()

    def rate(self,user_id,points):
        if self.id:
            from datetime import datetime
            if not self.user_had_vote_course(user_id):
                course_vote = Course_Vote(user_id = user_id, rating = points,created_at = datetime.now(),course_id = self.id)
                course_vote.save()
                return True
            else:
                return False

    def user_had_vote_course(self,user_id):
        if self.id:
            try:
                vote = self.votes.get(user_id=user_id)
            except Course_Vote.DoesNotExist:
                return False
            else:
                return True
        else:
            return False

        """
    def save(self):
        super(Course, self).save()
        #Resize the image preventing big images
        from PIL import Image
        """
        """
        On Ubuntu:

        # install libjpeg-dev with apt
        sudo apt-get install libjpeg-dev

        # reinstall PIL
        pip install -I PIL
        If that doesn't work, try this:

        sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
        sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
        sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
        """
        """
        size=(263, 130)
        if self.image:
            filename = self.image.path
            image = Image.open(filename)
            image.thumbnail(size, Image.ANTIALIAS)
            image.save(filename)
        """




#Subjects of the Courses
class Subject(models.Model):
    course = models.ForeignKey(Course,related_name='subjects')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    title = models.CharField(blank=False,max_length=245)
    order = models.IntegerField(blank=False)

    def __unicode__(self):
        return self.title + ' Orden: ' + str(self.order)

    def get_owner_id(self):
        return self.course.user.id

    class Meta:
        ordering = ["order"]


    """
    UPDATE tabla SET orden = orden - 1 WHERE orden > ordenActual AND orden <= nuevoOrden
    UPDATE tabla SET orden = nuevoOrden WHERE id = idRegistro
    """
    #To save and update the order
    def save(self):
        if not self.id:
            q = Subject.objects.filter(course=self.course).aggregate(Max('order'))
            self.order = int(q['order__max'] or 0) + 1
        else:
            subject = Subject.objects.get(pk = self.id)
            old_order = subject.order
            new_order = self.order
            if old_order > new_order:
                Subject.objects.filter(order__lt=old_order,order__gte = new_order, course = subject.course).update(order=F('order')+1)
            if old_order < new_order:
                Subject.objects.filter(order__gt=old_order,order__lte = new_order, course = subject.course).update(order=F('order')-1)
        super(Subject, self).save()

    #To delete and update the order
    def delete(self):
        if self.id:
            subject = Subject.objects.get(pk = self.id)
            old_order = subject.order
            Subject.objects.filter(order__gt = old_order, course = subject.course).update(order=F('order')-1)
        super(Subject,self).delete()


#Subject's Lessons
class Lesson(models.Model):
    subject = models.ForeignKey(Subject,related_name='lessons')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    title = models.CharField(blank=False,max_length=245)
    is_preview = models.BooleanField()
    order = models.IntegerField(blank=False)

    def __unicode__(self):
        return self.subject.title + ' -- ' + self.title

    def get_owner_id(self):
        return self.subject.course.user.id

    def user_had_vote_lesson(self,user_id):
        if self.id:
            try:
                vote = self.votes.get(user_id=user_id)
            except Vote.DoesNotExist:
                return False
            else:
                return True
        else:
            return False

    @property
    def get_scoring(self):
        score = self.votes.all().aggregate(Avg('points'))
        return score['points__avg']

    def vote(self,user_id,points):
        if self.id:
            from datetime import datetime
            if not self.user_had_vote_lesson(user_id):
                vote = Vote(user_id = user_id, points = points,created_at = datetime.now(),lesson_id = self.id)
                vote.save()
                return True
            else:
                return False

    class Meta:
        ordering = ["order"]

    #To save and update the order
    def save(self):
        if not self.id:
            q = Lesson.objects.filter(subject=self.subject).aggregate(Max('order'))
            self.order = int(q['order__max'] or 0) + 1
        else:
            lesson = Lesson.objects.get(pk = self.id)
            old_order = lesson.order
            new_order = self.order
            if old_order > new_order:
                Lesson.objects.filter(order__lt=old_order,order__gte = new_order,subject = lesson.subject).update(order=F('order')+1)
            if old_order < new_order:
                Lesson.objects.filter(order__gt=old_order,order__lte = new_order,subject = lesson.subject).update(order=F('order')-1)
        super(Lesson, self).save()

    #To delete and update the order
    def delete(self):
        if self.id:
            lesson = Lesson.objects.get(pk = self.id)
            old_order = lesson.order
            Lesson.objects.filter(order__gt = old_order, subject = lesson.subject).update(order=F('order')-1)
        super(Lesson,self).delete()


#Lesson's Videos
class Video(models.Model):
    lesson = models.OneToOneField(Lesson,unique=True,related_name='video')
    original_video_file = ValidatedFileField(_('Video'),upload_to='new_lesson_videos',max_length=245,content_types = ['video/mp4','video/x-ms-asf','video/avi','video/msvideo','video/x-msvideo','video/x-flv','video/quicktime','video/mpeg','video/x-ms-wmv','video/webm',])
    converted_video_file_mp4 = models.FileField(upload_to='converted_lesson_videos',max_length=245,blank=True,null=True)
    converted_video_file_webm = models.FileField(upload_to='converted_lesson_videos',max_length=245,blank=True,null=True)

    def __unicode__(self):
        return self.original_video_file.name

    def get_owner_id(self):
        return self.lesson.subject.course.user.id

    #Delete the file when deleting the record
#    def delete(self):
#        import os.path
#        video = Video.objects.get(pk = self.id)
#        if os.path.isfile(video.original_video_file.path):
#            default_storage.delete(video.original_video_file.path)
#        if os.path.isfile(video.converted_video_file_mp4.path):
#            default_storage.delete(video.converted_video_file_mp4.path)
#        if os.path.isfile(video.converted_video_file_webm.path):
#            default_storage.delete(video.converted_video_file_webm.path)
#        super(Video,self).delete()


#Lesson's Attach
class Attach(models.Model):
    lesson = models.OneToOneField(Lesson,unique=True,related_name='attach')
    file = models.FileField(_('File'),upload_to='lesson_attaches',max_length=245)

    def get_owner_id(self):
        return self.lesson.subject.course.user.id

    #Delete the file when deleting the record
#    def delete(self):
#        import os.path
#        if self.id:
#            attach = Attach.objects.get(pk = self.id)
#            if(os.path.isfile(attach.file.path)):
#                default_storage.delete(attach.file.path)
#        super(Attach,self).delete()


#Courses Enrrollment's
class Enrollment(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='enrollments')
    course = models.ForeignKey(Course,verbose_name=_('Course'),related_name='enrollments')
    start_date = models.DateTimeField(_('Start Date'),auto_created=True)
    tester = models.BooleanField()

    def get_owner_id(self):
        return self.user.id



#Lessons votes
class Vote(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='votes')
    lesson = models.ForeignKey(Lesson,verbose_name=_('Lesson'),related_name='votes')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    points = models.SmallIntegerField(verbose_name=_('Points'),max_length=1)

    def get_owner_id(self):
        return self.user.id

    def __str__(self):
        return unicode(self.user.username) + '--' + str(self.points)#Lessons votes


#Votes of Courses
class Course_Vote(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='course_votes')
    course = models.ForeignKey(Course,verbose_name=_('Course'),related_name='votes')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    rating = models.DecimalField(verbose_name=_('Rating'),max_digits=5,decimal_places=2)

    def get_owner_id(self):
        return self.user.id

    def __str__(self):
        return unicode(self.user.username) + '--' + str(self.rating)


#Lesson comments
class Comment(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='comments')
    lesson = models.ForeignKey(Lesson,verbose_name=_('Lesson'),related_name='comments')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    message = models.TextField(_('Message'),max_length=1000)
    parent_comment = models.ForeignKey('self',verbose_name=_('Comment'),related_name='replies',null=True, blank=True)

    def get_owner_id(self):
        return self.user.id

    def __unicode__(self):
        return unicode(self.created_at) + '--' + unicode(self.lesson.title) + '--' + unicode(self.user) + '--' + unicode(self.message)



# -------- Signals -----------

# Enrroll automatic in the course when the user is created
def auto_enrroll(sender, instance, created, **kwargs):
    if created:
        try:
            c = Course.objects.get(pk=23)
            e = Enrollment.objects.create(user=instance,course=c, start_date = datetime.now())
        except ObjectDoesNotExist:
            pass

post_save.connect(auto_enrroll, sender=User, dispatch_uid="auto-enrroll-when-register-signal")

# Create the user profile when create the User is created.
def delete_video_files(sender, instance, raw, **kwargs):
    if instance.id:
        old_video = Video.objects.get(pk=instance.id)
        if old_video.original_video_file != instance.original_video_file:
            if old_video.original_video_file:
                if os.path.isfile(old_video.original_video_file.path):
                    default_storage.delete(old_video.original_video_file.path)
            if old_video.converted_video_file_mp4:
                if os.path.isfile(old_video.converted_video_file_mp4.path):
                    default_storage.delete(old_video.converted_video_file_mp4.path)
            if old_video.converted_video_file_webm:
                if os.path.isfile(old_video.converted_video_file_webm.path):
                    default_storage.delete(old_video.converted_video_file_webm.path)

pre_save.connect(delete_video_files, sender=Video, dispatch_uid='video-delete-files-signal')