from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from Basic.models import ConfigItem
from .nymebox import NymeBox_Core
from .nymebox_ftpfilecheck import NymeBox_Check

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

app_mode = "TEST"
FTPLogFile = "Basic//FTP_Progress.txt"
FTPCheckFile = "Basic//FTP_FileCheck.txt"
configQuery = "SELECT * FROM basic_configitem WHERE ProcMode = %s"

def index(request):
        return HttpResponse("Hello World!")

def nymebox_home(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        return render(request, 'nymebox_home.html', {'config':config[0]})

def updatefile(request):
        return render(request,'test_log.html')

def ftpCheck(request):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        ftping = NymeBox_Check(config[0])
        ftping.check_ftp_files()
        outputfile = open(FTPCheckFile, "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_ftpcheck.html',{'output':fileContents})

def FTPLog(request):
        outputfile = open(FTPLogFile, "r")
        fileContents=outputfile.read()
        outputfile.close()
        return render(request,'nymebox_logfile.html',{'output':fileContents})
        
@csrf_protect
def do_ftp(request):
        #return HttpResponse("Trying to do an FTP!")
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        ftping = NymeBox_Core(config[0])
        ftping.do_ftp()
        outputfile = open(FTPLogFile, "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_output.html',{'output':fileContents})

def config_by_id(request, config_id):
        config = ConfigItem.Manager.raw(configQuery, [app_mode])
        return render(request, 'config_details.html', {'config':config[config_id]})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")

def last_results(request):
        outputfile = open(FTPLogFile, "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_lastlog.html',{'output':fileContents})