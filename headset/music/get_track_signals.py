import librosa
import numpy as np
import pandas as pd
import os
from math import ceil

import headset.shared as shared

track_path = '/Users/abby/work/TReV/music/audio-files/theotherside-jasonderulo.m4a'

# global default values
sr = 22050  # sampling rate of music
hop_length = 2048  # how many audio frames per fft
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


notee=4
def track_tempo(y, note=shared.note_dict['1/{}'.format(notee)]):
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


def by_beat_track_stereo():
    y, track_seconds = load_track(False)
    for idx in range(len(y)):
        _, beat_times = librosa.beat.beat_track(y=y[idx], sr=sr, units='time')
        beat_df = pd.DataFrame(columns=['beat', 'harmonic', 'percussive', 'note', 'cum_secs'])
        print('# of beats: {}'.format(len(beat_times)))
        beat_df['cum_secs'] = beat_times
        beat_df['beat'] = pd.Series(beat_times).diff()
        beat_df.loc[0, 'beat'] = beat_times[0]
        beat_df['note'] = shared.note_dict['1/{}'.format(notee)]
        beat_df['beat'] = beat_df['beat'] - beat_df['note']
        hz_db_harm, hz_db_perc = harm_vs_perc(y[idx])
        num_per_hop = ceil(hz_db_perc.shape[1] / len(beat_df))
        for i in range(len(beat_times)):
            idx_start = i * num_per_hop
            treb_db = np.sum(hz_db_harm[:, idx_start:idx_start + num_per_hop])
            bass_db = np.sum(hz_db_perc[:, idx_start:idx_start + num_per_hop])
            tot_db = bass_db + treb_db
            if tot_db > 0:
                bass_db /= tot_db
                treb_db /= tot_db
            beat_df.loc[i, ['harmonic', 'percussive']] = [treb_db, bass_db]
        beat_df.to_csv('track-data/{}-{}-beat.csv'.format(os.path.basename(track_path), idx), index=False)


def by_beat_track():
    y, track_seconds = load_track()
    tempo, beat_times = librosa.beat.beat_track(y=y, sr=sr, units='time')
    beat_df = pd.DataFrame(columns=['beat', 'harmonic', 'percussive', 'note', 'cum_secs'])
    beat_df['cum_secs'] = beat_times
    beat_df['beat'] = pd.Series(beat_times).diff()
    beat_df.loc[0, 'beat'] = beat_times[0]
    beat_df['note'] = shared.note_dict['1/{}'.format(notee)]
    beat_df['beat'] = beat_df['beat'] - beat_df['note']
    hz_db_harm, hz_db_perc = harm_vs_perc(y)
    num_per_hop = ceil(hz_db_perc.shape[1] / len(beat_df))
    for i in range(len(beat_times)):
        idx_start = i * num_per_hop
        treb_db = np.sum(hz_db_harm[:, idx_start:idx_start+num_per_hop])
        bass_db = np.sum(hz_db_perc[:, idx_start:idx_start+num_per_hop])
        tot_db = bass_db + treb_db
        if tot_db > 0:
            bass_db /= tot_db
            treb_db /= tot_db
        beat_df.loc[i, ['harmonic', 'percussive']] = [treb_db, bass_db]
    beat_df.to_csv('track-data/{}-monobeat.csv'.format(os.path.basename(track_path)), index=False)


def harm_vs_perc(y):
    D = librosa.stft(y, n_fft, hop_length)
    rp = np.median(np.abs(D))  # global reference power
    # remove noise by requiring that the horizontal and vertical filters differ by margin
    D_harmonic, D_percussive = librosa.decompose.hpss(D, margin=2)

    hz_db_harm = librosa.amplitude_to_db(abs(D_harmonic), ref=rp)
    hz_db_harm[hz_db_harm < 0] = 0
    print('hz_db_harm:', hz_db_harm.shape)
    hz_db_perc = librosa.amplitude_to_db(abs(D_percussive), ref=rp)
    hz_db_perc[hz_db_perc < 0] = 0
    print('\nhz_db_perc:', hz_db_perc.shape)
    return hz_db_harm, hz_db_perc


def stereo_signal():
    y, track_seconds = load_track(False)

    tempo_l, note = track_tempo(y[0])
    tempo_r, _ = track_tempo(y[1])

    hz_db_harm, hz_db_perc = harm_vs_perc(librosa.to_mono(y))

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
            df.loc[df.shape[0]] = [interval_beat, treb_db, bass_db, tempo_l, tempo_r, note]
    df['cum_secs'] = df['seconds'].cumsum()
    df.to_csv('track-data/{}-{}-stereo.csv'.format(notee, os.path.basename(track_path)), index=False)


def mono_signal():
    y, track_seconds = load_track()
    tempo, note = track_tempo(y)

    # get SFT
    hz_db = librosa.amplitude_to_db(abs(librosa.stft(y, n_fft, hop_length)))
    hz_db[hz_db < 0] = 0
    print(hz_db.shape)
    interval_beat, n_hops_interval = hops_per_interval(tempo, note, track_seconds, hz_db.shape[1])

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
            df.loc[df.shape[0]] = [interval_beat, treb_db, bass_db, tempo, note]

    df.to_csv('track-data/{}-mono.csv'.format(os.path.basename(track_path)), index=False)


if __name__ == '__main__':
    # mono_signal()
    # stereo_signal()
    by_beat_track()
    # by_beat_track_stereo()