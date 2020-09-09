from django.db import models

class ConfigItem(models.Model):
    FtpURL = models.URLField(max_length=250, default='https://qlink.to/TREK3')
    FileTypeList = models.CharField(max_length=250, default='*.GIF,*.JPG')
    FTPUser = models.CharField(max_length=250, default='ftpuser')
    FTPPassword = models.CharField(max_length=250, default='')
    SourceDir = models.CharField(max_length=250, default='/var/www/NymeBox/SDCARD/**')
    DestDir = models.CharField(max_length=20, default='/NymeBox')
    ProcMode = models.Manager()
