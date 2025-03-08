from django.db import models

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)  # ✅ 明确指定主键类型
    username = models.CharField(max_length=150)

class Pets(models.Model):
    id = models.BigAutoField(primary_key=True)  # ✅ 明确指定主键类型
    name = models.CharField(max_length=100)

from django.db import models

# Create your models here.
