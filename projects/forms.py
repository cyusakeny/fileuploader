from django.forms import ModelForm
from .models import File


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'size', 'extension']


class RenameForm(ModelForm):
    class Meta:
        model = File
        fields = ['name']
