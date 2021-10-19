# Music Key Recognization Website
This personal project uses the Django web framework to create a website to recognize keys from audio recordings. The website uses Xgboost a machine learning algorithm to predict the key based on the frequencies extracted from the audio file. The algorithm was trained on a custom dataset of 40,000 songs compiled using Pandas and the Spotify API.
The website also allows users to put spotify urls and get data such as the key, time signature and preview mp3 file straight from the Spotify API. The algorithm however still struggles to recognize key due to key recognition being more than just the frequencie overtones present and would take more analysis to create a better classifier.
Home Screen
![image](https://user-images.githubusercontent.com/23585933/137997691-d209d54a-d524-4991-822b-9b9b6cfeddb7.png)
Uploaded Song data:
![image](https://user-images.githubusercontent.com/23585933/137998238-31ecbc21-4c44-4e2b-aabd-c45b56156b63.png)

Spotify Song Data
![image](https://user-images.githubusercontent.com/23585933/137997725-f09d5a13-6861-47e8-825a-9c698a0c57a8.png)
