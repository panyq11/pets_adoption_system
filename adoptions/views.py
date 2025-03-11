from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Pet, PetImage
from accounts.models import User
from .models import Pet, AdoptPetInfo
from .forms import AdoptPetInfoForm

# Create your views here.

#@login_required
def available_pets(request):
    username = request.session.get('username', request.user.username)
    user = get_object_or_404(User, username=username)

    pets = Pet.objects.all()

    search_query = request.GET.get('q', '').strip()
    pet_type = request.GET.get('pet_type', '').strip()
    age_category = request.GET.get('age', '').strip()
    sex = request.GET.get('sex', '').strip()
    size = request.GET.get('size', '').strip()

    if search_query:
        pets = pets.filter(breed__icontains=search_query)

    if pet_type:
        pets = pets.filter(type__iexact=pet_type)

    if age_category:
        if age_category.lower() == 'young':
            pets = pets.filter(age__lte=2)
        elif age_category.lower() == 'adult':
            pets = pets.filter(age__gt=2)

    if sex:
        pets = pets.filter(sex__iexact=sex)

    if size:
        pets = pets.filter(size__iexact=size)

    context = {'pets': pets}
    return render(request, 'adoptions/available_pets.html', context)


def pet_detail(request, pet_id):

    pet = get_object_or_404(Pet, pet_id=pet_id)

    # 获取该宠物的所有关联图片
    images = pet.images.all()
    context = {
        'pet': pet,
        'images': images,
    }
    return render(request, 'adoptions/pet_detail.html', context)


def apply_for_adoption(request, pet_id):

    pet = get_object_or_404(Pet, pet_id=pet_id)

    if request.method == "POST":
        form = AdoptPetInfoForm(request.POST)
        if form.is_valid():
            adopt_info = form.save(commit=False)
            # 设置外键字段
            adopt_info.pet = pet
            adopt_info.user = request.user
            # 这里暂时用当前用户作为操作员
            adopt_info.operator = request.user
            adopt_info.save()
            # 表单提交成功后跳转到用户的申请列表或其他页面
            return redirect('adoptions:my_application')
    else:
        form = AdoptPetInfoForm()

    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'adoptions/apply_for_adoption.html', context)


def my_application(request):
    # 申请记录数据
    applications = [
        {
            'adopt_info_id': 1,
            'pet': {'name': 'Cindy'},
            'created_at': '2025-03-01 10:30',
            'status': 'Submitted',
        },
        {
            'adopt_info_id': 2,
            'pet': {'name': 'DianDian'},
            'created_at': '2025-03-05 14:15',
            'status': 'Processing',
        },
    ]
    context = {'my_applications': applications}
    return render(request, 'adoptions/my_application.html', context)


def adoption_approval_status(request, adopt_info_id):
    # 审批状态数据
    adopt_info = {
        'adopt_info_id': adopt_info_id,
        'pet': {'name': 'Cindy'},
        'created_at': '2025-03-05 14:15',
        'status': 'Processing',
        'timeline': [
            {'time': '2025-03-05 14:15', 'status': 'Submitted'},
            {'time': '2025-03-06 09:00', 'status': 'Processing'},
        ],
    }
    context = {'adopt_info': adopt_info}
    return render(request, 'adoptions/adoption_approval_status.html', context)


def adoption_history(request):
    # 领养历史数据
    history = [
        {
            'adopt_info_id': 1,
            'pet': {'name': 'Cindy'},
            'created_at': '2025-03-07 15:20',
            'status': 'Approved',
        },
        {
            'adopt_info_id': 2,
            'pet': {'name': 'Luna'},
            'created_at': '2025-02-15 11:00',
            'status': 'Approved',
        },
    ]
    context = {'adoption_history': history}
    return render(request, 'adoptions/adoption_history.html', context)
