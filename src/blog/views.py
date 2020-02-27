from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from .forms import NewComment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def home(req):
    posts = Post.objects.all()
    paginator = Paginator(posts, 1)
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': posts,
        'page': page
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