import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django_extensions.db.fields import AutoSlugField


def user_directory_path(instance, filename):
    return f"audios/user_{instance.user.id}/{instance.uid}.mp3"


# Create your models here.
class AudioClip(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="audioclips",
    )

    uid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    slug = AutoSlugField(
        populate_from=["title"],
        unique=True,
        allow_duplicates=False,
        max_length=512,
    )

    description = models.TextField(default="", null=False, blank=True)

    audio = models.FileField(upload_to=user_directory_path, null=False, blank=False)

    transcription = models.TextField(default="", null=False, blank=True)
    is_transcribed = models.BooleanField(default=False, null=False, blank=False)
    transcribed_at = models.DateTimeField(null=True, blank=True)

    ai_prompts = models.JSONField(default=list, null=False, blank=False)
    is_processed = models.BooleanField(default=False, null=False, blank=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AudioClip"
        verbose_name_plural = "AudioClips"

        unique_together = (("user", "title"),)

        ordering = ("-created_at", "title")

    def __str__(self):
        return f"{self.user} - {self.title}"

    def save(self, *args, **kwargs):
        if self.transcription:
            prev_state_transcription = ""
            prev_state = AudioClip.objects.filter(pk=self.pk)

            if prev_state:
                prev_state_transcription = prev_state.first().transcription

            if self.transcription != prev_state_transcription:
                self.transcribed_at = datetime.now()

        return super().save(*args, **kwargs)
