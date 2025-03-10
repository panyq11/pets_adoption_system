from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm
from django.contrib.auth import get_user_model
User = get_user_model()

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == "GET":
        form = RegisterForm()  # 确保 GET 请求时返回表单
        return render(request, 'accounts/register.html', {"form": form})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            User.objects.create_user(username=username, password=password) # 将user信息存储到数据库当中
            return redirect(reverse('accounts:login'))
        else:
            print(form.errors)
            return render(request, 'accounts/register.html', {"form": form})  # 重新渲染页面并显示错误

def profile(request):
    return render(request, 'accounts/profile.html')


def accounts(request):
    return render(request, 'accounts/login.html')
