from django.urls import path

from router.views.app import AppList
from router.views.log import LogList, LogDetail
from router.views.service import ServiceList, ServiceDetail
from router.views.session import SessionList, SessionDetail

urlpatterns = [
    path('apps', AppList.as_view(), name='app-list'),
    path('services/', ServiceList.as_view(), name='service-list'),
    path('services/<int:service_id>', ServiceDetail.as_view(), name='service-detail'),
    path('services/<int:service_id>/sessions/', SessionList.as_view(), name='service-list'),
    path('services/<int:service_id>/sessions/<int:session_id>', SessionDetail.as_view(), name='service-detail'),

    path('services/<int:service_id>/sessions/<int:session_id>/logs', LogList.as_view(), name='log-list'),
    path('services/<int:service_id>/sessions/<int:session_id>/logs/<int:log_id>', LogDetail.as_view(),
         name='log-detail'),
]
