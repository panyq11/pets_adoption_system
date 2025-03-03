from django.db import models
from admin_dashboard.models import Users, Pets
from accounts.models import User  # 确保 User 导入
from posts.models import Pet  # 确保 Pet 导入

# Create your models here.
class AdoptPetInfo(models.Model):
    adopt_info_id = models.AutoField(primary_key=True)

    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="adopted_pets")# 添加了related_name="adopted_pets"
    operator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="processed_adoptions") # 添加了related_name="processed_adoptions"

    home_type = models.CharField(max_length=50)
    home_ownership = models.CharField(max_length=50)
    has_landlord_permission = models.BooleanField(default=False)
    has_other_pets = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    experience_with_pets = models.BooleanField(default=False)
    reason_for_adoption = models.CharField(max_length=200)
    vaccinated = models.BooleanField(default=False)
    pet_passport = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (

        ('submitted', 'Submitted'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    def __str__(self):
        return f"Application by {self.user.username} for {self.pet.name}\n will be reviewed by {self.operator.username}"


class AdoptionReview(models.Model):
    adopt_review_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adoption_requests")
    operator_username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="processed_reviews")
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )  # 审核状态
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adoption Review for {self.pet.name} by {self.adopter.username} - {self.status}"