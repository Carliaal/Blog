from functools import wraps

from django.http import HttpResponseForbidden

from posts.models import Post


def author_required(view_func):
    @wraps(view_func)
    def wrapper(request, post_slug: str, **kwargs):
        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            return HttpResponseForbidden()
        if post.author is not None and post.author != request.user:
            return HttpResponseForbidden()
        return view_func(request, post=post, **kwargs)
    return wrapper
