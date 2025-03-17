from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Pet(models.Model):
    """宠物信息表，对应数据库中的 pets 表"""
    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.CharField(max_length=10, choices=[('Young', 'Young'), ('Adult', 'Adult')])
    weight = models.FloatField()
    breed = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Adopted', 'Adopted')], default='Available')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 关联用户
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=[('Dog', 'Dog'), ('Cat', 'Cat')])

    def __str__(self):
        return f"{self.name} ({self.type})"

class PetImage(models.Model):
    pet_image_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="images")
    pet_image = models.ImageField(upload_to='pet_images/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.pet.name}"


class PostPetInfo(models.Model):
    """🐾 用户发布的宠物信息表，对应 `post_pet_info`"""
    post_info_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)  # 🐶 关联宠物信息

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ 这里用 `settings.AUTH_USER_MODEL`
        on_delete=models.CASCADE,
        related_name="posted_pets",
        null = True,
        blank = True
    )  # ✅ **确保正确关联 `accounts.User`**

    email = models.EmailField(max_length=254, blank=True, null=True)  # ✅新增Email字段

    home_type = models.CharField(max_length=20,
                                 choices=[('Apartment', 'Apartment'), ('House', 'House'),
                                          ('Townhouse', 'Townhouse'), ('Farm/Rural', 'Farm/Rural')],
                                 default='Apartment'
                                 )
    home_ownership = models.CharField(max_length=20,
                                      choices=[('Own', 'Own'), ('Rent', 'Rent'),
                                          ('Living with parents', 'Living with parents'), ('Other', 'Other')],
                                      default='Own'
                                      )
    has_other_pets = models.TextField(blank=True, null=True)
    has_children = models.CharField(max_length=10,
                                      choices=[('0', '0'), ('1', '1'),
                                           ('2', '2'), ('3', '3'),
                                           ('4', '4'), ('5', '5')],
                                      default='0'
                                      )
    experience_with_pets = models.TextField(blank=True, null=True)
    reason_for_fostering = models.TextField(blank=True, null=True)

    pet_passport = models.TextField(blank=True, null=True)
    vaccinated = models.CharField(max_length=20,
                                 choices=[('Yes', 'Yes'), ('No', 'No'),
                                         ],
                                 default='No'
                                 )

    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )  # 📌 **审核状态**

    created_at = models.DateTimeField(auto_now_add=True)
    review_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Post {self.post_info_id} - {self.pet.name} ({self.status})"

    def get_email(self):
        """✅ 通过 `user` 获取 `email`"""
        return self.user.email


class PostReview(models.Model):
    post_id = models.AutoField(primary_key=True)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_reviews")
    operator_username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_posts")
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Review for {self.pet.name} by {self.username.username} - {self.status}"
