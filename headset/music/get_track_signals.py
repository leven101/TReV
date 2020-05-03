import librosa
import numpy as np
import pandas as pd
import os

track_path = '/Users/abby/work/TReV/music/audio-files/dt_16bars_102rap.wav'

# default values
sr = 22050  # sampling rate of music = audio spectrum
hop_length = 512  # how many audio frames per fft
n_fft = 2205  # number of buckets to divide audio spectrum into
hz_per_fft = int(sr / n_fft)  # sr/n_fft = hz buckets per fft

bass_range_hz = [60, 260]
treble_range_hz = [2000, 4000]
bass_range_idx = [int(bass_range_hz[0]/hz_per_fft), int(bass_range_hz[1]/hz_per_fft)]
treble_range_idx = [int(treble_range_hz[0]/hz_per_fft), int(treble_range_hz[1]/hz_per_fft)]

y, sr = librosa.load(track_path, sr)
# get length
track_seconds = librosa.get_duration(y, sr)
print('Track time: ', track_seconds)
print('One frame in seconds: ', track_seconds / sr)

# get tempo with the default beat tracker
tempo, beat_times = librosa.beat.beat_track(y, sr, hop_length=hop_length)
print('Tempo: ', tempo)

# get SFT
hz_db = librosa.amplitude_to_db(abs(librosa.stft(y, n_fft, hop_length)))
hz_db[hz_db < 0] = 0
print(hz_db.shape)
print('Seconds per hop: ', track_seconds / hz_db.shape[1])
n_hops_sec = int(1 / (track_seconds / hz_db.shape[1]))
print('hops per second: ', n_hops_sec)

df = pd.DataFrame(columns=['seconds', 'top', 'bottom', 'tempo'])

for i in range(0, hz_db.shape[1], n_hops_sec):
    # aggregate the bass and treble signal over the n_hops
    tmp = hz_db[:, i:i + n_hops_sec]
    bass_db = np.sum(tmp[bass_range_idx[0]:bass_range_idx[1]])
    treb_db = np.sum(tmp[treble_range_idx[0]:treble_range_idx[1]])
    tot_db = bass_db + treb_db
    if tot_db > 0:
        bass_db /= tot_db
        treb_db /= tot_db
    df.loc[df.shape[0]] = [1, bass_db, treb_db, tempo]


df.to_csv('{}-track-data.csv'.format(os.path.basename(track_path)), index=False)

