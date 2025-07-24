from django.urls import path

from router.views.website import list_services, list_sessions, list_logs

urlpatterns = [
    path('services/', list_services, name='list_services'),
    path('services/<int:service_id>/sessions/', list_sessions, name='service_sessions'),
    path('services/<int:service_id>/sessions/<int:session_id>/logs/', list_logs, name='session_logs'),
]
