from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Username is required',
        "max_length": "Username is too long",
        "min_length": "Username is too short"
        })

    password1 = forms.CharField(
        max_length=20,
        min_length=4,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Password is required',
            "max_length": "Password is too long",
            "min_length": "Password is too short"
        }
    )
    password2 = forms.CharField(
        max_length=20,
        min_length=4,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please confirm your password',
            "max_length": "Password is too long",
            "min_length": "Password is too short"
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data