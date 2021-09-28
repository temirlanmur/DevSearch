from django.urls import path
from . import views


app_name = 'projects'
urlpatterns = [
    path('', views.ProjectList.as_view(), name='projects'),
    path('new-project/', views.CreateProject.as_view(), name='create_project'),
    path('project/<str:id>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/<str:id>/update/', views.UpdateProject.as_view(), name='update_project'),
    path('project/<str:id>/delete/', views.DeleteProject.as_view(), name='delete_project'),
]