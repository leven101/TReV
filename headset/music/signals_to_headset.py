import time
import os
import serial
import pandas as pd

import headset.shared as shared
from multiprocessing import Process


rsl_brightness = 100
note = shared.note_dict['1/4']  # how long the light should be on for each beat
r = [1, 1]
c = [2, 2]
top_on = shared.cmd_template.format(shared.cmd_dict['top_on'], '{}', r[0], r[1], c[0], c[1])
top_off = '<11>'.encode()
bot_on = shared.cmd_template.format(shared.cmd_dict['bottom_on'], '{}', r[0], r[1], c[0], c[1])
bot_off = '<7>'.encode()


def top(conn, seconds, intensity, tempo, start):
    print('top', seconds, intensity, tempo, start)
    if intensity > 0:
        while time.time() - start < seconds:
            conn.write(top_on.format(intensity).encode())
            time.sleep(note)
            conn.write(top_off)
            time.sleep(tempo)


def bottom(conn, seconds, intensity, tempo, start):
    print('bottom', seconds, intensity, tempo, start)
    if intensity > 0:
        while time.time() - start < seconds:
            print(bot_on.format(intensity))
            conn.write(bot_on.format(intensity).encode())
            time.sleep(note)
            conn.write(bot_off)
            time.sleep(tempo)


# first off tempo secs, then on note secs
def ready_state_light(conn, seconds, tempo, start):
    # beat on the off tempo
    print('rsl', seconds, tempo, start)
    while time.time() - start < seconds:
        conn.write(shared.rsl_off_cmd)
        time.sleep(tempo)
        conn.write(shared.rsl_on_cmd.format(rsl_brightness).encode())
        time.sleep(note)


def get_tempo(bpm):
    # tempo: how many times the lights blink a second
    # note: how long each light is on for
    if bpm > 0:
        tempo = shared.beats_per_second(bpm)
        return tempo - note
    else:
        return 0


def run_track_program():
    shared.play_track(in_audio_path, False)
    for _, row in df.iterrows():
        procs = []
        tempo = get_tempo(row['tempo'])
        top_intensity = row['top'] * shared.total_brightness  # % of top
        bot_intensity = row['bottom'] * shared.total_brightness  # % of bottom
        print(top_intensity, bot_intensity, top_intensity + bot_intensity)
        s_t = time.time()
        procs.append(Process(target=top, args=(ser, row['seconds'], top_intensity, tempo, s_t)))
        procs.append(Process(target=bottom, args=(ser, row['seconds'], bot_intensity, tempo, s_t)))
        procs.append(Process(target=ready_state_light, args=(ser, row['seconds'], tempo, s_t)))
        [p.start() for p in procs]
        [p.join() for p in procs]
    ser.write(shared.off_cmd)


if __name__ == '__main__':
    in_audio_path = '/Users/abby/work/TReV/music/audio-files/tones/100hz.mp3'
    in_signals_path = 'track-data/{}-track-data.csv'.format(os.path.basename(in_audio_path))
    df = pd.read_csv(in_signals_path, dtype=float)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    print(top_on, bot_on, shared.rsl_on_cmd)
    run_track_program()
    ser.close()
