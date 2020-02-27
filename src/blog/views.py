from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from .forms import NewComment, PostCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'blog/new_post.html'
    form_class = PostCreateForm
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)