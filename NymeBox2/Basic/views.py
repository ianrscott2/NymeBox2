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
from django.db import connection
from django.shortcuts import redirect

if 'nymebox' in socket.gethostname():
        app_mode = "PROD"
else:
        app_mode = "TEST"

configQuery = "SELECT * FROM basic_configitem WHERE ProcMode = %s"

def system_check():
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        nymebox_core = NymeBox_Core(config[0])
        mount = nymebox_core.mount_sdcard()
        fileList = nymebox_core.get_ftp_files()
        ftpButton = 'none'
        mountButton = 'none'
        fileCheckButton = 'none'

        if not mount == "Success":
                mountButton = 'default'
        elif not fileList:
                fileCheckButton = 'default'
        else:
                ftpButton = 'default'

        return mountButton, fileCheckButton, ftpButton 

def nymebox_home(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        buttonStatus = system_check()
        return render(request, 'nymebox_home.html', {'config':config[0], 'mountButton': buttonStatus[0], 'fileCheckButton': buttonStatus[1],'ftpButton': buttonStatus[2]})

def ftpCheckList(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        getftp = NymeBox_Core(config[0])
        fileCheckList = getftp.get_ftp_files()
        fileCheckList = '\n'.join(fileCheckList)
        return render(request, 'nymebox_ftpcheck.html', {'fileCheckList': fileCheckList})

def ftpCheck(request):
        #buttonStatus = system_check()
        response = redirect('/')
        return response

def FTPLog(request):
        fileContents = ""
        return render(request,'nymebox_logfile.html',{'output':fileContents})
        
@csrf_protect
def do_ftp(request):
        #return HttpResponse("Trying to do an FTP!")
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        ftping = NymeBox_Core(config[0])
        logInfo = ftping.do_ftp()
        #response = redirect('/')
        #return response
        #print(logInfo)
        return render(request,'nymebox_completed.html',{'logInfo':logInfo[0],'logInfoStatus':logInfo[1]})
        
def config_by_id(request, config_id):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        return render(request, 'config_details.html', {'config':config[config_id]})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")

def last_results(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        return render(request,'nymebox_lastlog.html',{'lastLog':config[0].LastLog})

def mount_sdcard(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        mount_card = NymeBox_Core(config[0])
        mount = mount_card.mount_sdcard()
        fileListUpdate = "UPDATE basic_configitem SET LastLog = %s WHERE ProcMode = %s;"
        with connection.cursor() as cursor:
            cursor.execute(fileListUpdate, [mount, self.app_mode])
        response = redirect('/')
        return response