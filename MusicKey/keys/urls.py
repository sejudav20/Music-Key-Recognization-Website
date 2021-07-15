from django.urls import path
from . import views

app_name = 'keys'
urlpatterns = [
    path('', views.upload, name="upload"),
    path('upload/', views.upload, name="upload"),
    path('results/', views.results, name="upload")
   
]