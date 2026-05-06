from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.edit_profile, name='profile-edit'),
    path('<str:username>/', views.profile_detail, name='profile-detail'),
]
