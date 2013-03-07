from django.contrib import admin
from elearning.models import Category,Course,Status,Subject,Attach,Video,Lesson,Enrollment,Vote,Comment, Course_Vote


class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_at','user','lesson',)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user','course','start_date','tester',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','user','get_owner_email','price','status','category','created_at','published_at')

admin.site.register(Category)
admin.site.register(Course,CourseAdmin)
admin.site.register(Status)
admin.site.register(Subject)
admin.site.register(Attach)
admin.site.register(Video)
admin.site.register(Lesson)
admin.site.register(Enrollment,EnrollmentAdmin)
admin.site.register(Vote)
admin.site.register(Course_Vote)
admin.site.register(Comment,CommentAdmin)