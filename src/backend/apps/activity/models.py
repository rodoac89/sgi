from django.db import models
from apps.core.models import Workstation

class Session(models.Model):
    pc = models.ForeignKey(
        Workstation, on_delete=models.SET_NULL, blank=False, null=True)
    start = models.BigIntegerField(blank=False, null=False)
    end = models.BigIntegerField(blank=True, null=True)
    alive = models.BigIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('pc', 'start')

    def __str__(self):
        return f'{self.pc} {self.start} -> {self.end}'
