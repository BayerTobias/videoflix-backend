from .test_setup import TestSetup
from django.core.files.uploadedfile import SimpleUploadedFile
from video.models import Video
import uuid
import os
from django.conf import settings


class TestVideoView(TestSetup):

    def test_video_upload(self):

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        video_content = b"Fake video content"
        thumbnail_content = b"Fake thumbnail content"
        video_file = SimpleUploadedFile(
            "test_video.mp4", video_content, content_type="video/mp4"
        )
        thumbnail_file = SimpleUploadedFile(
            "test_thumbnail.jpg", thumbnail_content, content_type="image/jpeg"
        )
        data = {
            "title": "Test Video",
            "description": "Test description",
            "video_file": video_file,
            "thumbnail_file": thumbnail_file,
            "visibility": "public",
            "genre": "fitness",
        }
        response = self.client.post(self.videos_url, data, format="multipart")
        self.assertEqual(response.status_code, 201)
        video = Video.objects.get(title="Test Video")
        self.assertEqual(video.description, "Test description")
        self.assertEqual(video.visibility, "public")
        self.assertEqual(video.genre, "fitness")
        self.assertTrue(video.video_file)
        self.assertTrue(video.thumbnail_file)
        self.assertEqual(video.user, self.user)
        video.video_file.delete()
        video.thumbnail_file.delete()

    def test_get_public_videos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")

        video_content = b"Fake video content"
        thumbnail_content = b"Fake thumbnail content"
        test_token = str(uuid.uuid4())
        video_file = SimpleUploadedFile(
            f"test_video{test_token}.mp4", video_content, content_type="video/mp4"
        )
        thumbnail_file = SimpleUploadedFile(
            f"test_thumbnail{test_token}.jpg",
            thumbnail_content,
            content_type="image/jpeg",
        )

        Video.objects.create(
            title="Public Video 1",
            description="Test description",
            visibility="public",
            genre="fitness",
            user=self.user,
            video_file=video_file,
            thumbnail_file=thumbnail_file,
        )

        Video.objects.create(
            title="Public Video 2",
            description="Test description",
            visibility="public",
            genre="animals",
            user=self.user,
            video_file=video_file,
            thumbnail_file=thumbnail_file,
        )

        Video.objects.create(
            title="Private Video 1",
            description="Test description",
            visibility="private",
            genre="landscapes",
            user=self.user,
            video_file=video_file,
            thumbnail_file=thumbnail_file,
        )

        response = self.client.get(f"{self.videos_url}?visibility=public")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        print(response_data)

        self.assertEqual(len(response_data), 2)
        for video in response_data:
            self.assertEqual(video["visibility"], "public")

        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if test_token in file:
                    os.remove(os.path.join(root, file))

    def test_get_private_videos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        video_content = b"Fake video content"
        thumbnail_content = b"Fake thumbnail content"
        test_token = str(uuid.uuid4())
        video_file = SimpleUploadedFile(
            f"test_video{test_token}.mp4", video_content, content_type="video/mp4"
        )
        thumbnail_file = SimpleUploadedFile(
            f"test_thumbnail{test_token}.jpg",
            thumbnail_content,
            content_type="image/jpeg",
        )

        Video.objects.create(
            title="Public Video 1",
            description="Test description",
            visibility="public",
            genre="fitness",
            user=self.user,
            video_file=video_file,
            thumbnail_file=thumbnail_file,
        )

        Video.objects.create(
            title="Public Video 2",
            description="Test description",
            visibility="public",
            genre="animals",
            user=self.user,
            video_file=video_file,
            thumbnail_file=thumbnail_file,
        )

        Video.objects.create(
            title="Private Video 1",
            description="Test description",
            visibility="private",
            genre="landscapes",
            user=self.user,
            video_file=video_file,
            thumbnail_file=thumbnail_file,
        )

        response = self.client.get(f"{self.videos_url}?visibility=private")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        print(response_data)

        self.assertEqual(len(response_data), 1)
        for video in response_data:
            self.assertEqual(video["visibility"], "private")

        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if test_token in file:
                    os.remove(os.path.join(root, file))
