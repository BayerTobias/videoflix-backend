from django.conf import settings
from rest_framework import status, viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.core.cache import cache

# CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("created_at")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class ClearCacheView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cache.set("a", "Value asdasdasdas")
        cache.set("b", "Value asdasdasdas")
        cache.set("c", "Value asdasdasdas")

        # cache.clear()

        keys = cache.keys("*")
        views = cache.keys("*views.decorators*")
        print("all keys:", keys)
        print("view keys", views)
        cache.delete_many(views)

        keys = cache.keys("*")
        print("all keys:", keys)

        # if value is None:
        #     print("Cache wurde erfolgreich gelöscht.")
        #     return Response(status=status.HTTP_200_OK)
        # else:
        #     print("Cache löschen hat nicht funktioniert. Der Wert ist noch:", value)
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class VideoView(APIView):
    # permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        visibility = request.query_params.get("visibility")

        if visibility == "public":
            videos = Video.objects.filter(visibility="public")
        elif visibility == "private":
            videos = Video.objects.filter(user=request.user, visibility="private")
        else:
            return Response(
                {"error": "Invalid visibility parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = VideoSerializer(videos, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VideoSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
