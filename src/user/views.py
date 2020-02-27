from django.shortcuts import render, redirect
from .forms import UserCreationForm,LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    posts_count = len(posts)
    paginator = Paginator(posts, 1)
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    
    return render(req, 'user/profile.html',{
        'title': 'الملف الشخصي',
        'posts': posts,
        'page': page,
        'posts_count': posts_count
    })
    
@login_required(login_url='login')
def profile_update(req):
    if req.method == 'POST':
        user_form = UserUpdateForm(req.POST or None,instance=req.user)
        profile_form = ProfileUpdateForm(req.POST or None,req.FILES,instance=req.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            print('passed from here')
            user_form.save()
            profile_form.save()
            messages.success(
                req, 'تم تحديث الملف الشخصي بنجاح ')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=req.user)
        profile_form = ProfileUpdateForm(instance=req.user.profile)

    context = {
        'title': 'تعديل الملف الشخصي',
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(req, 'user/profile_update.html', context)