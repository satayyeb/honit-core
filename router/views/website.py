from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from router.models import Service, Session, App
from router.serializers import ServiceSerializer


@login_required
def list_services(request):
    services = Service.objects.filter(user=request.user)
    return render(request, 'services.html', {'services': services})


@login_required
def create_service(request):
    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return redirect('list_services')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        apps = App.objects.all()
        return render(request, 'create_service.html', {'apps': apps})


@login_required
def list_sessions(request, service_id):
    sessions = Session.objects.filter(service_id=service_id, service__user=request.user)
    return render(request, 'sessions.html', {'sessions': sessions})


@login_required
def list_logs(request, service_id, session_id):
    session = Session.objects.get(id=session_id, service_id=service_id, service__user=request.user)
    return render(request, 'logs.html', {'logs': session.logs, 'service_id': service_id, 'session_id': session_id})


def landing(request):
    return render(request, 'landing.html')


class BasicLoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return render(request, 'login.html')  # Your login form template

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('list_services')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
