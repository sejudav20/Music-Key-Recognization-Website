from django.shortcuts import render
from django import forms
from pydub import AudioSegment
# Create your views he

def upload(request):
    return render(request, 'keys/upload.html', {})


def resultsFileUpload(request):
    uploaded_file = request.POST["music_file"]
    sound = AudioSegment.from_file('newFile.mp3', format='mp3')

    sound.export('myfile.wav', format='wav')
    return render(request, "keys/results.html",{})

def resultsRecord(request):

    return render(request, "keys/results.html",{})