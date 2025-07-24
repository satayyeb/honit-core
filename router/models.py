import secrets

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class AppType(models.TextChoices):
    SSH = 'SSH'
    K8S = 'K8S'


class App(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=AppType.choices)
    price = models.PositiveIntegerField()
    master_prompt = models.TextField()

    def __str__(self):
        return self.name

    def call(self, message: str, context: dict):
        ...


class Service(models.Model):
    name = models.CharField(max_length=255)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(64)
        super().save(*args, **kwargs)


class Session(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.service.name

    @property
    def logs(self):
        return self.log_set.all().order_by('datetime')

    @property
    def context(self):
        context = [{'role': 'system', 'content': self.service.app.master_prompt}]
        for log in self.logs:
            context.append({'role': 'user', 'content': log.request})
            context.append({'role': 'assistant', 'content': log.response})
        return context


class Log(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    request = models.TextField()
    response = models.TextField()
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
