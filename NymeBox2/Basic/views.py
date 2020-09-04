from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .models import ConfigItem
from .nymebox import NymeBox_Core

def index(request):
        return HttpResponse("Hello World!")

def nymebox_home(request):
        config = ConfigItem.objects.get(pk=1)
        return render(request, 'nymebox_home.html', {'config':config})

@csrf_protect
def do_ftp(request):
        #return HttpResponse("Trying to do an FTP!")
        #config = ConfigItem.objects.get(pk=1)
        #doing_ftp = NymeBox_Core.do_ftp(config.FTP_URL,config.FileType_List)
        return render(request,'nymebox_output.html')

def config_by_id(request, config_id):
        config = ConfigItem.objects.get(pk=config_id)
        return render(request, 'config_details.html', {'config':config})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")