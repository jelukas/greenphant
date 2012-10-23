from django.forms import ModelForm
from elearning.models import Course

class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('user','published_at','status')
