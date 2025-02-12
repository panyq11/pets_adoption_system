from django.shortcuts import render

# Create your views here.
def available_pets(request):
    return render(request, 'adoptions/available_pets.html')