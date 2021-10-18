from django.urls import path

from . import views


urlpatterns = [
    path('', views.Routes.as_view(), name='api_routes'),
]