from django.forms import ModelForm
from elearning.models import Course,Subject,Lesson,Video, Attach


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('user','published_at','status')


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        exclude = ('course','created_at','order')


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
