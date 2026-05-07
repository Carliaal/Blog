from django.db import models
from django.conf import settings

class Comment(models.Model):
    alias = models.CharField(max_length=128)
    content = models.TextField()
    post = models.ForeignKey(
        'posts.Post',              
        related_name='comments',   
        on_delete=models.CASCADE, 
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)