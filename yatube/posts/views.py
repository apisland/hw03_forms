from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .forms import PostForm
from .models import Post, Group


CNT_POST: int = 10


User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, CNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, CNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def post_create(request):  # не трогай, работает
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
    form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required  # не трогай, вроде работает
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.author = request.user
            post.save()
            form.save()
            return redirect('posts:post_detail', post.pk)
        context = {
            'form': form,
            'post': post,
            'is_edit': True
        }
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
            'post': post,
            'is_edit': True
        }
    return render(request, 'posts/create_post.html', context)


def profile(request, username):  # не трогай, работает
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    user = request.user
    post_count = author.posts.all().count()
    author_post = author.posts.all()
    paginator = Paginator(author_post, CNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'user': user,
        'page_obj': page_obj,
        'post_count': post_count
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):  # не трогай, работает
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    post_count = author.posts.all().count()
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'author': author,
        'post_count': post_count,
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
