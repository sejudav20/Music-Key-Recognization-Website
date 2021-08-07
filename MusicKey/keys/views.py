from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from pydub import AudioSegment
from keys.analysis import predict
# Create your views he

def upload(request):
    return render(request, 'keys/upload.html', {})


def resultsFileUpload(request):
    
    uploaded_file = request.FILES.get('music_file',None)
#     with open('', 'wb+') as destination:
 #       for chunk in uploaded_file.chunks():
  #          destination.write(chunk)
    sound = AudioSegment.from_file(uploaded_file)
    sound = sound.set_channels(1)
    sound.export('myfile.wav', format='wav')
    
    notes, key, mode= predict('myfile.wav') 
    print("Hello predicted ",notes, key, mode)
    notes=notes[0]
    note_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key=note_list[key]
    if mode == 0:
        mode='Minor'
    else:
        mode='Major'
    i=1
    str_note=""
    for note in notes:
        if i>5:
            break
        str_note+=" " + note_list[note]
        i+=1
    return HttpResponseRedirect(reverse('keys:results', args=(str_note,key, mode)))


def resultsRecord(request):
    #recorded_file=request.POST["audio_url"]
    recorded_file = request.FILES.get('audio_url')
    
    sound = AudioSegment.from_file(recorded_file)
    sound = sound.set_channels(1)
    sound.export('myfile.wav', format='wav')
    
    notes, key, mode= predict('myfile.wav') 
    print("Hello predicted ",notes, key, mode)
    notes=notes[0]
    note_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key=note_list[key]
    if mode == 0:
        mode='Minor'
    else:
        mode='Major'
    i=1
    str_note=""
    for note in notes:
        if i>5:
            break
        str_note+=" " + note_list[note]
        i+=1
    return HttpResponseRedirect(reverse('keys:results', args=(str_note,key, mode)))

def results(request, notes, key, mode):
    notes=notes.split()
    return render(request, 'keys/results.html', {'notes': notes,'key': key, 'mode':mode})