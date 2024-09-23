import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from content.tasks import convert_480p
from .models import Video
import django_rq

from django.contrib.auth import get_user_model
from django.conf import settings
from .views import send_activation_email

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
  print("Video saved")
  if created:
    print("Video created")
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(convert_480p, instance.video_file.path)
    # convert_480p(instance.video_file.path)
    
@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            
@receiver(post_save, sender=get_user_model())
def user_post_save(sender, instance, created, **kwargs):
    print("User saved")
    if created:
        print("User created")
        # Nur wenn ein neuer Benutzer erstellt wurde
        send_activation_email(instance)