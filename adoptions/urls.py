from django.urls import path
from adoptions import views

app_name = 'adoptions'

urlpatterns = [
    path('', views.available_pets, name='available_pets'),
]