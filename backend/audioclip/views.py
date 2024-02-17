from rest_framework import filters, generics, permissions

from .models import AudioClip
from .paginations import DefaultPagination
from .serializers import AudioClipSerializer


# Create your views here.
class AudioClipListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AudioClipSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        return AudioClip.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AudioClipDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AudioClipSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return AudioClip.objects.filter(user=self.request.user)
