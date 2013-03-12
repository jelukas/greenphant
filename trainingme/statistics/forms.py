from django import forms
from django.utils.translation import ugettext as _
from .models import Interest

class InterestList(forms.ModelForm):
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label=_('What type of courses interest you ?'))

    class Meta:
        model = Interest
        exclude = ('user',)
