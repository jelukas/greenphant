from django.contrib import admin
from elearning.models import Category,Course,Status,Subject,Attach,Video,Lesson,Enrollment,Vote,Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_at','user','lesson',)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user','course','start_date',)

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Status)
admin.site.register(Subject)
admin.site.register(Attach)
admin.site.register(Video)
admin.site.register(Lesson)
admin.site.register(Enrollment,EnrollmentAdmin)
admin.site.register(Vote)
admin.site.register(Comment,CommentAdmin)