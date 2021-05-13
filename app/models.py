from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from django.utils import timezone
from model_utils import Choices
from django.db import models
import jsonfield
import uuid


class ClaimFile(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    file = models.ImageField(upload_to='claims/')
    name = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"File: {self.name} | {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class Claim(models.Model):
    STATUS = Choices('preparing', 'submitted', 'accepted', 'rejected', 'updated')
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    files = models.ManyToManyField(ClaimFile)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS.preparing)
    details = models.TextField(default='', blank=True, null=True)
    telegram = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    estimations = jsonfield.JSONField(default={})
    vitex_address = models.CharField(max_length=56, default='', blank=True, null=True)
    team_comments = models.TextField(default='', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"CLAIM: {self.telegram} | {self.timestamp}"