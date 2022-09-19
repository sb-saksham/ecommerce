from django import forms
from .models import Clothes


class ImageForm(forms.Form):
    image = forms.ImageField()
    
    
class ClothForm(forms.ModelForm):
    apparel_type = forms.TextInput()
    size = forms.TextInput()
    cloth_type = forms.TextInput()

    class Meta:
        model = Clothes
        fields = '__all__'