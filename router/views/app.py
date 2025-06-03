from rest_framework.generics import ListAPIView

from router.models import App
from router.serializers import AppSerializer


class AppList(ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
