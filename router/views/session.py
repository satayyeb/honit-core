from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from router.models import Session, Service
from router.serializers import SessionSerializer


class SessionList(APIView):
    serializer_class = SessionSerializer

    def get(self, request: Request, service_id):
        sessions = Session.objects.filter(service__id=service_id, service__user=request.user)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request, service_id):
        service = get_object_or_404(Service, pk=service_id, user=request.user)
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(service=service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionDetail(APIView):
    serializer_class = SessionSerializer

    def get_object(self, service_id, session_id) -> Session:
        return get_object_or_404(Session, id=session_id, service__id=service_id, service__user=self.request.user)

    def get(self, request, service_id, session_id):
        session = self.get_object(service_id, session_id)
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    def disabled_put(self, request, service_id, session_id):
        session = self.get_object(service_id, session_id)
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id, session_id):
        session = self.get_object(service_id, session_id)
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
