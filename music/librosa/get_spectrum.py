import librosa


path = '../audio-files/dt_16bars_102rap.wav'

x, sr = librosa.load(path, sr=44100)

hop_length = 512
n_fft = sr
X = librosa.stft(x, n_fft=n_fft, hop_length=hop_length)

print(X.shape)

S = librosa.amplitude_to_db(abs(X))

print(S.shape)

time = librosa.core.frames_to_time(S.shape[1], sr=sr, hop_length=hop_length)
print(time)
print(float(hop_length)/sr)
print(float(hop_length)/sr * S.shape[1])


# print(float(n_fft)/sr)