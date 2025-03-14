from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'  # 定义当前应用名称，方便在模板中使用 URL 反向解析

urlpatterns = [
    # 登录页面,
    path('', views.yfLogin, name='yfLogin'),

    # 注册页面，由自定义的 register 视图处理
    path('register/', views.register, name='register'),

    path('profile/', views.profile, name='profile')

]
