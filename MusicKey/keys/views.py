from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from pydub import AudioSegment
from keys.analysis import predict
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
import keys.cred as cred

# Create your views he


def upload(request):
    return render(request, 'keys/upload.html', {})


def resultsSpotify(request):
    note_list = ['C', 'C#', 'D', 'D#', 'E',
                 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    scope = "user-read-recently-played"
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id,
                                                    client_secret=cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))
        
        
        id = request.POST["sp_input"]
        song = sp.track(id)
        preview_url = song['preview_url']
        name = song["name"]
        image = song["album"]["images"][0]["url"]
        artist =song["artists"][0]["name"]
        song_features = sp.audio_features(song["uri"])[0]
        tempo = song_features["tempo"]
        key = song_features["key"]
        key = note_list[key]
        mode ="minor" if song_features["mode"] == 0 else "major"
        energy = song_features["energy"]
        loudness = song_features["loudness"]
        time_sig = song_features["time_signature"] 
        return render(request, 'keys/results_sp.html', {'name':name,'author': artist,'key': key, 'mode': mode, 'tempo': tempo, 'energy': energy, 'loudness': loudness, 'time_sig':time_sig, "preview_url": preview_url,"image": image})
    except Exception:
        return sendError('Spotify Link or id was invalid', request)
   


def resultsFileUpload(request):
    # major key detector 53.24%
    # minor key detector 50.99%
    # Mode detector 61.52%
    uploaded_file = request.FILES.get('music_file', None)
#     with open('', 'wb+') as destination:
 #       for chunk in uploaded_file.chunks():
  #          destination.write(chunk)
    sound = AudioSegment.from_file(uploaded_file)
    sound = sound.set_channels(1)
    sound.export('myfile.wav', format='wav')

    notes, key, mode = predict('myfile.wav')
    print("Hello predicted ", notes, key, mode)
    notes = notes[0]
    note_list = ['C', 'C#', 'D', 'D#', 'E',
                 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = note_list[key]
    if mode == 0:
        mode = 'Minor'
    else:
        mode = 'Major'
    i = 1
    str_note = ""
    for note in notes:
        if i > 5:
            break
        str_note += " " + note_list[note]
        i += 1
    return HttpResponseRedirect(reverse('keys:results', args=(str_note, key, mode)))


def sendError(error_message, request):
    return render(request, 'keys/upload.html', {'error_message':error_message})


def resultsRecord(request):
    # recorded_file=request.POST["audio_url"]
    recorded_file = request.FILES.get('audio_url')

    sound = AudioSegment.from_file(recorded_file)
    sound = sound.set_channels(1)
    sound.export('myfile.wav', format='wav')

    notes, key, mode = predict('myfile.wav')
    print("Hello predicted ", notes, key, mode)
    notes = notes[0]
    note_list = ['C', 'C#', 'D', 'D#', 'E',
                 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = note_list[key]
    if mode == 0:
        mode = 'Minor'
    else:
        mode = 'Major'
    i = 1
    str_note = ""
    for note in notes:
        if i > 5:
            break
        str_note += " " + note_list[note]
        i += 1
    return HttpResponseRedirect(reverse('keys:results', args=(str_note, key, mode)))


def results(request, notes, key, mode):
    notes = notes.split()
    return render(request, 'keys/results.html', {'notes': notes, 'key': key, 'mode': mode})
