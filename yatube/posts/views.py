from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings


from .forms import PostForm
from .models import Post, Group, User


def numeration(queryset, request):
    paginator = Paginator(queryset, settings.CNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.all().select_related('author', 'group')
    context = {
        'page_obj': numeration(post_list, request)
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author', 'group')
    context = {
        'group': group,
        'page_obj': numeration(post_list, request),
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
    author = get_object_or_404(User, username=username)
    author_post = author.posts.select_related('author')
    context = {
        'author': author,
        'page_obj': numeration(author_post, request),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):  # не трогай, работает
    post = Post.objects.select_related('group').get(id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
