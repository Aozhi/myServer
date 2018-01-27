from django.shortcuts import render, HttpResponse
from . import models
import os
import time


# Create your views here.
Rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def music_home(request):
    return render(request,'music_home.html')

def upload_midi(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        midistart = request.POST.get("midistart", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not midistart:  
            return HttpResponse("no files for upload!")  
        else:
            date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
            midifile_dest = os.path.join(Rootpath, os.path.join('DMZ_nas', date_and_time+'.midistart')) # shall be stored in db
            mf = open(midifile_dest,'w')    # 打开特定的文件 wrote to nas    
            mf.write(midistart)
            mf.close
            # for chunk in midistart.chunks():      # 分块写入文件nas  
            #     destination.write(chunk)  
            # destination.close()  
            return HttpResponse("upload over!") 
