'''
To try:
Boom - Tiesto
Friction - Imagine Dragons
new Rules - Dua Lipa
'''
import serial
import time
import threading

from headset.shared import cmd_dict, off_cmd, cmd_template, \
    note_dict, rsl_template, rsl_off_cmd, play_track

'''
Revolt - Malaa

open with "tickle"
mostly metronome

drum_rhythm()
beat up x 2 on bottom grid
pause
beat down x 2 on top grid


"scrape and scratch" 
 LEDS: single row from front to back and back to front. each LED blinks the whole way
 RSL: dimmest to brightest
'''


def revolt_drum_rhythm():
    r = [1, 2]
    c = [1, 2]
    seconds = 0.40
    note = note_dict['1/16']
    tempo = (seconds - (note*3)) / 3
    for i in range(0, 2):
        time.sleep(0.125)
        blink(r, c, cmd_dict['bottom_on'], seconds=seconds, tempo=tempo, note=note_dict['1/16'])
    time.sleep(1)


def scrape_n_scratch():
    threading.Thread(target=rsl_gradient).start()
    r = [1, 1]
    seconds = 0.25
    tempo = 0.001
    for i in range(0, 7):
        blink(r, [0, i], cmd_dict['top_on'], seconds=seconds, tempo=tempo)
    for i in range(5, -1, -1):
        blink(r, [0, i], cmd_dict['top_on'], seconds=seconds, tempo=tempo)


def rsl_gradient():
    for i in range(0, 256, 9):
        ser.write(rsl_on_cmd.format(i).encode())
        time.sleep(0.10)
    ser.write(rsl_off_cmd)


def blink(r, c, cmd_type, seconds=0.5, tempo=0.1, note=note_dict['1/4'], rsl=False):
    cmd = cmd_template.format(cmd_type, led_brightness, r[0], r[1], c[0], c[1])
    s = time.time()
    while time.time() - s < seconds:
        if rsl:
            ser.write(rsl_on_cmd.format(rsl_brightness).encode())
        time.sleep(tempo)
        ser.write(cmd.encode())
        if rsl:
            ser.write(rsl_off_cmd)
        time.sleep(note)
        ser.write(off_cmd)


def revolt_by_malaa():
    r = [1, 1]
    c = [3, 3]
    play_track('/Users/abby/Documents/TREV/sound/revolt.malaa.m4a')
    time.sleep(2)
    s = time.time()
    blink(r, c, cmd_dict['all_on'], 37, 0.58, rsl=True)
    time.sleep(0.5)
    while time.time() - s < 60:
        revolt_drum_rhythm()
    time.sleep(0.5)
    scrape_n_scratch()
    time.sleep(0.5)
    while time.time() - s < 68:
        revolt_drum_rhythm()
    scrape_n_scratch()
    while time.time() - s < 77:
        revolt_drum_rhythm()
    scrape_n_scratch()
    while time.time() - s < 87:
        revolt_drum_rhythm()
    scrape_n_scratch()
    blink(r, c, cmd_dict['all_on'], 20, 0.58, rsl=True)
    time.sleep(2)
    print(time.time() - s)


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    rsl_on_cmd = rsl_template.format(cmd_dict['ready_state_on'], '{}')
    led_brightness = 6
    rsl_brightness = 100
    revolt_by_malaa()
