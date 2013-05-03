from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Message


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','is_first_login')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('message',)


class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)