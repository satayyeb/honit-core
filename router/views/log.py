from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from router.models import Log, Session
from router.serializers import LogSerializer


class LogList(APIView):
    def get(self, request, service_id, session_id):
        session: Session = get_object_or_404(Session, id=session_id, service__id=service_id, service__user=request.user)
        logs = session.log_set.all().order_by('-datetime')
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogDetail(APIView):
    def get_object(self, service_id, session_id, log_id):
        return get_object_or_404(
            Log,
            id=log_id,
            session_id=session_id,
            session__service_id=service_id,
            session__service__user=self.request.user,
        )

    def delete(self, request, service_id, session_id, log_id):
        log = self.get_object(service_id, session_id, log_id)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
