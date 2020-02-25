from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from .forms import NewComment

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
    if req.method == 'POST':
        comment_form = NewComment(data=req.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = NewComment()
    else:
        comment_form = NewComment()
    context={
        'title': post,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(req, 'blog/detail.html',context)