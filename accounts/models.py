from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型，扩展 Django 的 AbstractUser
    """
    email = models.EmailField(unique=True)  # 设置 email 唯一
    username = models.CharField(max_length=50, unique=True)  # 自定义用户名长度
    phone_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)

    user_type = models.CharField(
        max_length=20,
        choices=[('User', 'User'), ('Admin', 'Admin')],
        default='User'
    )  # 用户类型（普通用户 / 管理员）

    status = models.CharField(
        max_length=10,
        choices=[('Active', 'Active'), ('Banned', 'Banned')],
        default='Active'
    )  # 用户状态

    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
