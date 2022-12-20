from django.db import models


class CoreSave(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    class Meta:
        abstract = True
