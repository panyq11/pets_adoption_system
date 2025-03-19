from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from posts.models import PostPetInfo,Pet
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
from adoptions.models import AdoptionReview, AdoptPetInfo
from django.utils.timezone import now

def admin_dashboard(request):
    """ 管理员主界面，包含多个管理功能 """
    keyword = request.GET.get('keyword', '').strip()
    tab = request.GET.get('tab', '')  # 获取 tab 值，避免重复计算
    # 所有用户列表
    users_list = User.objects.all().order_by('-date_joined')

    # 所有宠物列表，并按照类型分类(cat/dog)
    pets_list_cats = Pet.objects.filter(
        type__iexact='Cat',
        postpetinfo__status='Approved'
    ).order_by('-created_at').distinct()
    pets_list_dogs = Pet.objects.filter(
        type__iexact='Dog',
        postpetinfo__status='Approved'
    ).order_by('-created_at').distinct()

    ## 获取所有待审核的宠物发布信息
    post_list = PostPetInfo.objects.select_related('pet','user').all().order_by('-created_at')

    adoption_reviews = AdoptionReview.objects.prefetch_related(
        'adopt_info'
    ).select_related(
        'pet', 'adopter_username', 'operator_username'
    ).order_by('-applied_at')


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
        'adoption_reviews': adoption_reviews,
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

    # ✅ **同步更新 Pet 的状态**
    pet = post_info.pet
    if new_status == "Approved":
        pet.status = "Available"  # **改成 Available**
    elif new_status == "Rejected":
        pet.status = "Not Available"  # **标记为不可用**
    elif new_status == "Pending":
        pet.status = "Pending"  # **保持 Pending**
    pet.save()

    if new_status != 'Pending':
        post_info.review_time = timezone.now()
    else:
        post_info.review_time = None
    post_info.save()

    messages.success(request, "Pet status updated successfully.")
    return redirect(reverse('admin_dashboard:admin_dashboard'))


@require_POST
def update_adoption_status(request, review_id):
    new_status = request.POST.get("status")
    # 注意这里使用 adopt_review_id 而非 id
    review = get_object_or_404(AdoptionReview, adopt_review_id=review_id)
    review.status = new_status  # ✅ 更新 AdoptionReview 的状态

    # ✅ 确保 `operator_username` **不会被错误覆盖**
    if not review.operator_username:
        admin_operator = User.objects.filter(user_type='Admin').order_by('?').first()
        if admin_operator:
            review.operator_username = admin_operator

    # ✅ **同步更新 Pet 的状态**
    pet = review.pet
    if new_status == "Approved":
        pet.status = "Adopted"  # **领养成功，设为 Adopted**
    elif new_status == "Rejected":
        pet.status = "Available"  # **拒绝后宠物仍然可以被申请**
    pet.save()

    if new_status in ["Pending", "Approved", "Rejected"]:
        review.status = new_status
        review.review_time = timezone.now()  # 明确保存当前时间

        review.operator_username = request.user  # 明确保存当前管理员
        review.save()
        messages.success(request, "Adoption review updated successfully.")
    else:
        messages.error(request, "Invalid status update.")
    return redirect(reverse('admin_dashboard:admin_dashboard'), context={"reviews": review})






