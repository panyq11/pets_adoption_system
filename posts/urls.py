from django.urls import path
from posts import views


urlpatterns = [
    path('post_pet', views.post_pet, name='post_pet'),  # 宠物发布问卷界面 `/post/`
    path('my_posts/', views.my_posts, name='my_posts'),  # 发布历史 `/my_posts/`
    path('review_status/', views.review_status, name='review_status'),  # 发布审核 `/review_status/`
]