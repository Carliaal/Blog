from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.text import slugify

from comments.models import Comment
from .models import Post
from .forms import AddPostForm, EditPostForm
from shared.decorators import author_required


@login_required
def post_list(request):
    posts = Post.objects.order_by('-created_at', '-id')
    return render(request, 'posts/post/list.html', {'posts': posts})


@login_required
def post_detail(request, post_slug: str):
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return HttpResponse(f'Post with slug "{post_slug}" does not exist!')
    comments = Comment.objects.filter(post=post).order_by('id')
    return render(request, 'posts/post/detail.html', {
        'post': post,
        'is_author': post.author == request.user,
        'comments': comments,
    })


@login_required
def add_post(request):
    if request.method == 'POST':
        if (form := AddPostForm(request.POST)).is_valid():
            post = form.save(commit=False)
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            post.slug = slug
            post.author = request.user
            post.save()
            return redirect('posts:post-list')
    else:
        form = AddPostForm()
    return render(request, 'posts/post/add.html', {'form': form})


@login_required
@author_required
def edit_post(request, post: Post):
    if request.method == 'POST':
        if (form := EditPostForm(request.POST, instance=post)).is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts:post-list')
    else:
        form = EditPostForm(instance=post)
    return render(request, 'posts/post/edit.html', {'post': post, 'form': form})


@login_required
@author_required
def delete_post(request, post: Post):
    post.delete()
    return redirect('posts:post-list')
