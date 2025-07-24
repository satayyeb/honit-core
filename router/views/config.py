import yaml
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.views import APIView

from core.settings import HONIT_BASE_URL
from router.models import Service


class ConfigApiView(APIView):
    def get(self, request: Request):
        services = Service.objects.filter(user=request.user)
        config = {
            'base_url': HONIT_BASE_URL,
            'services': [
                {
                    'name': service.name,
                    'type': service.app.type,
                    'id': service.id,
                    'token': service.token,
                    'port': service.port,
                } for service in services
            ]
        }

        yaml_data = yaml.dump(config, allow_unicode=True)

        return HttpResponse(
            yaml_data,
            content_type='application/x-yaml',
            headers={'Content-Disposition': 'attachment; filename="config.yaml"'},
        )