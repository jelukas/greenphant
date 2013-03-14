from django.forms import ModelForm
from personal.models import Profile
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','is_first_login')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)