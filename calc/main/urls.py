from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    #path("test/", views.test, name="test"),
    #path("uploaded/", views.upload_file, name="upload"),
    #path("uploaded/<str:filename>/", views.upload_file, name="upload"),
    #path("loading/", views.loading, name="loading")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)