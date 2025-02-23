from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    """宠物信息表，对应数据库中的 pets 表"""
    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.IntegerField()
    weight = models.FloatField()
    breed = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Adopted', 'Adopted')], default='Available')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')])

    def __str__(self):
        return f"{self.name} ({self.breed})"


class PostPetInfo(models.Model):
    """用户发布的宠物信息表，对应 post_pet_info"""
    post_info_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)  # 关联 pets 表
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_pets")  # 关联用户
    operator_username = models.CharField(max_length=150, blank=True, null=True)  # 管理员操作员
    home_type = models.CharField(max_length=100, blank=True, null=True)
    home_ownership = models.BooleanField(default=False)
    has_landlord_permission = models.BooleanField(default=False)
    has_other_pets = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    experience_with_pets = models.BooleanField(default=False)
    reason_for_fostering = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    pet_passport = models.BooleanField(default=False)
    vaccinated = models.BooleanField(default=False)

    def __str__(self):
        return f"Post {self.post_info_id} - {self.pet.name} ({self.status})"
