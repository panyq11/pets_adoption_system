# adoptions/forms.py
from django import forms
from .models import AdoptPetInfo

class AdoptPetInfoForm(forms.ModelForm):
    class Meta:
        model = AdoptPetInfo

        fields = [
            'home_type',
            'home_ownership',
            'has_landlord_permission',
            'has_other_pets',
            'has_children',
            'experience_with_pets',
            'reason_for_adoption',
        ]
