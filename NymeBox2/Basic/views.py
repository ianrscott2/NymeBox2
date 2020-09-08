from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .models import ConfigItem
from .nymebox import NymeBox_Core

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

####################################  Progress Bar Code
from flask import Flask
from flask import render_template, request, jsonify, make_response

app = Flask(__name__)

@app.route("/progressBarTest", methods=["GET", "POST"])
def progressBarTest(request):

        if request.method == "POST":
                filesize = request.cookies.get("filesize")
                file = request.files["file"]

                print(f"Filesize:{filesize}")
                print(file)

                res = make_response(jsonify({"message": f"{file.filename} uploaded"}), 200)

                return res

        return render(request, 'upload_video.html', {'request':request})

########################################################


def index(request):
        return HttpResponse("Hello World!")

def nymebox_home(request):
        config = ConfigItem.objects.get(pk=1)
        return render(request, 'nymebox_home.html', {'config':config})

@csrf_protect
def do_ftp(request):
        #return HttpResponse("Trying to do an FTP!")
        config = ConfigItem.objects.get(pk=1)
        doing_ftp = NymeBox_Core.do_ftp(config)
        print(doing_ftp)
        outputfile = open("FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_output.html',{'output':fileContents})

def config_by_id(request, config_id):
        config = ConfigItem.objects.get(pk=config_id)
        return render(request, 'config_details.html', {'config':config})
        #return HttpResponse(f"Config Field: {config.field}, Value: {config.value}")

def last_results(request):
        outputfile = open("FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_output.html',{'output':fileContents})

def settings(request):
        outputfile = open("FTP_Progress.txt", "r")
        fileContents=outputfile.read()
        return render(request,'nymebox_output.html',{'output':fileContents})