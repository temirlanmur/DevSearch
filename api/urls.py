from django.urls import path

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.Routes.as_view(), name='api_routes'),
    path('projects', views.ProjectList.as_view(), name='project_list'),
    path('projects/<uuid:project_id>', views.ProjectRetrieve.as_view(), name='project_detail'),
]