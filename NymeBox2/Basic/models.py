from django.db import models

class ConfigItem(models.Model):
    FTP_URL = models.CharField(max_length=250)
    JPG  = models.BooleanField(default=False)
    GIF  = models.BooleanField(default=False)
    NEF  = models.BooleanField(default=False)
