import pyglet
import librosa

oggfile = librosa.util.example_audio_file()
song = pyglet.media.load("audio-files/dt_16bars_102rap.wav")
song.play()
pyglet.app.run()
pyglet.app.