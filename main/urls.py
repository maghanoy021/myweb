from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), 
    path("profile/edit/", views.edit_profile, name="edit_profile"),   
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path('announcements/', views.announcements, name='announcements'),
    path('events/', views.events, name='events'),
    path('files/', views.file_list, name='files'),
    path('messages/', views.messages_view, name='messages'),
]         