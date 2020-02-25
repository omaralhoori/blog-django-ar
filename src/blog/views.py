from django.shortcuts import render, get_object_or_404
from .models import Post,Comment

# Create your views here.
def home(req):
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': Post.objects.all()
    }
    return render(req, 'blog/index.html', context)

def about(req):
    return render(req, 'blog/about.html',{'title':'من أنا'})

def post_detail(req, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(active=True)
    context={
        'title': post,
        'post': post,
        'comments': comments
    }
    return render(req, 'blog/detail.html',context)