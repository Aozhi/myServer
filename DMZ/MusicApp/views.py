from django.shortcuts import render, HttpResponse
from . import models
import os
import time
import socket
import logging
import json
import requests
import simplejson
# import urllib

# Create your views here.
Rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Static_path = "/home/baby/pang/Server/DMZ/static"
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
            log = logging.getLogger("Core.Analysis.Processing")
            post_server = "localhost:8000"
            # req = urllib.request(post_server,json.dumps({'filename' : date_and_time, 'midistart' : midistart}))   #生成页面请求的完整数据
            # response = urlopen(req)    # 发送页面请求
            # except urllib2.HTTPError,error:
            #     print ("ERROR:error.read()")
            response = requests.post("http://localhost:8007/generator/", data = json.dumps({'filename':date_and_time, 'midistart' : midistart}))
    # if request.method == 'POST':
        # req2 = simplejson.loads(request.body)
        # filedir = req['wavdir']
        # print(filedir)
        # response.getOutputSteam(wavfile)
        # reponse2 = request.POST.get("wavfile", None)
            print(response)
            # content = {'wavdir':reponse2}
            while True: 
                        # print(str(Static_path)+ '/' + str(date_and_time) + '/' + str(date_and_time) + '.wav')
                if os.path.isfile(str(Static_path) + '/wav/' + str(date_and_time) + '/' + str(date_and_time) + '.wav'):
                    content = {'wavdir': 'wav/' + str(date_and_time) + '/' + str(date_and_time) + '.wav',
                               'oggdir': 'wav/' + str(date_and_time) + '/' + str(date_and_time) + '.ogg',
                               'mp3dir': 'wav/' + str(date_and_time) + '/' + str(date_and_time) + '.mp3'}
                    # content = {'wavdir': str(Static_path)+'/wav/' + str(date_and_time) + '/' + str(date_and_time) + '.wav'}
                    break;
            return render(request,'wavplayer.html', content)
            # return HttpResponse("upload over!") 
        # if request.POST.get("1.wav", None):
             

