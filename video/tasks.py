import subprocess
from django.conf import settings
import os


def create_thumbnail(source_path, time="00:00:05", width=640, height=360):
    file_name = os.path.splitext(os.path.basename(source_path))[0]
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, "thumbnails", f"{file_name}.jpg")
    cmd = 'ffmpeg -i "{}" -ss {} -vframes 1 -vf "scale={}:{}" -update 1 "{}"'.format(
        source_path, time, width, height, thumbnail_path
    )
    subprocess.run(cmd, shell=True)
    return thumbnail_path


def convert720p(source_path):
    new_file_name = convert_path(source_path, "720p")
    cmd = (
        'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert480p(source_path):
    new_file_name = convert_path(source_path, "480p")
    cmd = (
        'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert_path(source_path, resolution):
    dot_index = source_path.rfind(".")
    base_name = source_path[:dot_index]
    ext = source_path[dot_index:]
    return f"{base_name}_{resolution}{ext}"
