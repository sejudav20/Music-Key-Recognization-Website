from django.urls import path
from . import views

app_name = 'keys'
urlpatterns = [
    path('', views.upload, name="upload"),
    path('upload/', views.upload, name="upload"),
    path('upload/results/file/upload', views.resultsFileUpload, name="results_upload"),
    path('<str:notes>/<str:key>/<str:mode>/results/', views.results, name="results"),
    path('upload/results/file/record', views.resultsRecord, name="results_record"),
    path('upload/results/file/spotify', views.resultsSpotify, name="results_spotify")

   
]