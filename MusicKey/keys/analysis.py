from scipy.io import wavfile
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from django.templatetags.static import static

from sklearn.preprocessing import MinMaxScaler
import os
def predict(filename):
    
    df=pd.DataFrame()
    df=convert_song_frequency(df, filename)
    print(df.columns)
    for i in range(0,100):
        df[i] = df[i].apply(convert_frequency_to_note)
    key_model=XGBClassifier()
    mode_model=XGBClassifier()
    
    key_url = os.path.dirname(os.path.realpath(__file__)) + '/static/keys/key_detector.model'
    mode_url = os.path.dirname(os.path.realpath(__file__)) + '/static/keys/mode_detector.model'
    test_url=static('../keys/test.png')
    print("test url------", test_url)
    with open(os.path.dirname(os.path.realpath(__file__)) + '/static/keys/test.png') as f:
        print(f.name)

    scalerf = MinMaxScaler(feature_range=(0, 1))

    features = scalerf.fit_transform(df.loc[:,0:23])
    print(features.shape)
    key_model.load_model(key_url)
    mode_model.load_model(mode_url)
    key_pred=key_model.predict(features)
    mode_pred=key_model.predict(features)
    return (df.values.tolist(),key_pred[0], mode_pred[0])

def convert_song_frequency(df, filename):
    sample_rate, data=wavfile.read(filename)
    song_data=[]
    frequency_num=100
    t = np.arange(data.shape[0])
    freq=np.fft.fftfreq(t.shape[-1])*sample_rate
    amps = abs(np.fft.fft(data).real)
    freq_data = pd.DataFrame({'frequency':freq,'amplitude': amps},columns=['frequency', 'amplitude'])
    freq_data = freq_data[freq_data['frequency']>0]
    dfreq=freq_data.nlargest(frequency_num,'amplitude')
    dfreq['frequency'].tolist()
    song_data.extend(dfreq['frequency'].tolist())
    df = df.append(pd.Series(song_data), ignore_index=True)
    return df

def convert_frequency_to_note(frequency):
    NOTES = {'C':261.63, 'C#':277.18, 'D':293.66, 'D#':311.13, 'E':329.63, 'F':349.23, 'F#':369.99, 'G':392.00, 'G#':415.30, 'A':440.00, 'A#':466.16, 'B':493.88}
    while(frequency<254.285):
        frequency*=2
    while(frequency>508.565):
        frequency/=2
    closest_name = 'C'
    min_distance=1000
    for name, f in NOTES.items():
        dist = abs(frequency - f)
        if(dist < min_distance):
            min_distance = dist
            closest_name = name
    notes=list(NOTES.keys())
    
    return notes.index(closest_name)


def main():
    pass

if __name__=='__main__':
    main()