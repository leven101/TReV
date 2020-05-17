import librosa
import numpy as np
import pandas as pd
import os

import headset.shared as shared

track_path = '/Users/abby/work/TReV/music/audio-files/b5.m4a'
# track_path = '/Users/abby/work/TReV/music/audio-files/tones/100hz.wav'

# global default values
sr = 22050  # sampling rate of music
hop_length = 512  # how many audio frames per fft
n_fft = 2205  # number of buckets to divide audio spectrum into
hz_per_fft = int(sr / n_fft)  # sr/n_fft = hz buckets per fft
bass_range_hz = [50, 300]
treble_range_hz = [750, 1000]
bass_range_idx = [int(bass_range_hz[0] / hz_per_fft), int(bass_range_hz[1] / hz_per_fft)]
treble_range_idx = [int(treble_range_hz[0] / hz_per_fft), int(treble_range_hz[1] / hz_per_fft)]


def load_track(mono=True):
    y, _ = librosa.load(track_path, sr, mono=mono)
    # y, _ = librosa.load(librosa.util.example_audio_file(), duration=10, sr=sr, mono=mono)
    # get length
    track_seconds = librosa.get_duration(y, sr)
    print('Track time: ', track_seconds)
    print('One frame in seconds: ', track_seconds / sr)
    return y, track_seconds


def track_tempo(y, note=shared.note_dict['1/4']):
    # tempo is how many times per second we flash the light
    # note is how long the light should be on for each beat/flash
    bpm, beat_times = librosa.beat.beat_track(y, sr, hop_length=hop_length)
    print('BPM: ', bpm)
    tempo = shared.get_tempo(bpm, note)
    print('tempo: ', tempo)
    return tempo, note


def hops_per_interval(tempo, note, seconds, num_hops):
    # window size of hops for each time frame
    hops_per_second = seconds / num_hops
    print('hops per seconds: ', hops_per_second)
    beats_per_sec = 1 / note
    interval_beat = beats_per_sec * (tempo + note)
    n_hops_interval = int(round(interval_beat / hops_per_second))
    print('hops per interval: ', n_hops_interval)
    return interval_beat, n_hops_interval


def stereo_signal():
    y, track_seconds = load_track(False)

    tempo_l, note = track_tempo(y[0])
    tempo_r, _ = track_tempo(y[1])

    D = librosa.stft(librosa.to_mono(y), n_fft, hop_length)
    rp = np.median(np.abs(D))  # global reference power
    # remove noise by requiring that the horizontal and vertical filters differ by margin
    D_harmonic, D_percussive = librosa.decompose.hpss(D, margin=16)

    hz_db_harm = librosa.amplitude_to_db(abs(D_harmonic), ref=rp)
    hz_db_harm[hz_db_harm < 0] = 0
    print('hz_db_harm:', hz_db_harm.shape)
    hz_db_perc = librosa.amplitude_to_db(abs(D_percussive), ref=rp)
    hz_db_perc[hz_db_perc < 0] = 0
    print('\nhz_db_perc:', hz_db_perc.shape)
    avg_tempo = np.mean([tempo_l, tempo_r])
    interval_beat, n_hops_interval = hops_per_interval(avg_tempo, note, track_seconds, hz_db_harm.shape[1])

    df = pd.DataFrame(columns=['seconds', 'harmonic', 'percussive', 'tempo_left', 'tempo_right', 'note'])
    for i in range(0, hz_db_harm.shape[1], n_hops_interval):
        treb_db = np.sum(hz_db_harm[treble_range_idx[0]:treble_range_idx[1], i:i + n_hops_interval])
        bass_db = np.sum(hz_db_perc[bass_range_idx[0]:bass_range_idx[1], i:i + n_hops_interval])
        tot_db = bass_db + treb_db
        if tot_db > 0:
            bass_db /= tot_db
            treb_db /= tot_db
        if i + n_hops_interval > hz_db_harm.shape[1]:
            interval_beat = track_seconds - np.sum(df['seconds'])
        if interval_beat > 0:
            df.loc[df.shape[0]] = [interval_beat, bass_db, treb_db, tempo_l, tempo_r, note]
    df.to_csv('track-data/stereo-track-data.csv', index=False)


def mono_signal():
    y, track_seconds = load_track()
    tempo, note = track_tempo(y)

    # get SFT
    hz_db = librosa.amplitude_to_db(abs(librosa.stft(y, n_fft, hop_length)))
    hz_db[hz_db < 0] = 0
    print(hz_db.shape)
    interval_beat, n_hops_interval = hops_per_interval(tempo, note, track_seconds, hz_db)

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

    df.to_csv('track-data/test-track-data.csv', index=False)
    # df.to_csv('track-data/{}-track-data.csv'.format(os.path.basename(track_path)), index=False)


if __name__ == '__main__':
    # mono_signal()
    stereo_signal()
