from datetime import date
from django.conf import settings
from django.db import models


# Create your models here.
class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to="videos/", blank=True, null=True)

    def __str__(self):
        # return self.title
        return f"{self.title} ({self.created_at}) - {self.description}"

    @property
    def hls_url(self):
        base_url = settings.MEDIA_URL + self.video_file.name.replace(".mp4", "_hls/")
        return f"{base_url}index.m3u8"
