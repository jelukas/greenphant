from django.contrib import admin
from elearning.models import Category,Course,Status,Subject,Attach,Video,Lesson,Enrollment,Vote,Comment, Course_Vote, TesterSheet
from django.core.urlresolvers import reverse
from datetime import timedelta


class AttachAdmin(admin.ModelAdmin):
    list_display = ('lesson','file','get_course',)

    def get_course(self,object):
        url = reverse('admin:%s_%s_change' %( object.lesson.subject.course._meta.app_label,   object.lesson.subject.course._meta.module_name),  args=[ object.lesson.subject.course.id] )
        return u'<a href="%s">%s</a>' %(url,  object.lesson.subject.course.title)
    get_course.short_description = 'Course'
    get_course.allow_tags = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_at','user','lesson',)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user','get_user_email','course','start_date','tester','active')

    def get_user_email(self,object):
        url = reverse('admin:%s_%s_change' %( object.user._meta.app_label,   object.user._meta.module_name),  args=[ object.user_id] )
        return u'<a href="%s">%s</a>' %(url,  object.user.email)
    get_user_email.short_description = 'View User'
    get_user_email.allow_tags = True


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','user','get_owner_email','price','status','category','created_at','published_at','learning_course')
    list_filter = ('status',)
    search_fields = ['title','user__email']


    def learning_course(self,object):
        url = reverse('elearning.views.learning_course', args=(object.id,))
        return u'<a href="%s">%s</a>' %(url, 'View In Site')
    learning_course.short_description = 'View In Site'
    learning_course.allow_tags = True


class TesterSheetAdmin(admin.ModelAdmin):
    list_display = ('created_at','course','user','video_rating','audio_rating','course_rating','price_1_rating','price_2_rating','price_2_rating')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('original_video_file','lesson','video_duration','duration','get_course',)

    def video_duration(self,object):
        duration = 0
        if object.duration:
            duration = object.duration
        return u'%s' %(str(timedelta(seconds=int(duration))))
    video_duration.short_description = 'Duration h:m:s'

    def get_course(self,object):
        url = reverse('admin:%s_%s_change' %( object.lesson.subject.course._meta.app_label,   object.lesson.subject.course._meta.module_name),  args=[ object.lesson.subject.course.id] )
        return u'<a href="%s">%s</a>' %(url,  object.lesson.subject.course.title)
    get_course.short_description = 'Course'
    get_course.allow_tags = True

admin.site.register(Category)
admin.site.register(Course,CourseAdmin)
admin.site.register(Status)
admin.site.register(Subject)
admin.site.register(Attach,AttachAdmin)
admin.site.register(Video,VideoAdmin)
admin.site.register(Lesson)
admin.site.register(Enrollment,EnrollmentAdmin)
admin.site.register(Vote)
admin.site.register(Course_Vote)
admin.site.register(TesterSheet,TesterSheetAdmin)
admin.site.register(Comment,CommentAdmin)