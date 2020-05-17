import time
import os
import serial
import pandas as pd

import headset.shared as shared
from multiprocessing import Process

rsl_brightness = 100
r = [1, 1]
c = [2, 3]
top_left_on = shared.cmd_template.format(shared.cmd_dict['left_top_on'], '{}', r[0], r[1], c[0], c[1])
top_right_on = shared.cmd_template.format(shared.cmd_dict['right_top_on'], '{}', r[0], r[1], c[0], c[1])
bot_left_on = shared.cmd_template.format(shared.cmd_dict['left_bottom_on'], '{}', r[0], r[1], c[0], c[1])
bot_right_on = shared.cmd_template.format(shared.cmd_dict['right_bottom_on'], '{}', r[0], r[1], c[0], c[1])
top_left_off = shared.off_cmd.format(shared.cmd_dict['left_top_off']).encode()
top_right_off = shared.off_cmd.format(shared.cmd_dict['right_top_off']).encode()
bot_left_off = shared.off_cmd.format(shared.cmd_dict['left_bottom_off']).encode()
bot_right_off = shared.off_cmd.format(shared.cmd_dict['right_bottom_off']).encode()


def top_left(conn, data, intensity, start):
    print('top_left', data['seconds'], intensity, data['tempo_left'], start)
    if intensity > 0:
        while True:
            # if we have time left to play the note
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(top_left_on.format(intensity).encode())
                time.sleep(data['note'])
            else:
                break
            if conn:
                conn.write(top_left_off)
            if time.time() - start < data['seconds'] - data['tempo_left']:
                time.sleep(data['tempo_left'])
            else:
                break


def top_right(conn, data, intensity, start):
    print('top_right', data['seconds'], intensity, data['tempo_left'], start)
    if intensity > 0:
        while True:
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(top_right_on.format(intensity).encode())
                time.sleep(data['note'])
            else:
                break
            if conn:
                conn.write(top_right_off)
            if time.time() - start < data['seconds'] - data['tempo_right']:
                time.sleep(data['tempo_right'])
            else:
                break


def bottom_left(conn, data, intensity, start):
    print('bottom_left', data['seconds'], intensity, data['tempo_right'], start)
    if intensity > 0:
        while True:
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(bot_left_on.format(intensity).encode())
                time.sleep(data['note'])
            else:
                break
            if conn:
                conn.write(bot_left_off)
            if time.time() - start < data['seconds'] - data['tempo_left']:
                time.sleep(data['tempo_left'])
            else:
                break


def bottom_right(conn, data, intensity, start):
    print('bottom_right', data['seconds'], intensity, data['tempo_right'], start)
    if intensity > 0:
        while True:
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(bot_right_on.format(intensity).encode())
                time.sleep(data['note'])
            else:
                break
            if conn:
                conn.write(bot_right_off)
            if time.time() - start < data['seconds'] - data['tempo_right']:
                time.sleep(data['tempo_right'])
            else:
                break


# first off tempo secs, then on note secs
def ready_state_light(conn, data, start):
    # beat on the off tempo
    print('rsl', data['seconds'], data['tempo_left'], start)
    while True:
        if time.time() - start < data['seconds'] - data['tempo_left']:
            if conn:
                conn.write(shared.rsl_off_cmd)
            time.sleep(data['tempo_left'])
        else:
            break
        if conn:
            conn.write(shared.rsl_on_cmd.format(rsl_brightness).encode())
        if time.time() - start < data['seconds'] - data['note']:
            time.sleep(data['note'])
        else:
            break


def run_track_program():
    shared.play_track(in_audio_path, True)
    start_time = time.time()
    for _, row in df.iterrows():
        row_start_time = time.time()
        top_intensity = round(row['harmonic'] * shared.total_brightness)  # % of top
        bot_intensity = round(row['percussive'] * shared.total_brightness)  # % of bottom
        # print(top_intensity, bot_intensity, top_intensity + bot_intensity)
        s_t = time.time()
        top_left(ser, row, top_intensity, s_t)
        top_right(ser, row, top_intensity, s_t)
        bottom_left(ser, row, bot_intensity, s_t)
        bottom_right(ser, row, bot_intensity, s_t)
        ready_state_light(ser, row, s_t)
        print('row', time.time()-row_start_time)
    print('run_track_program:', time.time()-start_time)
    if ser:
        ser.write(shared.all_off_cmd)


if __name__ == '__main__':
    in_audio_path = '/Users/abby/work/TReV/music/audio-files/b5.m4a'
    in_signals_path = 'track-data/stereo-track-data.csv'
    # in_signals_path = 'track-data/{}-track-data.csv'.format(os.path.basename(in_audio_path))
    df = pd.read_csv(in_signals_path, dtype=float)
    ser = None # serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    run_track_program()
    if ser:
        ser.close()
