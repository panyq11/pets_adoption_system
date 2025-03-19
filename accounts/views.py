from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate  # ✅ 这里改对了
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
User = get_user_model()
from .forms import UserProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
import datetime



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

                # 🚀 **判断用户类型**
                if user.user_type == "Admin":
                    return redirect(reverse("admin_dashboard:admin_dashboard"))  # **管理员跳转**
                else:
                    return redirect("adoptions:available_pets")  # 🚀 登录成功后跳转
            else:
                print("❌ 无效的用户名或密码")
                form.add_error(None, "Invalid username or password")

        return render(request, 'accounts/login.html', {"form": form})  # 显示错误信息


def logout_view(request):
    logout(request)
    return redirect(reverse("accounts:yfLogin"))


@csrf_exempt
@login_required
def profile(request):
    user = request.user

    if request.method == 'GET':
        # 返回HTML
        return render(request, 'accounts/Profile.html', {
            'user': user,
            # 你还可以传别的 context
        })

    elif request.method == 'POST':
        # 处理更新
        user.email = request.POST.get('email', user.email)
        user.phone_no = request.POST.get('phone_no', user.phone_no)
        user.address = request.POST.get('address', user.address)

        birthday_str = request.POST.get('birthday', '')
        if birthday_str:
            try:
                # 假设前端日期格式是 "YYYY-MM-DD"
                user.birthday = datetime.datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                # 如果转换失败，保留原值或根据需要处理错误
                messages.error(request, "Invalid birthday format.")

        new_password = request.POST.get('password', '')
        if new_password and new_password != "********":
            user.set_password(new_password)
            # 更新会话认证，防止修改密码后用户被登出
            update_session_auth_hash(request, user)
        # 处理头像上传（字段名称为 'avatar'）
        if 'avatar' in request.FILES:
            user.user_image = request.FILES['avatar']
        user.save()
        # 返回 JSON 响应，前端可以根据此响应做页面刷新或提示
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



def admin_dashboard(request):
    """🐾 管理员控制面板"""
    return render(request, "admin_dashboard/admin_dashboard.html")



