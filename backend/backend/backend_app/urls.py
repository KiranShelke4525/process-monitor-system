from django.urls import path
from . import views

urlpatterns = [
    path("agent/ingest/", views.ingest_agent_data, name="ingest"),
    path("agent/latest/", views.latest_systems, name="latest_systems"),
    path("agent/system/<int:system_id>/", views.system_detail, name="system_detail"),
    path("monitor/", views.monitor, name="monitor"),
]
