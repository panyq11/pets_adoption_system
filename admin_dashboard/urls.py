from django.urls import path
from admin_dashboard import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('update_post_status/<int:post_id>/', views.update_post_status, name='update_post_status'),  # 更新审核状态
    path('update-adoption/<int:review_id>/', views.update_adoption_status, name='update_adoption_status'),
]
