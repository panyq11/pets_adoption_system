from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate  # ✅ 这里改对了
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
User = get_user_model()

@require_http_methods(['GET', 'POST'])
def register(request):
    """🐾 用户注册视图"""
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'accounts/register.html', {"form": form})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')  # 确保用 `password1`
            password2 = form.cleaned_data.get('password2')

            # 🚨 检查用户名是否已存在，避免数据库报错
            if User.objects.filter(username=username).exists():
                form.add_error('username', "This username is already taken.")
                return render(request, 'accounts/register.html', {"form": form})

            # 🚨 检查密码是否一致
            if password1 != password2:
                form.add_error('password2', "Passwords do not match.")
                return render(request, 'accounts/register.html', {"form": form})

            # ✅ 创建用户，确保使用 `set_password()`
            user = User(username=username)
            user.set_password(password1)  # Django 推荐加密存储密码
            user.save()

            print(f"✅ 用户 {username} 注册成功！")
            return redirect(reverse('accounts:yfLogin'))  # 注册成功跳转到登录页
        else:
            print(form.errors)
            return render(request, 'accounts/register.html', {"form": form})  # 重新渲染页面显示错误


def yfLogin(request):
    """🐾 用户登录视图"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'accounts/login.html', {"form": form})  # 传递表单

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            print(f"🔍 Trying to authenticate user: {username}")
            # 🔍 **使用 `authenticate()` 进行身份验证**
            user = authenticate(request, username=username, password=password)
            print(f"✅ Authentication result: {user}")

            if user is not None:
                print(f"✅ 用户 {username} 登录成功！")
                login(request, user)  # 登录用户
                return redirect("adoptions:available_pets")  # 🚀 登录成功后跳转
            else:
                print("❌ 无效的用户名或密码")
                form.add_error(None, "Invalid username or password")

        return render(request, 'accounts/login.html', {"form": form})  # 显示错误信息



def profile(request):
    return render(request, 'accounts/profile.html')



