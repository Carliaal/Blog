from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('add/', views.add_post, name="post-add"),
    path('<slug:post_slug>/', views.post_detail, name='post-detail'),
    path('<slug:post_slug>/edit', views.edit_post, name='post-edit')
]
