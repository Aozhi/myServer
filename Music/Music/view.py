from django.shortcuts import render, HttpResponse
import os
import json
import requests
import simplejson
import subprocess

Rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Codepath =  "/home/baby/pang/aimusic/magenta/magenta/models"
Modelpath = "/home/baby/pang/aimusic/Data/lightmusic_cp"
static_path = "/home/baby/pang/Server/DMZ/static/wav"
def MusicGenerate(request):
    if request.method == 'POST':
    #     req = json.loads(request.body)
        # response1 = request.POST.get("http://localhost:8001")
        req = simplejson.loads(request.body)
        filename = req['filename']
        midistart = req['midistart']
        # midistart = response1.json() 

    INTERPRETER = "/home/baby/.conda/envs/python2/bin/python"
    TIMIDITY = "/usr/bin/timidity"
    if not os.path.exists(INTERPRETER): 
        log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER)  
    processor = os.path.join(Codepath, 'performance_rnn/performance_rnn_generate.py')
    output_dir = '--output_dir='+os.path.join(Rootpath, os.path.join('Music_nas',str(filename)))
    midi_start = '--primer_melody='+midistart 
    cmd_genmidi = [INTERPRETER] + [processor] + ['--bundle_file=/home/baby/pang/aimusic/Data/performance.mag'] + ['--config=performance'] + ['--num_outputs=1'] + ['--num_steps=600'] + [output_dir] + [midi_start]   
    # cmd_genmidi = [INTERPRETER] + [processor] + ['--run_dir='] +  [Modelpath] + ['--config=performance'] + ['--num_outputs=1'] + ['--num_steps=6000'] + ['--output_dir='] + [output_dir] + ['--primer_melody=']+[midistart]   
    # print(cmd_genmidi)
    my_env = os.environ
    my_env["PATH"]= INTERPRETER
    outputs1 = subprocess.check_output(cmd_genmidi, env=my_env, stderr=subprocess.STDOUT)
    # outputs = subprocess.check_output(cmd_genmidi, stderr=subprocess.STDOUT)
    # for dirpath, dirnames, filenames in (os.walk(os.path.join(Rootpath, os.path.join('Music_nas',str(filename))))):
    #     print(dirpath)
    #     print(dirnames)
    #     print(filenames)
    filelist = [(os.path.join(Rootpath, os.path.join('Music_nas',str(filename))))+'/'+ i for i in os.listdir(os.path.join(Rootpath, os.path.join('Music_nas',str(filename))))]
    midifile=os.path.join(str(os.path.join(Rootpath, os.path.join('Music_nas',str(filename)))),str(filelist[0]))
    os.mkdir(str(os.path.join(static_path, str(filename))))

    wavfile=os.path.join(str(os.path.join(static_path, str(filename))), str(filename+'.wav'))
    cmd_midi2wav = [TIMIDITY] + [midifile] + ['-Ow'] + ['-o'] + [wavfile]
    # print(cmd_midi2wav)
    # outputs2 = subprocess.Popen(cmd_midi2wav, env=my_env)
    outputs2 = subprocess.check_output(cmd_midi2wav, env=my_env, stderr=subprocess.STDOUT)
    #outputs = outputs.split('\n')
    # print(wavfile)
    # reponse_2 = requests.post("localhost:8000/upload_midi/", data = json.dumps({'wavdir':wavfile}))
    oggfile=os.path.join(str(os.path.join(static_path, str(filename))), str(filename+'.ogg'))
    cmd_midi2ogg = [TIMIDITY] + [midifile] + ['-Ov'] + ['-o'] + [oggfile]
    # print(cmd_midi2wav)
    # outputs2 = subprocess.Popen(cmd_midi2wav, env=my_env)
    outputs3 = subprocess.check_output(cmd_midi2ogg, env=my_env, stderr=subprocess.STDOUT)
    mp3file=os.path.join(str(os.path.join(static_path, str(filename))), str(filename+'.mp3'))
    cmd_wav2mp3 = ["/home/baby/.conda/envs/py3/bin/ffmpeg"] + ['-i'] + [wavfile] + ['-f'] + ['mp3']+ ['-acodec'] + ['libmp3lame'] + ['-y'] + [mp3file]    
    # outputs4 = subprocess.check_output(cmd_wav2mp3, env=my_env, stderr=subprocess.STDOUT)
    return HttpResponse("generated over!") 

