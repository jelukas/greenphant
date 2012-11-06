from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models import F
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage

#Category of the Courses Model
class Category(models.Model):
    name = models.CharField(_('Name'),blank=False,max_length=245)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


#Status of the Courses Model
""" There are 4: (building, checking, evaluating, published) """
class Status(models.Model):
    name = models.CharField(_('Status'),blank=False,max_length=245)

    class Meta:
        verbose_name_plural = _('statuses')

    def __unicode__(self):
        return self.name


#Course model
class Course(models.Model):
    user = models.ForeignKey(User,related_name='courses')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    price = models.DecimalField(_('price'),blank=False,max_digits=20,decimal_places=2)
    title = models.CharField(_('title'),blank=False,max_length=80)
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
    video = models.ImageField(_('Featured Video'),upload_to='course_promo_videos',blank=True)
    published_at = models.DateTimeField(null=True,blank=True)
    download_allowed = models.BooleanField(_('Download Allowed'))
    status = models.ForeignKey(Status,related_name='courses')
    category = models.ForeignKey(Category,related_name='courses',verbose_name=_('Category'))

    def __unicode__(self):
        return self.title

    def get_owner_id(self):
        return self.user.id


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
        return self.title

    def get_owner_id(self):
        return self.subject.course.user.id

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
    original_video_file = models.FileField(_('Video'),upload_to='original_lesson_videos',max_length=245)
    converted_video_file = models.FileField(upload_to='converted_lesson_videos',max_length=245,blank=True,null=True)

    def __unicode__(self):
        return self.original_video_file

    def get_owner_id(self):
        return self.lesson.subject.course.user.id

    #Delete the file when deleting the record
    def delete(self):
        import os.path
        if self.id:
            video = Video.objects.get(pk = self.id)
            if(os.path.isfile(video.original_video_file.path)):
                default_storage.delete(video.original_video_file.path)
        super(Video,self).delete()


#Lesson's Attach
class Attach(models.Model):
    lesson = models.OneToOneField(Lesson,unique=True,related_name='attach')
    file = models.FileField(_('File'),upload_to='lesson_attaches',max_length=245)

    def get_owner_id(self):
        return self.lesson.subject.course.user.id

    #Delete the file when deleting the record
    def delete(self):
        import os.path
        if self.id:
            attach = Attach.objects.get(pk = self.id)
            if(os.path.isfile(attach.file.path)):
                default_storage.delete(attach.file.path)
        super(Attach,self).delete()


#Courses Enrrollment's
class Enrollment(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='enrollments')
    course = models.ForeignKey(Course,verbose_name=_('Course'),related_name='enrollments')
    start_date = models.DateTimeField(_('Start Date'))

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

#Lesson comments
class Comment(models.Model):
    user = models.ForeignKey(User,verbose_name=_('User'),related_name='comments')
    lesson = models.ForeignKey(Lesson,verbose_name=_('Lesson'),related_name='comments')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    message = models.TextField(_('Message'),max_length=1000)

    def get_owner_id(self):
        return self.user.id