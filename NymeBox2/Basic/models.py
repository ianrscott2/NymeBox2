from django.db import models

class ConfigItem(models.Model):
    FTP_URL = models.CharField(max_length=250)
    FileType_List = models.CharField(max_length=250, default='')
