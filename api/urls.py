from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.Routes.as_view(), name='api_routes'),
    path('projects', views.ProjectList.as_view(), name='project_list'),
    path('projects/<uuid:project_id>', views.ProjectRetrieve.as_view(), name='project_detail'),

    # Simple JWT plugin's routes
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]