from django.urls import path
from . import views


app_name ='users'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.ProfileList.as_view(), name='profiles'),
    path('profile/<str:id>/', views.ProfileDetail.as_view(), name='profile_detail'),
    #path('profile/<str:id>/update/', views.ProfileDetail.as_view(), name='update_profile'),
    #path('profile/<str:id>/delete/', views.ProfileDetail.as_view(), name='delete_profile'),
    path('account/', views.ProfileAccount.as_view(), name='account'),
    path('account/edit/', views.UpdateProfile.as_view(), name='update_profile'),
    path('new-skill/', views.CreateSkill.as_view(), name='create_skill'),
    path('skill/<str:id>/update/', views.UpdateSkill.as_view(), name='update_skill'),
    path('skill/<str:id>/delete/', views.DeleteSkill.as_view(), name='delete_skill'),
    path('inbox/', views.Inbox.as_view(), name='inbox'),
    path('message/<str:id>/', views.MessageDetail.as_view(), name='message'),
    path('create-message/<str:id>/', views.CreateMessage.as_view(), name='create_message')
]