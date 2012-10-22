from django.db import models
from django.contrib.auth.models import User

#Category of the Courses Model
class Category(models.Model):
    name = models.CharField(blank=False,max_length=245)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


#Status of the Courses Model
class Status(models.Model):
    name = models.CharField(blank=False,max_length=245)

    class Meta:
        verbose_name_plural = 'statuses'

    def __unicode__(self):
        return self.name


#Course model
class Course(models.Model):
    user = models.ManyToManyField(User,related_name='courses')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    price = models.DecimalField(blank=False,max_digits=20,decimal_places=2)
    title = models.CharField(blank=False,max_length=245)
    language = models.CharField(blank=False,max_length=245)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='course_images',blank=True)
    video = models.ImageField(upload_to='course_promo_videos',blank=True)
    published_at = models.DateTimeField(blank=True)
    status = models.ManyToManyField(Status,related_name='courses')
    category = models.ManyToManyField(Category,related_name='courses')

    def __unicode__(self):
        return self.title


#Subjects of the Courses
class Subject(models.Model):
    course = models.ManyToManyField(Course,related_name='subjects')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    title = models.CharField(blank=False,max_length=245)

    def __unicode__(self):
        return self.title


#Subject's Lessons
class Lesson(models.Model):
    subject = models.ManyToManyField(Subject,related_name='lessons')
    created_at = models.DateTimeField(blank=False,auto_now_add=True)
    title = models.CharField(blank=False,max_length=245)
    is_preview = models.BooleanField()

    def __unicode__(self):
        return self.title


#Lesson's Videos
class Video(models.Model):
    lesson = models.OneToOneField(Lesson,unique=True,related_name='video')
    original_video_file = models.FileField(upload_to='original_lesson_videos',max_length=245)
    converted_video_file = models.FileField(upload_to='converted_lesson_videos',max_length=245,blank=True,null=True)

    def __unicode__(self):
        return self.original_video_file


#Lesson's Attach
class Attach(models.Model):
    lesson = models.OneToOneField(Lesson,unique=True,related_name='attach')
    file = models.FileField(upload_to='lesson_attaches',max_length=245)
