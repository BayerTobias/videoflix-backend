from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import LoginView, UserViewSet
from video.views import VideoView, VideoViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"videos", VideoViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("login/", LoginView.as_view(), name="login"),
    path("videos/", VideoView.as_view(), name="videos"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("django-rq/", include("django_rq.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
