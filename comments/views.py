from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from .forms import AddCommmentForm
from .models import Comment


@login_required
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        if (form := AddCommmentForm(request.POST)).is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post-detail', post_slug=post.slug)
    else:
        form = AddCommmentForm()
    return render(request, 'comments/add.html', {'form': form, 'post': post})


def comment_detail(request, post_slug, comment_id):
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    return render(request, 'comments/detail.html', {
        'comment': comment,
        'post': post,
        'is_author': comment.author == request.user,
    })


@login_required
def delete_comment(request, post_slug, comment_id):
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if comment.author != request.user:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('posts:post-detail', post_slug=post.slug)
