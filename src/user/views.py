from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib import messages
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
