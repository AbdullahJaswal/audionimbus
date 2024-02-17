from django.urls import path

from .views import HealthCheck

app_name = "status"

urlpatterns = [path("", HealthCheck.as_view(), name="health-check")]
