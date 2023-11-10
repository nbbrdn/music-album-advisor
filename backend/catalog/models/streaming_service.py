from django.db import models


class StreamingService(models.Model):
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)
    name = models.CharField("Service", max_length=250)

    def __str__(self):
        return self.name
