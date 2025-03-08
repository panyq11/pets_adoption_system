from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Pet, PetImage, PostReview
from .forms import PetForm, PetImageForm
from django.contrib.auth.decorators import login_required


# Create your views here.
#def my_posts(request):
    #return render(request,'posts/my_posts.html')

@login_required
def post_pet(request):
    """
    处理用户提交的宠物信息
    """
    if request.method == "POST":
        pet_form = PetForm(request.POST)
        image_form = PetImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('pet_image')  # ✅ 从前端获取多张图片

        if pet_form.is_valid() and len(images) <= 6:  # 限制最多 6 张
            pet = pet_form.save(commit= False)
            pet.posted_by = request.user
            pet.save()

            for image in images:
                PetImage.objects.create(pet=pet, pet_image=image)  # ✅ 保存每张图片

            # 生成审核状态
            PostReview.objects.create(post=pet, user=request.user)

            # ✅ 根据用户选择的按钮跳转
            redirect_target = request.POST.get("redirect_target")
            if redirect_target == "review_status":
                return redirect('review_status')  # ✅ 用户跳转到审核状态页面
            else:
                return redirect('my_posts')  # ✅ 用户跳转到发布历史页面

    else:
        pet_form = PetForm()
        image_form = PetImageForm()

    return render(request, 'posts/post_pet.html', {'pet_form': pet_form, 'image_form': image_form})


@login_required
def my_posts(request):
    """
    显示所有发布的宠物
    """
    pets = Pet.objects.filter(posted_by=request.user)
    return render(request, 'posts/my_posts.html', {'pets': pets})


@login_required
def review_status(request):
    """
    显示用户的发布审核状态
    """
    reviews = PostReview.objects.filter(user=request.user)
    return render(request, 'posts/review_status.html', {'reviews': reviews})
