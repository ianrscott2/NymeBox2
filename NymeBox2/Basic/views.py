from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from Basic.models import ConfigItem
from .nymebox import NymeBox_Core
import socket
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import os
import os.path
from os import path

if 'nymebox' in socket.gethostname():
        app_mode = "PROD"
else:
        app_mode = "TEST"

configQuery = "SELECT * FROM basic_configitem WHERE ProcMode = %s"

def index(request):
        return HttpResponse("Hello World!")

def nymebox_home(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        #getftp = NymeBox_Core(config[0])
        return render(request, 'nymebox_home.html', {'config':config[0], 'ftpbutton':'default', 'resetbutton':'none'})

def ftpCheck(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        getftp = NymeBox_Core(config[0])
        fileList = getftp.get_ftp_files()
        return render(request,'nymebox_ftpcheck.html',{'output':fileList})

def FTPLog(request):
        fileContents = ""
        return render(request,'nymebox_logfile.html',{'output':fileContents})
        
@csrf_protect
def do_ftp(request):
        #return HttpResponse("Trying to do an FTP!")
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        ftping = NymeBox_Core(config[0])
        ftping.do_ftp()
        return render(request, 'nymebox_home.html', {'config':config[0], 'ftpbutton':'none', 'resetbutton':'default'})
        
def config_by_id(request, config_id):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        return render(request, 'config_details.html', {'config':config[config_id]})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")

def last_results(request):
        fileContents = ''
        return render(request,'nymebox_lastlog.html',{'output':fileContents})