from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<slug:post_slug>/comments/', views.comments_list, name='comments-list'),
    path('<slug:post_slug>/comments/add/', views.add_comment, name='add-comment'),
    path('<slug:post_slug>/comments/<int:comment_id>/', views.comment_detail, name='detail'),
    path('<slug:post_slug>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
]
