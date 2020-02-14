import serial
import time
import os
import playsound
import threading


def clear_lights():
    ser.write(b'|')
    ser.flush()


def play_track(track_path):
    playsound.playsound(os.path.join(music_dirc, track_path))


def bass_example():
    clear_lights()
    ser.write(b'b')
    play_track('tones/300hz.mp3')
    clear_lights()


def treble_example():
    clear_lights()
    ser.write(b't')
    play_track('tones/1000hz.mp3')
    clear_lights()


def thread_example():
    clear_lights()
    # ser.write(b'd')
    t1 = threading.Thread(target=play_track,
                          args=('simple-hip-hop-beat_170bpm.wav',))
    t1.start()
    ser.write(b'q6|304')
    clear_lights()


def tempo_example():
    clear_lights()
    ser.write(b'q6|696')
    play_track('simple-hip-hop-beat_170bpm.wav')
    clear_lights()

    time.sleep(2)

    ser.write(b'q7|418')
    play_track('heavy-beat_140bpm_C_major.wav')
    clear_lights()

    time.sleep(2)

    ser.write(b'q14|882')
    play_track('beats-drum-loop.wav')
    clear_lights()

    # time.sleep(2)
    # ser.write(b'q37|580.5')
    # play_track('dt_16bars_102rap.wav')
    # clear_lights()


def bass_treble_demo():
    play_track('tones/300hz.mp3')
    time.sleep(1)
    play_track('tones/1000hz.mp3')
    time.sleep(2)

    bass_example()
    time.sleep(1)
    treble_example()


def tempo_demo():
    play_track('simple-hip-hop-beat_170bpm.wav')
    time.sleep(2)
    play_track('heavy-beat_140bpm_C_major.wav')
    time.sleep(2)
    play_track('beats-drum-loop.wav')
    time.sleep(2)
    tempo_example()


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    music_dirc = '/Users/abby/Documents/TREV/sound/'
    # thread_example()
    # ser.write(b'r')
    # bass_treble_demo()
    # clear_lights()
    tempo_example()
    ser.close()
