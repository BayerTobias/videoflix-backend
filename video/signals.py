from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Video
from .tasks import convert720p, convert480p, convert_path, create_thumbnail
import os
from django_rq import enqueue
import django_rq

from django.core.cache import cache


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        if not instance.thumbnail_file.name:
            thumbnail_path = create_thumbnail(instance.video_file.path)
            instance.thumbnail_file.name = thumbnail_path[
                len(settings.MEDIA_ROOT) + 1 :
            ]
            instance.save()
        queue = django_rq.get_queue("default", autocommit=True)
        queue.enqueue(convert720p, instance.video_file.path)
        queue.enqueue(convert480p, instance.video_file.path)

        cache.clear()


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        path_720p = convert_path(instance.video_file.path, "720p")
        path_480p = convert_path(instance.video_file.path, "480p")

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            os.remove(instance.thumbnail_file.path)
            os.remove(path_720p)
            os.remove(path_480p)

            cache.clear()
