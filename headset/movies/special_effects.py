import serial
import time

from headset.shared import cmd_dict, all_off_cmd, \
    cmd_template

random_cmd = '<{} {}>'.format(cmd_dict['random'], 1).encode()


def gun_shot(ser, pos):
    # flash LED in center
    for i in range(4, 15):
        ser.write(cmd_template.format(cmd_dict[pos], i, 1, 1, 2, 2).encode())
        time.sleep(0.025)
        ser.write(all_off_cmd)
    for i in range(15, -1, -1):
        ser.write(cmd_template.format(cmd_dict[pos], i, 0, 2, 1, 3).encode())
        time.sleep(0.05)
    ser.write(all_off_cmd)


def explosion(ser, pos, secs):
    delay = (secs - 1) / 10
    for i in range(4, 15):
        ser.write(cmd_template.format(cmd_dict[pos], i, 0, 2, 1, 3).encode())
        time.sleep(delay)
        ser.write(all_off_cmd)
    ser.write(random_cmd)
    ser.write(all_off_cmd)


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    gun_shot(ser, 'left_bottom_on')
    # explosion(ser, 'left_bottom_on', 3)