from django.shortcuts import render, redirect
from .forms import UserCreationForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(req, f'تهانينا {new_user} ,لقد تم التسجيل بنجاح ')
            return redirect('login')
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

@login_required(login_url='login')
def profile(req):
    posts = Post.objects.filter(author=req.user)
    return render(req, 'user/profile.html',{
        'title': 'الملف الشخصي',
        'posts': posts
    })