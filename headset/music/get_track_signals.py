import librosa
import numpy as np
import pandas as pd
import os

import headset.shared as shared

track_path = '/Users/abby/work/TReV/music/audio-files/revolt.malaa.m4a'
# track_path = '/Users/abby/work/TReV/music/audio-files/tones/100hz.wav'

# default values
sr = 22050  # sampling rate of music = audio spectrum
hop_length = 512  # how many audio frames per fft
n_fft = 2205  # number of buckets to divide audio spectrum into
hz_per_fft = int(sr / n_fft)  # sr/n_fft = hz buckets per fft


bass_range_hz = [50, 300]
treble_range_hz = [750, 1000]
bass_range_idx = [int(bass_range_hz[0]/hz_per_fft), int(bass_range_hz[1]/hz_per_fft)]
treble_range_idx = [int(treble_range_hz[0]/hz_per_fft), int(treble_range_hz[1]/hz_per_fft)]

y, sr = librosa.load(track_path, sr)
# get length
track_seconds = librosa.get_duration(y, sr)
print('Track time: ', track_seconds)
print('One frame in seconds: ', track_seconds / sr)

# get tempo and note
note = shared.note_dict['1/4']  # how long the light should be on for each beat
bpm, beat_times = librosa.beat.beat_track(y, sr, hop_length=hop_length)
print('BPM: ', bpm)
tempo = shared.get_tempo(bpm, note)
print('tempo: ', tempo)


# get SFT
hz_db = librosa.amplitude_to_db(abs(librosa.stft(y, n_fft, hop_length)))
hz_db[hz_db < 0] = 0
print(hz_db.shape)
hops_per_second = track_seconds / hz_db.shape[1]
print('hops per seconds: ', hops_per_second)

beats_per_sec = 1 / note
interval_beat = beats_per_sec * (tempo + note)
n_hops_interval = int(round(interval_beat / hops_per_second))
print('hops per interval: ', n_hops_interval)

df = pd.DataFrame(columns=['seconds', 'top', 'bottom', 'tempo', 'note'])

for i in range(0, hz_db.shape[1], n_hops_interval):
    # aggregate the bass and treble signal over the n_hops
    tmp = hz_db[:, i:i + n_hops_interval]
    bass_db = np.sum(tmp[bass_range_idx[0]:bass_range_idx[1]])
    treb_db = np.sum(tmp[treble_range_idx[0]:treble_range_idx[1]])
    tot_db = bass_db + treb_db
    if tot_db > 0:
        bass_db /= tot_db
        treb_db /= tot_db
    if i + n_hops_interval > hz_db.shape[1]:
        interval_beat = track_seconds - np.sum(df['seconds'])
    if interval_beat > 0:
        df.loc[df.shape[0]] = [interval_beat, bass_db, treb_db, tempo, note]

df.to_csv('track-data/{}-track-data.csv'.format(os.path.basename(track_path)), index=False)

