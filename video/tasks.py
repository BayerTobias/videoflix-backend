import subprocess
from django.conf import settings
import os


def create_thumbnail(source_path, time="00:00:05", width=640, height=360):
    """
    Creates a thumbnail for a given video file.

    This function generates a thumbnail image from the specified video file at a given time,
    with specified width and height.

    Args:
    - source_path (str): The path to the source video file.
    - time (str, optional): The timestamp in the video from which to capture the thumbnail. Defaults to "00:00:05".
    - width (int, optional): The width of the thumbnail image. Defaults to 640.
    - height (int, optional): The height of the thumbnail image. Defaults to 360.

    Returns:
    - str: The path to the generated thumbnail image.
    """

    file_name = os.path.splitext(os.path.basename(source_path))[0]
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, "thumbnails", f"{file_name}.jpg")
    cmd = 'ffmpeg -i "{}" -ss {} -vframes 1 -vf "scale={}:{}" -update 1 "{}"'.format(
        source_path, time, width, height, thumbnail_path
    )
    subprocess.run(cmd, shell=True)
    return thumbnail_path


def convert720p(source_path):
    """
    Converts a video file to 720p resolution.

    This function converts the given video file to 720p resolution using FFmpeg.

    Args:
    - source_path (str): The path to the source video file.
    """

    new_file_name = convert_path(source_path, "720p")
    cmd = (
        'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert480p(source_path):
    """
    Converts a video file to 480p resolution.

    This function converts the given video file to 480p resolution using FFmpeg.

    Args:
    - source_path (str): The path to the source video file.
    """

    new_file_name = convert_path(source_path, "480p")
    cmd = (
        'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert_path(source_path, resolution):
    """
    Generates a new file path with a resolution suffix.

    This function creates a new file path by appending the specified resolution to the base name of the source file.

    Args:
    - source_path (str): The path to the source file.
    - resolution (str): The resolution suffix to add to the new file name.

    Returns:
    - str: The new file path with the resolution suffix.
    """

    dot_index = source_path.rfind(".")
    base_name = source_path[:dot_index]
    ext = source_path[dot_index:]
    return f"{base_name}_{resolution}{ext}"
