from django.shortcuts import render, HttpResponse
import os
import json
import requests
import simplejson
import subprocess

Rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Codepath =  "/home/baby/pang/aimusic/magenta/magenta/models"
Modelpath = "/home/baby/pang/aimusic/Data/lightmusic_cp"
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
    cmd_genmidi = [INTERPRETER] + [processor] + ['--bundle_file=/home/baby/pang/aimusic/Data/performance.mag'] + ['--config=performance'] + ['--num_outputs=1'] + ['--num_steps=6000'] + [output_dir] + [midi_start]   
    # cmd_genmidi = [INTERPRETER] + [processor] + ['--run_dir='] +  [Modelpath] + ['--config=performance'] + ['--num_outputs=1'] + ['--num_steps=6000'] + ['--output_dir='] + [output_dir] + ['--primer_melody=']+[midistart]   
    # print(cmd_genmidi)
    my_env = os.environ
    my_env["PATH"]= INTERPRETER
    outputs1 = subprocess.Popen(cmd_genmidi, env=my_env)
    # outputs = subprocess.check_output(cmd_genmidi, stderr=subprocess.STDOUT)
    for dirpath, dirnames, filenames in os.walk(output_dir):
        print(filenames[0])
    midifile=os.path.join(output_dir,filenames[0])
    wavfile=os.path.join(output_dir,str(filename)+'.wav')
    cmd_midi2wav = [TIMIDITY] + [midifile] + ['-Ow'] + ['-o'] + [wavfile]
    print(cmd_midi2wav)
    outputs2 = subprocess.check_output(cmd_midi2wav, stderr=subprocess.STDOUT)
    # #outputs = outputs.split('\n')
    # reponse = request.POST("localhost:8000/generator", data = midistart)
    return HttpResponse("generated over!") 

