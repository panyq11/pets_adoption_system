from django import forms
from .models import Pet, PetImage, PostPetInfo

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'sex', 'age', 'weight', 'breed', 'size', 'type']

class PetImageForm(forms.ModelForm):
    """🐾 宠物图片表单"""
    class Meta:
        model = PetImage
        fields = ['pet_image']


class PostPetInfoForm(forms.ModelForm):
    class Meta:
        model = PostPetInfo
        fields = [
            'email',  # ✅ **发布人 Email**
            'home_type', 'home_ownership',
            'has_other_pets', 'has_children', 'experience_with_pets',
            'reason_for_fostering', 'pet_passport', 'vaccinated'
        ]