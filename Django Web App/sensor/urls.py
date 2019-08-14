from django.urls import path
from .views import (
    DeviceListView,
    DeviceDeleteView,
    DeviceDetailView,

)
from . import views


urlpatterns = [
    path('', DeviceListView.as_view(), name="sensor-home"),
    path('device/generate/', views.generate, name="sensor-generate"),
    path('device/<int:pk>/delete/', DeviceDeleteView.as_view(), name="device-delete"),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name="device-detail"),



]
