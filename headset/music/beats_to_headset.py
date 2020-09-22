import time
import os
import serial
import pandas as pd
from multiprocessing import Process

import headset.shared as shared
tmpl = shared.cmd_template
r = [0, 2]
c = [1, 4]


def blink_single(pos, bght, row):
    print('blink_single', pos, bght)
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], bght, r[0], r[1], c[0], c[1]).encode())
    time.sleep(row['note'])
    ser.write(shared.off_cmd.format(shared.cmd_dict['{}_off'.format(pos)]).encode())
    time.sleep(row['beat'])


def rsl(row):
    ser.write(shared.rsl_on_cmd.format(100).encode())
    time.sleep(row['beat'])
    ser.write(shared.rsl_off_cmd)
    time.sleep(row['note'])


def blink_double(pos, bght, row):
    print('blink_double', pos, bght)
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], bght, r[0], r[1], c[0], c[1]).encode())
    time.sleep(row['note']/2)
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], round(bght/2), r[1]+1, r[1]+1, c[1]+1, c[1]+1).encode())
    time.sleep(row['note']/2)
    ser.write(shared.off_cmd.format(shared.cmd_dict['{}_off'.format(pos)]).encode())
    time.sleep(row['beat'])


def blink_double2(pos, bght, row):
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], bght, r[0], r[1], c[0], c[1]).encode())
    time.sleep(row['note']/2)
    ser.write(shared.off_cmd.format(shared.cmd_dict['{}_off'.format(pos)]).encode())
    time.sleep(row['beat'])
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], bght, r[0], r[1], c[0], c[1]).encode())
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], round(bght/2), r[1]+1, r[1]+1, c[1]+1, c[1]+1).encode())
    time.sleep(row['note']/2)
    ser.write(shared.off_cmd.format(shared.cmd_dict['{}_off'.format(pos)]).encode())


def blink_double3(pos, bght, row):
    ser.write(shared.off_cmd.format(shared.cmd_dict['{}_off'.format(pos)]).encode())
    time.sleep(row['beat'])
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], bght, r[0], r[1], c[0], c[1]).encode())
    time.sleep(row['note']/2)
    ser.write(tmpl.format(shared.cmd_dict['{}_on'.format(pos)], round(bght/2), r[1]+1, r[1]+1, c[1]+1, c[1]+1).encode())
    time.sleep(row['note']/2)
    ser.write(shared.off_cmd.format(shared.cmd_dict['{}_off'.format(pos)]).encode())


def play_side(df, func, side=None, offbeat=True):
    start_time = time.time()
    for _, row in df.iterrows():
        top_b = int(round(row['harmonic'] * shared.total_brightness))  # % of top
        bot_b = int(round(row['percussive'] * shared.total_brightness))  # % of bottom
        procs = []
        if side:
            procs.append(Process(target=func, args=('{}_top'.format(side), top_b, row)))
            procs.append(Process(target=func, args=('{}_bottom'.format(side), bot_b, row)))
        else:
            procs.append(Process(target=func, args=('top', top_b, row)))
            procs.append(Process(target=func, args=('bottom', bot_b, row)))
        if offbeat:
            procs.append(Process(target=rsl, args=(row, )))
        [p.start() for p in procs]
        [p.join() for p in procs]
        print('tot track time', time.time() - start_time)
    if side:
        ser.write(shared.off_cmd.format('{}_top_off'.format(side)).encode())
        ser.write(shared.off_cmd.format('{}_bottom_off'.format(side)).encode())
        if offbeat: ser.write(shared.rsl_off_cmd)
    else:
        ser.write(shared.all_off_cmd)


def play_mono(func=blink_single):
    in_signals_path = 'track-data/{}-monobeat.csv'.format(os.path.basename(in_audio_path))
    df = pd.read_csv(in_signals_path, dtype=float)
    shared.play_track(in_audio_path, False)
    play_side(df, func, None, True)


def play_stereo(func):
    in0 = 'track-data/{}-0-beat.csv'.format(os.path.basename(in_audio_path))
    df0 = pd.read_csv(in0, dtype=float)
    in1 = 'track-data/{}-1-beat.csv'.format(os.path.basename(in_audio_path))
    df1 = pd.read_csv(in1, dtype=float)
    shared.play_track(in_audio_path, False)
    procs = []
    procs.append(Process(target=play_side, args=(df0, func, 'left', True)))
    procs.append(Process(target=play_side, args=(df1, func, 'right', False)))
    [p.start() for p in procs]
    [p.join() for p in procs]


if __name__ == '__main__':
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/dontworry-behappy.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/creep-r3hab.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/01-DanceMonkey.mp3'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/bulls-rage.m4a'
    in_audio_path = '/Users/abby/work/TReV/music/audio-files/killing-rage.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/07-Friction.mp3'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/parallelLife-nekliff.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/theotherside-jasonderulo.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/BohemianRhapsody-Queen.mp3'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/trollz-nickiminaj.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/midnightblues-joebonamassa.m4a'
    ###
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/08-Ticks&Leeches.mp3'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/umbrella-rihanna.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/newrules-dualipa.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/morado-jBalvin.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/onemargarita-lukebryan.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/istandalone-godsmack.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/intheend-linkinpark.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/sexyback-justintimberlake.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/Name_of_the_Game_The_Crystal_Method.wav'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/non-stop.hamilton.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/Stay(2016Remaster).mp3'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/onedance-drake.m4a'
    # in_audio_path = '/Users/abby/work/TReV/music/audio-files/dirt-jayz.m4a'
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    if ser: ser.write(shared.all_off_cmd)
    if os.path.exists('track-data/{}-0-beat.csv'.format(os.path.basename(in_audio_path))):
        play_stereo(blink_double)
    else:
        play_mono(blink_double)
    if ser: ser.write(shared.all_off_cmd)