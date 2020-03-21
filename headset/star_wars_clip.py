import serial
import time
import random

from headset.shared import cmd_dict, leds_cmd, off_cmd, cmd_template

start_choices = ['right_bottom_on', 'right_top_on', 'left_bottom_on', 'left_top_on']
row_choices = [0, 1]
col_choices = [0, 1, 2, 3, 4, 5, 6]


def brightness_gradient_up(cmd_shell):
    for i in range(0, 15, 5):
        cmd = cmd_shell.format(i)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.1)
    ser.write(off_cmd)


def brightness_gradient_down(cmd_shell):
    for i in range(14, -1, -5):
        cmd = cmd_shell.format(i)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.1)
    ser.write(off_cmd)


def select_start_end_coordinates():
    start_grid = random.choice(start_choices)
    if 'right' in start_grid:
        end_grid = random.choice(start_choices[2:])
    else:
        end_grid = random.choice(start_choices[:2])
    r = random.choice(row_choices)
    c = random.choice(col_choices)
    start_cmd = cmd_template.format(cmd_dict[start_grid], '{}', r, r+1, c, c)
    end_cmd = cmd_template.format(cmd_dict[end_grid], '{}', r, r+1, c, c)
    return start_cmd, end_cmd


def single_laser_beam():
    fire_cmd, hit_cmd = select_start_end_coordinates()
    print(fire_cmd, hit_cmd)
    brightness_gradient_up(fire_cmd)
    brightness_gradient_down(hit_cmd)


def ship_takeoff():
    # bottom right LED grid goes on (low to high rows/intensity) when blue lights go (3 seconds)
    # left LED grid goes (low to high row)
    brightness = 0
    col = 1
    print(cmd_template)
    tmp_cmd = cmd_template.format(cmd_dict['right_bottom_on'], '{}', '{}', '{}', col, col+2)
    for i in range(3, -1, -1):
        brightness += 3
        cmd = tmp_cmd.format(brightness, i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.375)

    tmp_cmd = cmd_template.format(cmd_dict['right_top_on'], brightness, '{}', '{}', col, col + 2)
    for i in range(0, 4):
        cmd = tmp_cmd.format(i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.375)
    ser.write(off_cmd)

    tmp_cmd = cmd_template.format(cmd_dict['left_bottom_on'], brightness, '{}', '{}', col, col + 2)
    for i in range(3, -1, -1):
        cmd = tmp_cmd.format(i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.25)

    tmp_cmd = cmd_template.format(cmd_dict['left_top_on'], brightness, '{}', '{}', col, col + 2)
    for i in range(0, 4):
        cmd = tmp_cmd.format(i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.25)
    ser.write(off_cmd)


def irritate_noise():
    cmd = cmd_template.format(cmd_dict['left_top_on'], 7, 2, 4, '{}', '{}')
    s = time.time()
    while time.time() - s < 2:
        ser.write(cmd.format(0, 1).encode())
        time.sleep(0.2)
        ser.write(off_cmd)
        ser.write(cmd.format(1, 2).encode())
        time.sleep(0.2)
        ser.write(off_cmd)


def warp_speed_effect():
    # go from back column to front column with all rows lit
    cmd = cmd_template.format(cmd_dict['all_on'], 7, 0, 3, '{}', '{}')
    for i in range(6, -1, -1):
        print(cmd.format(i, i+1))
        ser.write(cmd.format(i, i+1).encode())
        time.sleep(0.4)

    delay = 0.025
    ser.write(off_cmd)
    ser.write(cmd.format(1, 5).encode())
    time.sleep(delay)

    ser.write(off_cmd)
    ser.write(cmd.format(2, 4).encode())
    time.sleep(delay)

    ser.write(off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 7, 0, 2, 2, 4).encode())
    time.sleep(delay)

    ser.write(off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 7, 0, 2, 2, 3).encode())
    time.sleep(delay)

    ser.write(off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 7, 0, 1, 2, 3).encode())
    time.sleep(delay)

    ser.write(off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 7, 0, 0, 2, 2).encode())
    time.sleep(delay)

    ser.write(off_cmd)


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    s = time.time()
    # irritate_noise()
    # ship_takeoff()
    # ser.write(off_cmd)
    warp_speed_effect()
    # while time.time() - s < 8:
    #     single_laser_beam()

    ser.close()



















