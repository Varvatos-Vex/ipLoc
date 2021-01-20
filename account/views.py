from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime
import shutil
import json
import sys
import subprocess
from django.http import HttpResponse, Http404
import mimetypes

# Create your views here.
from .forms import CreateUserForm

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('accounts')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)                
                return redirect('login')
        context = {'form':form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('accounts')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('accounts')
            else:
                messages.info(request, 'Username OR password is incorrect')
                
        context = {}
        return render(request, 'accounts/login.html', context)
        

def logoutUser(request):
    logout(request)
    return redirect('login')

#-------------------Landing Page Viw-----------------------
@login_required(login_url='login')
def home_view(request):
    kmoniter = ServiceMonitor('kibana')
    emoniter = ServiceMonitor('elasticsearch')
    lmoniter = ServiceMonitor('logstash')
    data = []
    data.append('badge-success') if kmoniter.is_active() else data.append('badge-danger')
    data.append('badge-success') if emoniter.is_active() else data.append('badge-danger')
    data.append('badge-success') if lmoniter.is_active() else data.append('badge-danger')

    #print(data)
    return render(request, "accounts/services.html",context={"data" : data})

#---------------------File copy data from Media folder to Ingestion Folder------
@login_required(login_url='login')
def ingestion(request):
    tmp_file = ""
    selectIndex = ""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('ingestion_file')
        if uploaded_file is not None:
            name = uploaded_file.name #----Access File Name
            #print(uploaded_file.readlines)
            path = default_storage.save(name, ContentFile(uploaded_file.read())) #----Save File in default Location
            tmp_file = os.path.join(settings.MEDIA_ROOT, path) #----File Path 
            print('FIle upload Succesfully For Ingestion............')
            #print(tmp_file)
    if request.method == 'POST' and 'SelectIndex' in request.POST:
        selectIndex = request.POST.get('SelectIndex')
        #print(selectIndex)
    movingFile(selectIndex,tmp_file)
    return render(request, "accounts/ingestion.html")

#---------------------Moving file from ingestion to ingested Folder-------
def movingFile(index,sourcePath):
    dataLakePath = "/home/ta2/Desktop/Datalake_TA/data/DataLake/"
    dataLakeTAPath = "/home/ta2/Desktop/Datalake_TA/data/DataLake_TA/"
    CompendiumPath = "/home/ta2/Desktop/Datalake_TA/data/Compendium/"
    TPIPath = "/home/ta2/Desktop/Datalake_TA/data/TPI/"
    mediaFilePath = "/home/ta2/Desktop/python elastic/ipLoc-master/media/"
    
    if(sourcePath != ""):
        fileName = os.path.basename(sourcePath)
        if(index == "Data Lake"):            
            clearLocation(dataLakePath) #------ Function Clear the Path of Input Index
            shutil.move(os.path.join(mediaFilePath, fileName), dataLakePath)           
        elif(index == "Data Lake TA"):
            clearLocation(dataLakeTAPath) #------ Function Clear the Path of Input Index
            shutil.move(os.path.join(mediaFilePath, fileName), dataLakeTAPath)
        elif(index == "Compendium"):
            clearLocation(CompendiumPath) #------ Function Clear the Path of Input Index
            shutil.move(os.path.join(mediaFilePath, fileName), CompendiumPath) 
        else:
            clearLocation(TPIPath) #------ Function Clear the Path of Input Index
            shutil.move(os.path.join(mediaFilePath, fileName), TPIPath) 
    else:
        print("Select File............")

#-----------------Clean Ingestion File Path-------------
def clearLocation(sourcePath1):
    date = datetime.today().strftime('%Y-%m-%d')
    #sourcePath = '/home/ta2/Desktop/python elastic/source'
    DestinationPath = '/home/ta2/Desktop/Datalake_TA/ingestedData/' + str(date) + '/'
    try:
        os.makedirs(DestinationPath) ## it creates the destination folder
    except:
        print("Folder already exist")
    file_names = os.listdir(sourcePath1)
    for file_name in file_names:
        shutil.move(os.path.join(sourcePath1, file_name), DestinationPath)
    print("Clear Path Succesfully")

#--------------------------------------Sevice call request responce-------------
@login_required
def service(request):
    service = request.GET.get('service')

    response = ''

    kmoniter = ServiceMonitor('kibana')
    emoniter = ServiceMonitor('elasticsearch')
    lmoniter = ServiceMonitor('logstash')

    if(service == 'kstart'):
        print("............Starting Kibana............")
        if kmoniter.start():
            response = 'Success'
        else:
            response = 'Failed'
        


    elif(service == 'kstop'):
        print("............Stop Kibana............")
        if kmoniter.stop():
            response = 'Success'
        else:
            response = 'Failed'


    elif(service == 'krestart'):
        print("............Restart Kibana............")
        if kmoniter.restart():
            response = 'Success'
        else:
            response = 'Failed'

    if(service == 'estart'):
        print("............Starting ElasticSearch............")
        if emoniter.start():
            response = 'Success'
        else:
            response = 'Failed'


    elif(service == 'estop'):
        print("............Stop Elastissearch............")
        if emoniter.stop():
            response = 'Success'
        else:
            response = 'Failed'


    elif(service == 'erestart'):
        print("............Restart Elastissearch............")
        if emoniter.restart():
            response = 'Success'
        else:
            response = 'Failed'


    if(service == 'lstart'):
        print("............Starting Logstash............")
        if lmoniter.start():
            response = 'Success'
        else:
            response = 'Failed'


    elif(service == 'lstop'):
        print("............Stop Logstash............")
        if lmoniter.stop():
            response = 'Success'
        else:
            response = 'Failed'


    elif(service == 'lrestart'):
        print("............Restart Logstash............")
        if lmoniter.restart():
            response = 'Success'
        else:
            response = 'Failed'

    if request.method == 'GET':
        return HttpResponse(response)
    else:
        return HttpResponse("unsuccesful")



#---------------------Check For System Services Running or not-------------
class ServiceMonitor(object):
    def __init__(self, service):
        self.service = service

    def is_active(self):
        """Return True if service is running"""
        cmd = '/bin/systemctl status %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,encoding='utf8')
        stdout_list = proc.communicate()[0].split('\n')
        for line in stdout_list:
            if 'Active:' in line:
                if '(running)' in line:
                    print("{} is Runnning".format(self.service))
                    return True
        
        print("{} is Not Runnning".format(self.service))
        return False

    def start(self):
        cmd = '/bin/systemctl start %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf8')
        stdout = proc.communicate()
        #print(stdout[0])
        try:
            if 'Failed' in stdout[1]:
                return False
            elif(stdout[0] == '' and stdout[1] == ''):
                return True
            else:
                return False
        except:
            return False

    def stop(self):
        cmd = '/bin/systemctl stop %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf8')
        stdout = proc.communicate()
        #print(stdout[0])
        try:
            if 'Failed' in stdout[1]:
                return False
            elif(stdout[0] == '' and stdout[1] == ''):
                return True
            else:
                return False
        except:
            return False

    def restart(self):
        cmd = '/bin/systemctl restart %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf8')
        stdout = proc.communicate()
        try:
            if 'Failed' in stdout[1]:
                return False
            elif(stdout[0] == '' and stdout[1] == ''):
                return True
            else:
                return False
        except:
            return False





#---------------------------File Service-------------------
@login_required
def fileserver(request):
    listFile = []
    DictFile = {}
    currDir = '/home/user/Desktop/kavach'
    listDir = path_to_dict(currDir)
    print(listDir)
    return JsonResponse(listDir)



def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d




#---------------------Download--------------------
@login_required
def download(request):
    filename = request.GET.get('q')
    #file_path = os.path.join(settings.MEDIA_ROOT, path)
    currDir = '/home/user/Desktop/kavach/'
    file_path = currDir + filename
    
    if os.path.exists(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404