from django.shortcuts import render

from django.http import HttpResponse

from .models import ConfigItem

def index(request):
        return HttpResponse("Hello World!")

def config_by_id(request, config_id):
        config = ConfigItem.objects.get(pk=config_id)
        return render(request, 'config_details.html', {'config':config})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")