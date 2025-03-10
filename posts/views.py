from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Pet, PetImage, PostReview
from .forms import PetForm, PetImageForm



def post_pet(request):
    return render(request, 'posts/postPet.html')



def my_posts(request):
    return render(request, 'posts/myPosts.html')




def review_status(request):
    return render(request, 'posts/postReview.html')