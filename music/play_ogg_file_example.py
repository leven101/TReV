import pyglet
import librosa

oggfile = librosa.util.example_audio_file()
song = pyglet.media.load(oggfile)
song.play()
pyglet.app.run()