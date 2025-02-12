from django.urls import path
from admin_dashboard import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
]