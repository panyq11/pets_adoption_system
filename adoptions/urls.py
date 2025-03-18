from django.urls import path
from adoptions import views

app_name = 'adoptions'

urlpatterns = [
    path('', views.available_pets, name='available_pets'),

    path('available/', views.available_pets, name='available_pets'),

    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),

    path('apply/<int:pet_id>/', views.apply_for_adoption, name='apply_for_adoption'),

    path('applications/', views.my_application, name='my_application'),

    path('history/', views.adoption_history, name='adoption_history'),

    path('details/<int:pet_id>', views.history_details, name='history_details'),
]