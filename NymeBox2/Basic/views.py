from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from Basic.models import ConfigItem
from .nymebox import NymeBox_Core

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

def index(request):
        return HttpResponse("Hello World!")

def nymebox_home(request):
        config = ConfigItem.ProcMode.get(pk=1)
        print(type(config))
        return render(request, 'nymebox_home.html', {'config':config})

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
        config = ConfigItem.ProcMode.get(pk=1)
        ftping = NymeBox_Core()
        ftping.do_ftp(config)
        outputfile = open("Basic//FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_output.html',{'output':fileContents})

def config_by_id(request, config_id):
        config = ConfigItem.ProcMode.get(pk=config_id)
        return render(request, 'config_details.html', {'config':config})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")

def last_results(request):
        outputfile = open("Basic//FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_lastlog.html',{'output':fileContents})