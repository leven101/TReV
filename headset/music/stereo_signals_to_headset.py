import time
import os
import serial
import pandas as pd

import headset.shared as shared
from multiprocessing import Process

rsl_brightness = 200
r = [2, 3]
c = [1, 2]
top_left_on = shared.cmd_template.format(shared.cmd_dict['left_top_on'], '{}', r[0], r[1], c[0], c[1])
top_left_on_2 = shared.cmd_template.format(shared.cmd_dict['left_top_on'], '{}', r[0]+1, r[1]+1, c[0]+1, c[1]+1)
top_right_on = shared.cmd_template.format(shared.cmd_dict['right_top_on'], '{}', r[0], r[1], c[0], c[1])
top_right_on_2 = shared.cmd_template.format(shared.cmd_dict['right_top_on'], '{}', r[0]+1, r[1]+1, c[0]+1, c[1]+1)
bot_left_on = shared.cmd_template.format(shared.cmd_dict['left_bottom_on'], '{}', r[0], r[1], c[0], c[1])
bot_left_on_2 = shared.cmd_template.format(shared.cmd_dict['left_bottom_on'], '{}', r[0]+1, r[1]+1, c[0]+1, c[1]+1)
bot_right_on = shared.cmd_template.format(shared.cmd_dict['right_bottom_on'], '{}', r[0], r[1], c[0], c[1])
bot_right_on_2 = shared.cmd_template.format(shared.cmd_dict['right_bottom_on'], '{}', r[0]+1, r[1]+1, c[0]+1, c[1]+1)
top_left_off = shared.off_cmd.format(shared.cmd_dict['left_top_off']).encode()
top_right_off = shared.off_cmd.format(shared.cmd_dict['right_top_off']).encode()
bot_left_off = shared.off_cmd.format(shared.cmd_dict['left_bottom_off']).encode()
bot_right_off = shared.off_cmd.format(shared.cmd_dict['right_bottom_off']).encode()


def top_left(conn, data, intensity, start):
    print('top_left', data['seconds'], intensity, data['tempo_left'], start)
    if intensity > 0 and data['tempo_left'] > 0:
        while True:
            # if we have time left to play the note
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(top_left_on.format(intensity).encode())
                    time.sleep(data['note']/2)
                    conn.write(top_left_on_2.format(intensity).encode())
                time.sleep(data['note']/2)
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break
            if conn:
                conn.write(top_left_off)
            if time.time() - start < data['seconds'] - data['tempo_left']:
                time.sleep(data['tempo_left'])
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break


def top_right(conn, data, intensity, start):
    print('top_right', data['seconds'], intensity, data['tempo_left'], start)
    if intensity > 0 and data['tempo_right'] > 0:
        while True:
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(top_right_on.format(intensity).encode())
                    time.sleep(data['note']/2)
                    conn.write(top_right_on_2.format(intensity).encode())
                time.sleep(data['note']/2)
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break
            if conn:
                conn.write(top_right_off)
            if time.time() - start < data['seconds'] - data['tempo_right']:
                time.sleep(data['tempo_right'])
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break


def bottom_left(conn, data, intensity, start):
    print('bottom_left', data['seconds'], intensity, data['tempo_right'], start)
    if intensity > 0 and data['tempo_left'] > 0:
        while True:
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(bot_left_on.format(intensity).encode())
                    time.sleep(data['note']/2)
                    conn.write(bot_left_on_2.format(intensity).encode())
                time.sleep(data['note']/2)
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break
            if conn:
                conn.write(bot_left_off)
            if time.time() - start < data['seconds'] - data['tempo_left']:
                time.sleep(data['tempo_left'])
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break


def bottom_right(conn, data, intensity, start):
    print('bottom_right', data['seconds'], intensity, data['tempo_right'], start)
    if intensity > 0 and data['tempo_right'] > 0:
        while True:
            if time.time() - start < data['seconds'] - data['note']:
                if conn:
                    conn.write(bot_right_on.format(intensity).encode())
                    time.sleep(data['note']/2)
                    conn.write(bot_right_on_2.format(intensity).encode())
                time.sleep(data['note']/2)
            else:
                time.sleep(data['seconds'] - (time.time() - start))
                break
            if conn:
                conn.write(bot_right_off)
            if time.time() - start < data['seconds'] - data['tempo_right']:
                time.sleep(data['tempo_right'])
            else:
                time.sleep(data['seconds'] - (time.time() - start))
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
            time.sleep(data['seconds'] - (time.time() - start))
            break
        if conn:
            conn.write(shared.rsl_on_cmd.format(rsl_brightness).encode())
        if time.time() - start < data['seconds'] - data['note']:
            time.sleep(data['note'])
        else:
            time.sleep(data['seconds'] - (time.time() - start))
            break


def run_track_program(df, ser):
    start_time = time.time()
    for _, row in df.iterrows():
        row_start_time = time.time()
        top_intensity = int(round(row['harmonic'] * shared.total_brightness))  # % of top
        bot_intensity = int(round(row['percussive'] * shared.total_brightness))  # % of bottom
        # print(top_intensity, bot_intensity, top_intensity + bot_intensity)
        procs = []
        s_t = time.time()
        procs.append(Process(target=top_left, args=(ser, row, top_intensity, s_t)))
        procs.append(Process(target=top_right, args=(ser, row, top_intensity, s_t)))
        procs.append(Process(target=bottom_left, args=(ser, row, bot_intensity, s_t)))
        procs.append(Process(target=bottom_right, args=(ser, row, bot_intensity, s_t)))
        procs.append(Process(target=ready_state_light, args=(ser, row, s_t)))
        [p.start() for p in procs]
        [p.join() for p in procs]
        print('row time', time.time()-row_start_time)
        print('tot track time', time.time() - start_time)
    print('run_track_program:', time.time()-start_time)
    if ser:
        ser.write(shared.all_off_cmd)


# in_audio_path = '/Users/abby/work/TReV/music/audio-files/fg/sinefromabove-ladygaga.m4a'
in_audio_path = '/Users/abby/work/TReV/music/audio-files/fg/morado-jBalvin.m4a'
# in_audio_path = '/Users/abby/work/TReV/music/audio-files/fg/pessimist-paramore.m4a'

if __name__ == '__main__':
    in_signals_path = 'track-data/{}-stereo.csv'.format(os.path.basename(in_audio_path))
    # in_signals_path = 'track-data/tmp.m4a-stereo.csv'
    df = pd.read_csv(in_signals_path, dtype=float)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    if ser: ser.write(shared.all_off_cmd)
    shared.play_track(in_audio_path, True)
    time.sleep(2)
    run_track_program(df, ser)
    if ser:
        ser.close()
