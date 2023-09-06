from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import *

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        exclude = ['bootcamp']

class OrgForm(forms.ModelForm):
    pass

class ZorgLocatieForm(OrgForm):
    class Meta:
        model = ZorgLocatie
        exclude = ['users']

class SportschoolForm(OrgForm):
    class Meta:
        model = Sportschool
        exclude = ['users']

class BootcampForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org', None)
        super().__init__(*args, **kwargs)
        self.fields['zorglocatie'].empty_label = None
        self.fields['sportschool'].empty_label = None
        if isinstance(org, ZorgLocatie):
            self.fields['sportschool'].queryset = org.sportscholen.all()
            self.fields['zorglocatie'].queryset = ZorgLocatie.objects.filter(pk=org.pk)
        if isinstance(org, Sportschool):
            self.fields['sportschool'].queryset = Sportschool.objects.filter(pk=org.pk)
            self.fields['zorglocatie'].queryset = org.zorglocaties.all()

    class Meta:
        model = Bootcamp
        exclude = ['user', 'trainer', 'deleted']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M'),
            'end_time': forms.TimeInput(format='%H:%M'),
        }
