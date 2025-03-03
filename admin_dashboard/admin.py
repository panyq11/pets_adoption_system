from django.contrib import admin

# Register your models here.
from django.contrib import admin
from accounts.models import User  # 确保 User 存在于 accounts
from posts.models import Pet, PostReview, PetImage  # 确保 Pet 相关的模型在 posts 里
from adoptions.models import AdoptionReview  # 确保 AdoptionReview 在 adoptions 里

admin.site.register(User)
admin.site.register(Pet)
admin.site.register(PostReview)
admin.site.register(PetImage)
admin.site.register(AdoptionReview)
