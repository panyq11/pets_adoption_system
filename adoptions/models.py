from django.db import models
from admin_dashboard import Users, Pets

# Create your models here.
class AdoptPetInfo(models.Model):
    adopt_info_id = models.AutoField(primary_key=True)

    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    operator = models.ForeignKey(Users, on_delete=models.CASCADE)

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
