from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.my_posts, name='my_posts'),
]