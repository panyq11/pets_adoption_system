from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Pet, PetImage, PostPetInfo
from accounts.models import User
from .models import AdoptPetInfo, AdoptionReview
from .forms import AdoptPetInfoForm
from django.contrib import messages


# Create your views here.

@login_required
def available_pets(request):

    pets = Pet.objects.filter(status='Available').distinct()

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
            pets = pets.filter(age='Young')
        elif age_category.lower() == 'adult':
            pets = pets.filter(age='Adult')

    if sex:
        pets = pets.filter(sex__iexact=sex)

    if size:
        pets = pets.filter(size__iexact=size)

    context = {'pets': pets}
    return render(request, 'adoptions/available_pets.html', context)


@login_required
def pet_detail(request, pet_id):
    username = request.user.username
    pet = get_object_or_404(Pet, pet_id=pet_id)
    pet_info = PostPetInfo.objects.filter(pet_id=pet_id).first()

    images = pet.images.all()

    processing = False
    current_application = AdoptionReview.objects.filter(adopter_username__username=username, status='Pending').first()
    if current_application is not None:
        processing = True
        """"
        messages.error(request,
                       "You already have a pending adoption application. Please wait until it is processed before submitting a new one.")
        return redirect('adoptions:my_application')
        """

    context = {
        'pet': pet,
        'images': images,
        'pet_info': pet_info,
        'processing': processing,
    }
    return render(request, 'adoptions/pet_detail.html', context)


@login_required
def apply_for_adoption(request, pet_id):
    username = request.user.username
    user = User.objects.get(username=username)
    pet = get_object_or_404(Pet, pet_id=pet_id)

    current_application = AdoptionReview.objects.filter(adopter_username__username=username, status='Pending').first()

    if request.method == "POST":
        if current_application is not None:
            messages.error(request,
                           "You already have a pending adoption application. Please wait until it is processed before submitting a new one.")
            return redirect('adoptions:my_application')

        form = AdoptPetInfoForm(request.POST)
        if form.is_valid():
            adopt_info = form.save(commit=False)

            adopt_info.pet = pet

            adopt_info.user = request.user

            random_operator = User.objects.filter(user_type='Admin').order_by('?').first()
            if not random_operator:
                raise Exception("No Operator found.")
            adopt_info.operator = random_operator

            adopt_info.save()

            review = AdoptionReview(
                pet=pet,
                adopt_info = adopt_info,
                adopter_username=request.user,
                operator_username=random_operator,
                status='Pending'
            )
            review.save()

            return redirect('adoptions:my_application')

    if request.method == "GET":
        form = AdoptPetInfoForm()
        return render(request, 'adoptions/apply_for_adoption.html', {'form': form, 'pet': pet, 'user':user})
    return redirect('adoptions:available_pets')


@login_required
def my_application(request):
    username = request.user.username

    review = AdoptionReview.objects.filter(adopter_username=request.user, status='Pending').first()

    if review is None:
        messages.error(request, "You do not have any adoption applications.")
        return redirect('adoptions:available_pets')

    pet_id = review.pet_id
    pet_info = PostPetInfo.objects.get(pet_id=pet_id)

    application = AdoptPetInfo.objects.filter(pet=review.pet).first()

    context = {
        'application': application,
        'review': review,
        'pet_info': pet_info,
    }

    return render(request, 'adoptions/my_application.html', context)


@login_required
def adoption_history(request):
    username = request.user.username

    history_list = AdoptionReview.objects.filter(adopter_username__username=username)

    context = {
        'history_list': history_list,
    }
    return render(request, 'adoptions/adoption_history.html', context)

def history_details(request, pet_id):
    from django.db.models import Max

    application = AdoptPetInfo.objects.filter(pet__pet_id=pet_id) \
        .annotate(latest_review_time=Max('reviews__review_time')) \
        .order_by('-latest_review_time').first()

    review = AdoptionReview.objects.filter(pet__pet_id=pet_id).order_by('-applied_at').first()

    pet_info = PostPetInfo.objects.filter(pet_id=pet_id).filter(pet__pet_id=pet_id).first()

    context = {
        'application': application,
        'review': review,
        'pet_info':pet_info,
    }

    return render(request, 'adoptions/history_details.html', context)
