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

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("created_at")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class VideoView(APIView):
    permission_classes = [IsAuthenticated]
    """
    VideoView class for handling video-related requests.

    This view supports GET and POST methods for retrieving and creating videos respectively.
    The view requires the user to be authenticated.

    Methods:
    - get: Retrieves videos based on visibility (public or private).
    - post: Creates a new video entry for the authenticated user.
    """

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        """
        GET method for retrieving videos based on visibility.

        This method filters videos based on the 'visibility' query parameter.
        - If 'visibility' is 'public', it retrieves all public videos.
        - If 'visibility' is 'private', it retrieves private videos for the authenticated user.
        - If 'visibility' is invalid, it returns a 400 Bad Request error.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: A JSON response containing the serialized video data or an error message.
        """

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
        """
        POST method for creating a new video.

        This method allows the authenticated user to create a new video.
        It validates the input data using the VideoSerializer.

        Args:
        - request: The HTTP request object containing the video data.

        Returns:
        - Response: A JSON response containing the serialized video data if successful.
                    Otherwise, it returns a 400 Bad Request error with the validation errors.
        """

        serializer = VideoSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
