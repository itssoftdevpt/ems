import uuid

from django.db import models

from tenancy.models import AdministrativeUnit


class ReportSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.name
