import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth

API_BASE = 'http://127.0.0.1:8000/api/v1'


def list_services(request):
    response = requests.get(f'{API_BASE}/services/', auth=HTTPBasicAuth('admin', 'admin'))
    services = response.json() if response.ok else []
    return render(request, 'services.html', {'services': services})


@csrf_exempt
def create_service(request):
    if request.method == 'POST':
        name = request.POST['name']
        port = request.POST['port']
        app_id = request.POST['app']  # needs a dropdown in the form
        data = {'name': name, 'app': app_id, 'port': port}
        auth = HTTPBasicAuth('admin', 'admin')
        requests.post(f'{API_BASE}/services/', json=data, auth=auth)
        return redirect('list_services')
    else:
        # fetch app list for dropdown if needed
        apps = requests.get(f'{API_BASE}/apps', auth=HTTPBasicAuth('admin', 'admin')).json()
        return render(request, 'create_service.html', {'apps': apps})


def list_sessions(request, service_id):
    response = requests.get(f'{API_BASE}/services/{service_id}/sessions/', auth=HTTPBasicAuth('admin', 'admin'))
    sessions = response.json() if response.ok else []
    return render(request, 'sessions.html', {'sessions': sessions})


def list_logs(request, service_id, session_id):
    response = requests.get(f'{API_BASE}/services/{service_id}/sessions/{session_id}/logs',
                            auth=HTTPBasicAuth('admin', 'admin'))
    logs = response.json() if response.ok else []
    return render(request, 'logs.html', {'logs': logs, 'session_id': session_id})
