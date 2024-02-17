from rest_framework import serializers

from .models import AudioClip


class AudioClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioClip
        exclude = ["id", "user"]
