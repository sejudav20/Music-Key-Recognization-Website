from django.shortcuts import render

# Create your views he

def upload(request):
    return render(request, 'keys/upload.html', {})

def results(request):
    return render(request, "keys/results.html",{})
