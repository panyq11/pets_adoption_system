from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from posts.models import PostPetInfo,Pet
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q

def admin_dashboard(request):
    """ 管理员主界面，包含多个管理功能 """
    keyword = request.GET.get('keyword', '').strip()
    tab = request.GET.get('tab', '')  # 获取 tab 值，避免重复计算
    # 所有用户列表
    users_list = User.objects.all().order_by('-date_joined')

    # 所有宠物列表，并按照类型分类(cat/dog)
    pets_list_cats = Pet.objects.filter(type__iexact='Cat').order_by('-created_at')
    pets_list_dogs = Pet.objects.filter(type__iexact='Dog').order_by('-created_at')

    ## 获取所有待审核的宠物发布信息
    post_list = PostPetInfo.objects.select_related('pet','user').all().order_by('-created_at')

    has_results = False  # 标记是否有搜索结果

    if keyword:
        users_list = User.objects.filter(
            Q(username__icontains=keyword) |
            Q(email__icontains=keyword) |
            Q(phone_no__icontains=keyword)
        )

        pets_list_cats = pets_list_cats.filter(
            Q(name__icontains=keyword) | Q(breed__icontains=keyword)
        )

        pets_list_dogs = pets_list_dogs.filter(
            Q(name__icontains=keyword) | Q(breed__icontains=keyword)
        )

        # **只设置 tab，避免无限重定向**
        if users_list.exists():
            tab = "users"
            has_results = True
        elif pets_list_cats.exists() or pets_list_dogs.exists():
            tab = "pets"
            has_results = True
        else:
            messages.warning(request, "No matching results found!")

    context = {
        "users_list": users_list,
        "pets_list_cats": pets_list_cats,
        "pets_list_dogs": pets_list_dogs,
        "post_list": post_list,  # 传递 Post Review 数据
        "tab": tab,  # 传递给前端，避免 JS 误判
    }
    return render(request, 'admin_dashboard/admin_dashboard.html', context)



@require_POST
def update_post_status(request, post_id):
    """ 管理员更新宠物发布的审批状态 """

    new_status = request.POST.get('status')
    if new_status not in ['Approved', 'Rejected', 'Pending']:
        messages.error(request, "Invalid status selected.")
        return redirect(reverse('admin_dashboard:admin_dashboard'))

    post_info = get_object_or_404(PostPetInfo, post_info_id=post_id)
    post_info.status = new_status

    if new_status != 'Pending':
        post_info.review_time = timezone.now()
    else:
        post_info.review_time = None
    post_info.save()

    messages.success(request, "Pet status updated successfully.")
    return redirect(reverse('admin_dashboard:admin_dashboard'))
