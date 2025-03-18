from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

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

    def clean_username(self):
        """ 确保用户名唯一 """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password2(self):
        """ 确保密码匹配 """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean(self):
        """ 确保最终表单校验一致 """
        cleaned_data = super().clean()
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Username is required',
        "max_length": "Username is too long",
        "min_length": "Username is too short"
    })

    password = forms.CharField(
        max_length=20,
        min_length=4,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Password is required',
            "max_length": "Password is too long",
            "min_length": "Password is too short"
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # 🚀 先检查用户名是否存在，再检查密码
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,  # 允许不填密码
        label="New Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'address', 'birthday', 'user_image', 'password']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:  # 仅当用户输入了新密码才更新
            user.set_password(password)

        if commit:
            user.save()
        return user

