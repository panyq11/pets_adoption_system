from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Pet, PetImage
from accounts.models import User
from .models import AdoptPetInfo, AdoptionReview
from .forms import AdoptPetInfoForm

# Create your views here.

#@login_required
def available_pets(request):

    pets = Pet.objects.filter(postpetinfo__status='Approved').distinct()

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
    username = request.session.get('username', request.user.username)
    user = get_object_or_404(User, username=username)
    pet = get_object_or_404(Pet, pet_id=pet_id)

    if request.method == "POST":
        current_application = AdoptionReview.objects.filter(adopter_username__username=username, status='Pending').first()

        if current_application is None:
            form = AdoptPetInfoForm(request.POST)
            if form.is_valid():
                adopt_info = form.save(commit=False)

                adopt_info.pet = pet
                adopt_info.user = request.user
                # 这里暂时用当前用户作为操作员
                adopt_info.operator = request.user
                adopt_info.save()

                return redirect('adoptions:adoption_approval_status')
            else:
                messages.error(request, "请先完成当前的申请！")
                return redirect('adoptions:my_application')
    return redirect('adoptions:available_pets')





def my_application(request):
    username = request.user.username

    review = AdoptionReview.objects.filter(adopter_username__username=username, status='Pending').first()

    context = {
        'review': review,
    }

    return render(request, 'adoptions/my_application.html', context)



def adoption_history(request):
    username = request.user.username

    history_list = AdoptionReview.objects.filter(adopter_username__username=username)

    context = {
        'history_list': history_list,
    }
    return render(request, 'adoptions/adoption_history.html', context)
