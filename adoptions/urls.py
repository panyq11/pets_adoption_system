from django.urls import path
from adoptions import views

app_name = 'adoptions'

urlpatterns = [
    path('', views.available_pets, name='available_pets'),

    # 显示可领养的宠物列表
    path('available/', views.available_pets, name='available_pets'),

    # 展示宠物详情页面，传入宠物 id
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),

    # 申请领养宠物，传入宠物 id（用于初始化表单）
    path('apply/<int:pet_id>/', views.apply_for_adoption, name='apply_for_adoption'),

    # 用户查看所有申请记录
    path('applications/', views.my_application, name='my_application'),

    # 查看单个申请的审批状态，传入申请 id
    path('approval/<int:adopt_info_id>/', views.adoption_approval_status, name='adoption_approval_status'),

    # 查看领养历史记录
    path('history/', views.adoption_history, name='adoption_history'),
]