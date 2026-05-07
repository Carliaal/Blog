from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from .forms import AddCommmentForm
from .models import Comment

@login_required
def comments_list(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(post=post).order_by('id')
    return render(request, 'comments/list.html', {'comments': comments, 'post': post})


@login_required
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    parent_id = request.POST.get('parent_id') or request.GET.get('parent_id')
    parent = get_object_or_404(Comment, pk=parent_id, post=post) if parent_id else None
    if request.method == 'POST':
        if (form := AddCommmentForm(request.POST)).is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = parent
            comment.save()
            return redirect('posts:post-detail', post_slug=post.slug)
    else:
        form = AddCommmentForm()
    return render(request, 'comments/add.html', {'form': form, 'post': post, 'parent': parent})

@login_required
def comment_detail(request, post_slug, comment_id):
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    replies = comment.replies.order_by('created_at')
    return render(request, 'comments/detail.html', {
        'comment': comment,
        'post': post,
        'replies': replies,
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
