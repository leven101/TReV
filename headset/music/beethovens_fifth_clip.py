import serial
import time

from headset.shared import cmd_dict, play_track


def bottom_left_right_left_right(num_times, delay):
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start+1, c_start, c_start+1)
    left_cmd = '<' + cmd_dict['left_bottom_on'] + lcl_led_cmd + '>'
    right_cmd = '<' + cmd_dict['right_bottom_on'] + lcl_led_cmd + '>'

    for _ in range(0, num_times):
        for _ in range(0, 2):
            for i in range(0, 2):
                ser.write(left_cmd.encode())
                time.sleep(delay)
                ser.write(off_cmd)
                time.sleep(delay)

            for i in range(0, 2):
                ser.write(right_cmd.encode())
                time.sleep(delay)
                ser.write(off_cmd)
                time.sleep(delay)

        time.sleep(0.75)


def top_short_rsl_short_right_short_top_long(num_times):
    lcl_led_cmd = leds_cmd.format(min(brightness*2, 14), r_start, r_start+1, c_start, c_start+1)
    top_cmd = '<' + cmd_dict['top_on'] + lcl_led_cmd + '>'
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start+1, c_start, c_start+1)
    bot_cmd = '<' + cmd_dict['bottom_on'] + lcl_led_cmd + '>'

    for i in range(0, num_times):
        ser.write(top_cmd.encode())
        time.sleep(0.4)
        ser.write(off_cmd)

        rsl_cmd = '<' + cmd_dict['ready_state_on'] + ' 200' + '>'
        ser.write(rsl_cmd.encode())
        time.sleep(0.4)
        ser.write(off_cmd)

        ser.write(bot_cmd.encode())
        time.sleep(0.4)
        ser.write(off_cmd)

        for i in range(0, 10):
            ser.write(top_cmd.encode())
            time.sleep(0.09)
            ser.write(off_cmd)
            time.sleep(0.09)

        time.sleep(0.4)


def all_short_short_long():
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start+2, c_start, c_start+2)
    on_cmd = '<' + cmd_dict['all_on'] + lcl_led_cmd + '>'

    ser.write(on_cmd.encode())
    time.sleep(0.5)
    ser.write(off_cmd)
    time.sleep(0.5)

    ser.write(on_cmd.encode())
    time.sleep(0.5)
    ser.write(off_cmd)
    time.sleep(0.5)

    for i in range(0, 5):
        ser.write(on_cmd.encode())
        time.sleep(0.1)
        ser.write(off_cmd)
        time.sleep(0.1)


def beat_metronome(seconds, tempo=0.326, note=0.50, soft=False):
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start, c_start, c_start)
    beat_cmd = '<' + cmd_dict['all_on'] + lcl_led_cmd + '>'
    rsl_on_cmd = '<' + cmd_dict['ready_state_on'] + ' 200' + '>'
    rsl_off_cmd = '<' + cmd_dict['ready_state_off'] + '>'
    start_time = time.time()
    tempo *= 2 if soft else 1
    while time.time() - start_time < seconds:
        ser.write(rsl_off_cmd.encode())
        ser.write(beat_cmd.encode())
        time.sleep(note)
        ser.write(off_cmd)
        ser.write(rsl_on_cmd.encode())
        time.sleep(tempo)
    ser.write(off_cmd)


def flash_all(seconds=0.5):
    lcl_led_cmd = leds_cmd.format(brightness, 0, 4, 0, 7)
    flash_cmd = '<' + cmd_dict['all_on'] + lcl_led_cmd + '>'
    # print(flash_cmd)
    ser.write(flash_cmd.encode())
    time.sleep(seconds)
    ser.write(off_cmd)


def rsl_bright_to_dim():
    ready_state_cmd = '<' + cmd_dict['ready_state_on'] + ' {}' + '>'
    for i in range(256, 0, -9):
        ser.write(ready_state_cmd.format(i).encode())
        time.sleep(0.1)
    ser.write(off_cmd)


def top_to_bottom_flash(num_times):
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start+1, c_start, c_start+1)
    top_cmd = '<' + cmd_dict['top_on'] + lcl_led_cmd + '>'
    bot_cmd = '<' + cmd_dict['bottom_on'] + lcl_led_cmd + '>'
    for i in range(0, num_times):
        ser.write(top_cmd.encode())
        time.sleep(0.5)
        ser.write(off_cmd)
        time.sleep(0.05)
        ser.write(bot_cmd.encode())
        time.sleep(0.5)
        ser.write(off_cmd)
        time.sleep(0.05)


if __name__ == '__main__':
    # <cmd code, brightness, row start, row end, col start, col end>
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    r_start = 0
    c_start = 1
    brightness = 12
    off_cmd = ('<' + cmd_dict['all_off'] + '>').encode()
    ser.write(off_cmd)
    leds_cmd = ' {} {} {} {} {}'

    play_track('/Users/abby/work/TReV/music/audio-files/b5.m4a')
    time.sleep(3)
    start_time = time.time()
    top_short_rsl_short_right_short_top_long(2)
    ser.write(off_cmd)
    bottom_left_right_left_right(2, 0.125)
    bottom_left_right_left_right(1, 0.075)
    all_short_short_long()
    ser.write(off_cmd)
    time.sleep(1.2)
    top_short_rsl_short_right_short_top_long(1)
    ser.write(off_cmd)

    bottom_left_right_left_right(2, 0.125)
    beat_metronome(15)
    ser.write(off_cmd)
    time.sleep(0.5)
    flash_all()
    beat_metronome(17.5, soft=True)
    beat_metronome(10, note=0.25)
    ser.write(off_cmd)
    bottom_left_right_left_right(1, 0.125)
    beat_metronome(2)
    bottom_left_right_left_right(1, 0.125)
    beat_metronome(2)
    top_short_rsl_short_right_short_top_long(3)
    beat_metronome(10, soft=True)
    top_to_bottom_flash(3)
    rsl_bright_to_dim()
    flash_all(0.2)
    time.sleep(2)
    ser.close()
    print(time.time() - start_time)

