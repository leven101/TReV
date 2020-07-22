import serial
import time

from headset.shared import cmd_dict, all_off_cmd, \
    cmd_template, off_cmd

random_cmd = '<{} {}>'.format(cmd_dict['random'], 1).encode()


def gun_shot(ser, pos):
    # flash LED in center
    for i in range(4, 15):
        ser.write(cmd_template.format(cmd_dict[pos], i, 1, 1, 2, 2).encode())
        time.sleep(0.025)
        ser.write(all_off_cmd)
    for i in range(15, -1, -1):
        ser.write(cmd_template.format(cmd_dict[pos], i, 0, 2, 1, 3).encode())
        time.sleep(0.005)
    ser.write(all_off_cmd)


def explosion(ser, pos, secs):
    delay = (secs - 1) / 10
    for i in range(4, 15):
        ser.write(cmd_template.format(cmd_dict[pos], i, 0, 2, 1, 3).encode())
        time.sleep(delay)
        ser.write(all_off_cmd)
    ser.write(random_cmd)
    ser.write(all_off_cmd)


def circle_of_light(ser, secs_one, secs_tot, b=8):
    sec_per_col = secs_one / 14  # 14 columns
    start = time.time()
    while time.time() - start < secs_tot:
        for i in range(7):
            ser.write(cmd_template.format(cmd_dict['right_top_on'], b, 0, 3, i, i).encode())
            ser.write(cmd_template.format(cmd_dict['right_bottom_on'], b, 0, 3, i, i).encode())
            time.sleep(sec_per_col)
            ser.write(all_off_cmd)
        for i in range(7):
            ser.write(cmd_template.format(cmd_dict['left_top_on'], b, 0, 3, i, i).encode())
            ser.write(cmd_template.format(cmd_dict['left_bottom_on'], b, 0, 3, i, i).encode())
            time.sleep(sec_per_col)
            ser.write(all_off_cmd)


def gradient_up(ser, secs, b):
    sec_per_row = secs / 8
    for i in range(3, -1, -1):
        b += 1 if i % 2 == 0 else 0
        ser.write(cmd_template.format(cmd_dict['right_bottom_on'], b, i, 3, 0, 6).encode())
        ser.write(cmd_template.format(cmd_dict['left_bottom_on'], b, i, 3, 0, 6).encode())
        time.sleep(sec_per_row)
    for i in range(4):
        b += 1 if i % 2 == 0 else 0
        ser.write(cmd_template.format(cmd_dict['right_top_on'], b, 0, i, 0, 6).encode())
        ser.write(cmd_template.format(cmd_dict['left_top_on'], b, 0, i, 0, 6).encode())
        time.sleep(sec_per_row)
    ser.write(all_off_cmd)


def gradient_down(ser, secs, b):
    sec_per_row = secs / 8
    ser.write(cmd_template.format(cmd_dict['all_on'], b, 0, 3, 0, 6).encode())
    for i in range(2, -1, -1):
        b -= 1 if i % 2 == 0 else 0
        ser.write(off_cmd.format(cmd_dict['top_off']).encode())
        ser.write(cmd_template.format(cmd_dict['top_on'], b, 0, i, 0, 6).encode())
        time.sleep(sec_per_row)
    ser.write(off_cmd.format(cmd_dict['top_off']).encode())
    for i in range(4):
        b -= 1 if i % 2 == 0 else 0
        ser.write(off_cmd.format(cmd_dict['bottom_off']).encode())
        ser.write(cmd_template.format(cmd_dict['bottom_on'], b, i, 3, 0, 6).encode())
        time.sleep(sec_per_row)
    ser.write(all_off_cmd)


def sunrise(ser, secs, b=2):
    return gradient_up(ser, secs, b)


def sunset(ser, secs, b=10):
    gradient_down(ser, secs, b)


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    # ser.write(cmd_template.format(cmd_dict['bottom_on'], 10, 4, 4, 0, 6).encode())
    # explosion(ser, 'top_on', 3)
    # gun_shot(ser, 'left_bottom_on')
    # sunrise(ser, 5)
    # time.sleep(2)
    # sunset(ser, 5)