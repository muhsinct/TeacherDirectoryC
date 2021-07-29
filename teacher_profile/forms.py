from django import forms
from django.core.validators import FileExtensionValidator
from .models import Profiles


class ProfileImageUploadForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    zip_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip'])])
