from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from Basic.models import ConfigItem
from .nymebox import NymeBox_Core

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

app_mode = "TEST"

def index(request):
        return HttpResponse("Hello World!")

def nymebox_home(request):
        config = ConfigItem.Manager.raw('SELECT FtpURL, FileTypeList, FTPUser, FTPPassword, SourceDir, DestDir,ProcMode FROM basic_configitem WHERE ProcMode = %s', [app_mode])
        print("the config type is: " + str(type(config)) + "\n")
        print("the config type is: " + config[0].FtpURL + "\n")
        return render(request, 'nymebox_home.html', {'config':config[0]})

def updatefile(request):
        return render(request,'test_log.html')

def FTPLog(request):
        outputfile = open("Basic//FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        outputfile.close()
        return render(request,'nymebox_logfile.html',{'output':fileContents})
        
@csrf_protect
def do_ftp(request):
        #return HttpResponse("Trying to do an FTP!")
        config = ConfigItem.Manager.raw('SELECT * FROM basic_configitem WHERE ProcMode = %s', [app_mode])
        ftping = NymeBox_Core(config[0])
        ftping.do_ftp()
        outputfile = open("Basic//FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_output.html',{'output':fileContents})

def config_by_id(request, config_id):
        config = ConfigItem.Manager.raw('SELECT * FROM basic_configitem WHERE ProcMode = %s', [app_mode])
        return render(request, 'config_details.html', {'config':config[config_id]})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")

def last_results(request):
        outputfile = open("Basic//FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_lastlog.html',{'output':fileContents})