from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    else:
         print(request.POST)
         return HttpResponse("Login Successful")