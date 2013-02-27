from django.forms import ModelForm
from django.forms import widgets
from elearning.models import Course,Subject,Lesson,Video, Attach, Comment
from django.forms import ValidationError
from django.utils.translation import ugettext as _


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('user','published_at','status','slug',)

    def clean_price(self):
        data = self.cleaned_data['price']
        if data < 10:
            raise ValidationError(_("The minimum price must be 10 EUR"))
            # Always return the cleaned data, whether you have changed it or
        # not.
        return data

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        exclude = ('course','created_at','order')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('created_at','user','lesson','parent_comment')


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
