from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from router.llm import LLMApi
from router.models import Log, Session, Service
from router.serializers import LogSerializer

@method_decorator(csrf_exempt, name='dispatch')
class RouterApiView(APIView):
    serializer_class = LogSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, service_id, session_id):

        token = request.data.get('token')
        if not token:
            return Response(
                data={'response': 'EOF', 'error': 'Field token is required.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        service = get_object_or_404(Service, id=service_id, token=token)

        if not service.active:
            return Response(
                data={'response': 'EOF', 'error': 'Service is not active.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = request.data.get('request')
        if not message:
            return Response(
                data={'response': 'EOF', 'error': 'Field request is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if session_id > 0:
            session: Session = get_object_or_404(Session, id=session_id, service=service)
        else:
            session = Session.objects.create(service=service)

        log = LLMApi.chat(session, message)

        return Response({'response': log.response, 'session_id': session.id}, status=status.HTTP_200_OK)


class LogList(APIView):
    serializer_class = LogSerializer

    def get(self, request, service_id, session_id):
        session: Session = get_object_or_404(Session, id=session_id, service__id=service_id, service__user=request.user)
        serializer = LogSerializer(session.logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogDetail(APIView):
    serializer_class = LogSerializer

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
