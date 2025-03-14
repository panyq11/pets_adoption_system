from django import forms
from .models import Pet, PetImage

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'sex', 'age', 'weight', 'breed', 'size']

class PetImageForm(forms.Form):
    pet_images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )
