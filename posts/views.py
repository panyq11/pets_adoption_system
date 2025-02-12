from django.shortcuts import render

# Create your views here.
def my_posts(request):
    return render(request,'posts/my_posts.html')