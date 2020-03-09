import serial
import time
import threading
import playsound


def play_track():
    t1 = threading.Thread(target=playsound.playsound, daemon=True,
                          args=('/Users/abby/Documents/TREV/sound/b5.m4a',))
    t1.start()
    # playsound.playsound('/Users/abby/Documents/TREV/sound/b5.m4a')


def bottom_left_right_left(num_times, delay):
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start+2, c_start, c_start+2)
    left_cmd = cmd_dict['cmd_start'] + cmd_dict['left_bottom_on'] + lcl_led_cmd + cmd_dict['cmd_end']
    right_cmd = cmd_dict['cmd_start'] + cmd_dict['right_bottom_on'] + lcl_led_cmd + cmd_dict['cmd_end']

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


def short_short_short_long(num_times):
    lcl_led_cmd = leds_cmd.format(min(brightness*2, 14), r_start, r_start+2, c_start, c_start+2)
    top_cmd = cmd_dict['cmd_start'] + cmd_dict['top_on'] + lcl_led_cmd + cmd_dict['cmd_end']
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start+2, c_start, c_start+2)
    bot_cmd = cmd_dict['cmd_start'] + cmd_dict['bottom_on'] + lcl_led_cmd + cmd_dict['cmd_end']

    for i in range(0, num_times):
        ser.write(top_cmd.encode())
        time.sleep(0.4)
        ser.write(off_cmd)

        rsl_cmd = cmd_dict['cmd_start'] + cmd_dict['ready_state_on'] + ' 200' + cmd_dict['cmd_end']
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


def short_short_long():
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start + 3, c_start, c_start + 3)
    on_cmd = cmd_dict['cmd_start'] + cmd_dict['all_on'] + lcl_led_cmd + cmd_dict['cmd_end']

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


def beat_metronome(seconds):
    lcl_led_cmd = leds_cmd.format(brightness, r_start, r_start + 1, c_start, c_start + 1)
    beat_cmd = cmd_dict['cmd_start'] + cmd_dict['all_on'] + lcl_led_cmd + cmd_dict['cmd_end']
    rsl_on_cmd = cmd_dict['cmd_start'] + cmd_dict['ready_state_on'] + ' 200' + cmd_dict['cmd_end']
    rsl_off_cmd = cmd_dict['cmd_start'] + cmd_dict['ready_state_off'] + cmd_dict['cmd_end']
    start_time = time.time()
    while time.time() - start_time < seconds:
        ser.write(beat_cmd.encode())
        ser.write(rsl_off_cmd.encode())
        time.sleep(0.25)
        ser.write(off_cmd)
        ser.write(rsl_on_cmd.encode())
        time.sleep(0.325)
    ser.write(off_cmd)


if __name__ == '__main__':
    cmd_dict = {'cmd_start': '<', 'cmd_end': '>', 'all_off': '0', 'all_on': '1',
                'ready_state_on': '2', 'ready_state_off': '3', 'bottom_on': '4',
                'right_bottom_on': '5', 'left_bottom_on': '6', 'bottom_off': '7',
                'top_on': '8', 'right_top_on': '9', 'left_top_on': '10', 'top_off': '11',
                'random': '12'}
    # cmd code, brightness, row start, row end, col start, col end
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    r_start = 0
    c_start = 1
    brightness = 7
    off_cmd = (cmd_dict['cmd_start'] + cmd_dict['all_off'] + cmd_dict['cmd_end']).encode()
    ser.write(off_cmd)
    leds_cmd = ' {} {} {} {} {}'

    play_track()
    time.sleep(0.6)
    start_time = time.time()
    short_short_short_long(2)
    ser.write(off_cmd)
    bottom_left_right_left(2, 0.125)
    bottom_left_right_left(1, 0.075)

    short_short_long()
    ser.write(off_cmd)
    time.sleep(1.2)
    short_short_short_long(1)
    ser.write(off_cmd)
    # validated above this
    short_short_short_long(1)
    beat_metronome(5)
    print(time.time() - start_time)

