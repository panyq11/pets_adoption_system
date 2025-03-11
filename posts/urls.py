from django.urls import path
from posts import views

app_name = 'posts'
urlpatterns = [
    path('', views.post_pet, name='postPet'),  # 宠物发布问卷界面
    path('my_posts/', views.my_posts, name='myPost'),  # 发布历史
    path('review_status/', views.review_status, name='postReview'),  # 发布审核
]