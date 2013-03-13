from django import forms
from django.utils.translation import ugettext as _
from .models import Interest

class InterestList(forms.ModelForm):
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label=_('Tell us what category of courses interest you and you will be notified when they are published. If you\'re one of the top 5 in enrolling in a course, you can do for free to evaluate it.'))

    class Meta:
        model = Interest
        exclude = ('user',)
