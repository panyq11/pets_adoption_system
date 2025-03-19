from django.db import models
from accounts.models import User
from posts.models import Pet

# Create your models here.
class AdoptPetInfo(models.Model):
    adopt_info_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adopted_pets")# 添加了related_name="adopted_pets"
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="processed_adoptions") # 添加了related_name="processed_adoptions"

    home_type = models.CharField(max_length=50)
    home_ownership = models.CharField(max_length=50)
    has_landlord_permission = models.BooleanField(default=False)
    has_other_pets = models.TextField(blank=True, null=True)
    has_children = models.CharField(max_length=10,
                                    choices=[('0', '0'), ('1', '1'),
                                             ('2', '2'), ('3', '3'),
                                             ('4', '4'), ('5', '5')],
                                    default='0'
                                    )
    experience_with_pets = models.TextField()
    reason_for_adoption = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.user.username} for {self.pet.name}\n will be reviewed by {self.operator.username}"


class AdoptionReview(models.Model):
    adopt_review_id = models.AutoField(primary_key=True)
    adopt_info = models.ForeignKey(
        AdoptPetInfo, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adoption_requests")
    operator_username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="processed_reviews")
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )  # 审核状态
    applied_at = models.DateTimeField(auto_now_add=True)
    review_time = models.DateTimeField(null=True, blank=True)  # 确认这里
    def __str__(self):
        return f"Adoption Review for {self.pet.name} by {self.adopter_username.username} - {self.status}"