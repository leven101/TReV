import librosa
import numpy as np

filename = '/Users/abby/work/TReV/music/audio-files/fg/BohemianRhapsody-Queen.mp3'
# filename = '/Users/abby/work/TReV/music/audio-files/heavy-beat_140bpm_C_major.wav'
y_stereo, sr = librosa.load(filename, mono=False)


print('Stereo is valid? ', librosa.util.valid_audio(y_stereo, mono=False))
print(y_stereo.shape)
# tempo, beat_times = librosa.beat.beat_track(y=y_stereo, sr=sr, units='time')
# print('Stereo tempo: {:.2f} BPM'.format(tempo))
# print(beat_times)

tempo, beat_times = librosa.beat.beat_track(y=y_stereo[0], sr=sr, units='time')
print('Stereo[0] tempo: {:.2f} BPM'.format(tempo), len(beat_times))
# print(beat_times)

tempo, beat_times = librosa.beat.beat_track(y=y_stereo[1], sr=sr, units='time')
print('Stereo[1] tempo: {:.2f} BPM'.format(tempo), len(beat_times))
# print(beat_times)

y_mono, sr = librosa.load(filename)
print('Mono')
print(y_mono.shape)
tempo, beat_times = librosa.beat.beat_track(y=y_mono, sr=sr, units='time')
print('Mono tempo: {:.2f} BPM'.format(tempo), len(beat_times))
# print(beat_times)