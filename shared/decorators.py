from functools import wraps

from django.shortcuts import get_object_or_404
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

def object_required(model, pk_kwarg=None, slug_kwarg=None, slug_field='slug', author_check=False, kwarg_name=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            lookup = {}
            if pk_kwarg and pk_kwarg in kwargs:
                lookup['pk'] = kwargs.pop(pk_kwarg)
            if slug_kwarg and slug_kwarg in kwargs:
                lookup[slug_field] = kwargs.pop(slug_kwarg)  
            if 'post' in kwargs:
                lookup['post'] = kwargs['post']

            obj = get_object_or_404(model, **lookup)

            if author_check and obj.author != request.user:
                return HttpResponseForbidden()

            name = kwarg_name or model.__name__.lower()
            kwargs[name] = obj
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator