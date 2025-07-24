from django.contrib import admin
from django.contrib.admin import register

from router.models import App, Service, Session, Log


# Register your models here.
@register(App)
class AppAdmin(admin.ModelAdmin):
    pass


@register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'app', 'active']


@register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['service', 'datetime']


@register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['session', 'datetime']
