from django.forms import ModelForm
from personal.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
