import librosa

path = '../audio-files/dt_16bars_102rap.wav'

x, sr = librosa.load(path)

hop_length = 512
n_fft = 2048
X = librosa.stft(x, n_fft=n_fft, hop_length=hop_length)

print(X.shape)