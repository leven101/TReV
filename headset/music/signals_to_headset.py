import time
import os
import serial
import pandas as pd

import headset.shared as shared
from multiprocessing import Process


rsl_brightness = 100
r = [0, 3]
c = [0, 2]
top_on = shared.cmd_template.format(shared.cmd_dict['top_on'], '{}', r[0], r[1], c[0], c[1])
top_off = '<11>'.encode()
bot_on = shared.cmd_template.format(shared.cmd_dict['bottom_on'], '{}', r[0], r[1], c[0], c[1])
bot_off = '<7>'.encode()


def top(conn, data, intensity, start):
    print('top', data['seconds'], intensity, data['tempo'], start)
    if intensity > 0:
        while time.time() - start < data['seconds']:
            if conn:
                conn.write(top_on.format(intensity).encode())
            time.sleep(data['note'])
            if conn:
                conn.write(top_off)
            time.sleep(data['tempo'])


def bottom(conn, data, intensity, start):
    print('bottom', data['seconds'], intensity, data['tempo'], start)
    if intensity > 0:
        while time.time() - start < data['seconds']:
            if conn:
                conn.write(bot_on.format(intensity).encode())
            time.sleep(data['note'])
            if conn:
                conn.write(bot_off)
            time.sleep(data['tempo'])


# first off tempo secs, then on note secs
def ready_state_light(conn, data, start):
    # beat on the off tempo
    print('rsl', data['seconds'], data['tempo'], start)
    while time.time() - start < data['seconds']:
        if conn:
            conn.write(shared.rsl_off_cmd)
        time.sleep(data['tempo'])
        if conn:
            conn.write(shared.rsl_on_cmd.format(rsl_brightness).encode())
        time.sleep(data['note'])


def run_track_program(df):
    start_time = time.time()
    for _, row in df.iterrows():
        row_start_time = time.time()
        procs = []
        top_intensity = int(round(row['top'] * shared.total_brightness))  # % of top
        bot_intensity = int(round(row['bottom'] * shared.total_brightness))  # % of bottom
        # print(top_intensity, bot_intensity, top_intensity + bot_intensity)
        s_t = time.time()
        procs.append(Process(target=top, args=(ser, row, top_intensity, s_t)))
        procs.append(Process(target=bottom, args=(ser, row, bot_intensity, s_t)))
        procs.append(Process(target=ready_state_light, args=(ser, row, s_t)))
        [p.start() for p in procs]
        [p.join() for p in procs]
        print('row', time.time()-row_start_time)
    print('run_track_program:', time.time()-start_time)
    if ser:
        ser.write(shared.all_off_cmd)


if __name__ == '__main__':
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/tones/100hz.wav'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/tones/1000hz.wav'
    in_audio_path = '/Users/abby/work/TReV/music/audio-files/dt_16bars_102rap.wav'
    in_signals_path = 'track-data/{}-mono.csv'.format(os.path.basename(in_audio_path))
    df = pd.read_csv(in_signals_path, dtype=float)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    shared.play_track(in_audio_path, False)
    print(top_on, bot_on, shared.rsl_on_cmd)
    run_track_program(df)
    if ser:
        ser.close()
