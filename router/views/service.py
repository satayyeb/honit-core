from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from router.models import Service
from router.serializers import ServiceSerializer


class ServiceList(APIView):
    serializer_class = ServiceSerializer

    def get(self, request: Request):
        services = Service.objects.filter(user=request.user)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetail(APIView):
    serializer_class = ServiceSerializer

    def get_object(self, service_id):
        return get_object_or_404(Service, id=service_id, user=self.request.user)

    def get(self, request, service_id):
        service = self.get_object(service_id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def disabled_put(self, request, service_id):
        service = self.get_object(service_id)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id):
        service = self.get_object(service_id)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
