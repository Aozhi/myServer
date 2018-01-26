from django.shortcuts import render, HttpResponse
from . import models
# Create your views here.
Rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def music_home(request):
    return render(request,'music_home.html')

def upload_midi(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        myFile = request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!")  
        else:
        	destination = open(os.path.join(Rootpath, os.path.join(nas, myFile.name)),'wb+')    # 打开特定的文件进行二进制的写操作 writed to nas  
	        for chunk in myFile.chunks():      # 分块写入文件  
	            destination.write(chunk)  
	        destination.close()  

	        return HttpResponse("upload over!") 

# def play_midi(request):
#     context = {}
#     context['hello']='midiplayer'
#     return render(request,'midiplayer.html',context)