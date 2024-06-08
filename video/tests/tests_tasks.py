import os
from unittest.mock import patch
from django.test import TestCase
from video.tasks import create_thumbnail, convert720p, convert480p
from django.conf import settings


class TestVideoTasks(TestCase):
    @patch("video.tasks.subprocess.run")
    def test_create_thumbnail(self, mock_subprocess_run):
        source_path = "/path/to/video.mp4"
        file_name = os.path.splitext(os.path.basename(source_path))[0]
        expected_thumbnail_path = os.path.join(
            settings.MEDIA_ROOT, "thumbnails", f"{file_name}.jpg"
        )

        mock_subprocess_run.return_value = None

        thumbnail_path = create_thumbnail(source_path)

        self.assertEqual(thumbnail_path, expected_thumbnail_path)
        mock_subprocess_run.assert_called_once_with(
            'ffmpeg -i "{}" -ss 00:00:05 -vframes 1 -vf "scale=640:360" -update 1 "{}"'.format(
                source_path, expected_thumbnail_path
            ),
            shell=True,
        )

    @patch("video.tasks.subprocess.run")
    def test_convert720p(self, mock_subprocess_run):
        source_path = "/path/to/video.mp4"
        base, ext = os.path.splitext(source_path)
        expected_new_file_name = f"{base}_720p{ext}"

        mock_subprocess_run.return_value = None

        convert720p(source_path)

        mock_subprocess_run.assert_called_once_with(
            'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
                source_path, expected_new_file_name
            ),
            shell=True,
        )

    @patch("video.tasks.subprocess.run")
    def test_convert480p(self, mock_subprocess_run):
        source_path = "/path/to/video.mp4"
        base, ext = os.path.splitext(source_path)
        expected_new_file_name = f"{base}_480p{ext}"

        mock_subprocess_run.return_value = None

        convert480p(source_path)

        mock_subprocess_run.assert_called_once_with(
            'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
                source_path, expected_new_file_name
            ),
            shell=True,
        )
