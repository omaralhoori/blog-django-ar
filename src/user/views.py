from django.shortcuts import render, redirect
from .forms import UserCreationForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
# Create your views here.

def register(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(req, f'تهانينا {username} ,لقد تم التسجيل بنجاح ')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(req, 'user/register.html',{
        'title': 'التسجيل',
        'form': form,
    })

def login_user(req):
    if req.method == 'POST':
        form = LoginForm()
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username= username, password= password)
        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.warning(
                req, 'هناك خطأ في اسم المستخدم او كلمة المرور'
            )
    else:
        form = LoginForm()
    return render(req,'user/login.html',{
        'title': 'تسجيل الدخول',
        'form': form
    })

def logout_user(req):
    logout(req)
    return render(req, 'user/logout.html',{
        'title': 'تسجيل الخروج',
    })

def profile(req):
    posts = Post.objects.filter(author=req.user)
    return render(req, 'user/profile.html',{
        'title': 'الملف الشخصي',
        'posts': posts
    })