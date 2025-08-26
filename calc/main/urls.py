from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test/", views.test, name="test"),
    path("uploaded/", views.upload_file, name="upload")
]