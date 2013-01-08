from django.forms import ModelForm
from django.forms import widgets
from elearning.models import Course,Subject,Lesson,Video, Attach, Comment


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('user','published_at','status','slug')


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        exclude = ('course','created_at','order')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('created_at','user','lesson')


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ('subject','created_at','order')


class VideoForm(ModelForm):
    class Meta:
        model = Video
        exclude = ('lesson','converted_video_file_mp4','converted_video_file_webm')


class AttachForm(ModelForm):
    class Meta:
        model = Attach
        exclude = ('lesson',)
