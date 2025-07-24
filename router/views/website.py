import requests
from django.shortcuts import render
from requests.auth import HTTPBasicAuth

API_BASE = 'http://127.0.0.1:8000/api/v1'


def list_services(request):
    response = requests.get(f'{API_BASE}/services/', auth=HTTPBasicAuth('admin', 'admin'))
    services = response.json() if response.ok else []
    return render(request, 'services.html', {'services': services})


def list_sessions(request, service_id):
    response = requests.get(f'{API_BASE}/services/{service_id}/sessions/', auth=HTTPBasicAuth('admin', 'admin'))
    sessions = response.json() if response.ok else []
    return render(request, 'sessions.html', {'sessions': sessions, 'service_id': service_id})


def list_logs(request, service_id, session_id):
    response = requests.get(f'{API_BASE}/services/{service_id}/sessions/{session_id}/logs',
                            auth=HTTPBasicAuth('admin', 'admin'))
    logs = response.json() if response.ok else []
    return render(request, 'logs.html', {'logs': logs, 'session_id': session_id})
