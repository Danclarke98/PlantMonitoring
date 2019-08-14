import self as self
from django import forms
from django.forms import ModelChoiceField

from .models import Device


class ModifyDevicesForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ModifyDevicesForm, self).__init__(*args, **kwargs)

        devices = Device.objects.filter(owner=self.user)

        self.fields['device'] = forms.ModelChoiceField(queryset=devices)
