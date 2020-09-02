from django.db import models

class ConfigItem(models.Model):
    field = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
