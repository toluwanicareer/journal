from django.urls import path, include
from . import views


urlpatterns = [
    path('convert', views.ConvertView.as_view() ),
    ]