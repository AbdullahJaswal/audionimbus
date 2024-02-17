from audioclip.views import AudioClipDetailView, AudioClipListView
from django.urls import path

app_name = "audioclip"

urlpatterns = [
    path("", AudioClipListView.as_view(), name="audioclip-list"),
    path("<slug:slug>/", AudioClipDetailView.as_view(), name="audioclip-detail"),
]
