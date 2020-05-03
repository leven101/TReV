import numpy as np
import librosa.display
import matplotlib.pyplot as plt

path = '../audio-files/tones/100hz.mp3'

# sr/n_fft = hz buckets per fft
sr = 22050  # 44100
x, sr = librosa.load(path, sr=sr)

hop_length = 512  # how many frames per fft
# from spectrum_analysis.py n_fft = sr * (seconds / hops)
n_fft = 2205
X = librosa.stft(x, n_fft=n_fft, hop_length=hop_length)

print(X.shape)

S = librosa.amplitude_to_db(abs(X))

print(S.shape)


time = librosa.core.frames_to_time(S.shape[1], sr=sr, hop_length=hop_length)
print('time in seconds: ', time)
print('seconds per fft: ', n_fft/sr)
print('seconds per hop:', hop_length/sr)
print('Seconds per hop (2): ', time / S.shape[1])
print('time by (secs per hop * # hops): ', float(hop_length)/sr * S.shape[1])


plt.figure(figsize=(15, 5))
librosa.display.specshow(S, sr=sr, hop_length=hop_length, x_axis='time', y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.show()

hz_per_fft = int(sr / n_fft)
print('hz per fft bucket: ', hz_per_fft)
bass_range_hz = [60, 260]
bass_range_idx = [int(bass_range_hz[0]/hz_per_fft), int(bass_range_hz[1]/hz_per_fft)]
treble_range_hz = [2000, 4000]
treble_range_idx = [int(treble_range_hz[0]/hz_per_fft), int(treble_range_hz[1]/hz_per_fft)]

# for c in S.T:
#     print('S maxarg: ', c.argmax())
#     print('bass sum: ', np.sum(c[bass_range_idx[0]: bass_range_idx[1]]))
#     print('treble sum: ', np.sum(c[treble_range_idx[0]: treble_range_idx[1]]))

