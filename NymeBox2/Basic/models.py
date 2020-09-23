from django.db import models

class ConfigItem(models.Model):
    Manager = models.Manager()
    FtpURL = models.CharField(max_length=250, default='TREK')
    FileTypeList = models.CharField(max_length=250, default='*.GIF,*.JPG')
    FTPUser = models.CharField(max_length=250, default='ftpuser')
    FTPPassword = models.CharField(max_length=250, default='')
    SourceDir = models.CharField(max_length=250, default='/var/www/NymeBox/SDCARD/**')
    DestDir = models.CharField(max_length=20, default='/NymeBox')
    ProcMode = models.CharField(max_length=30, db_index=True, default='TEST', primary_key=True)
    LastLog = models.TextField(default='')
    MovedFiles = models.TextField(default='')