import serial
import time
import random

from headset.shared import cmd_dict, all_off_cmd, \
    cmd_template, rsl_on_cmd, rsl_off_cmd, flash_all, play_clip

start_choices = ['right_bottom_on', 'right_top_on', 'left_bottom_on', 'left_top_on']
row_choices = [0, 1]
col_choices = [0, 1, 2, 3, 4, 5, 6]

'''TODO for Hans Solo face
- add surprise RSL gradient  at 1:14
- happy for 2:25 - 2:26
'''


def brightness_gradient_up(cmd_shell, speed):
    for i in range(0, 15, 5):
        cmd = cmd_shell.format(i)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(speed)
    ser.write(all_off_cmd)


def brightness_gradient_down(cmd_shell, speed):
    for i in range(14, -1, -5):
        cmd = cmd_shell.format(i)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(speed)
    ser.write(all_off_cmd)


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


def single_laser_beam(speed=0.1):
    fire_cmd, hit_cmd = select_start_end_coordinates()
    print(fire_cmd, hit_cmd)
    brightness_gradient_up(fire_cmd, speed)
    brightness_gradient_down(hit_cmd, speed)


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
        time.sleep(0.5)

    tmp_cmd = cmd_template.format(cmd_dict['right_top_on'], brightness, '{}', '{}', col, col + 2)
    for i in range(0, 4):
        cmd = tmp_cmd.format(i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.5)
    ser.write(all_off_cmd)

    time.sleep(0.5)

    tmp_cmd = cmd_template.format(cmd_dict['left_bottom_on'], brightness, '{}', '{}', col, col + 2)
    for i in range(3, -1, -1):
        cmd = tmp_cmd.format(i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.5)

    tmp_cmd = cmd_template.format(cmd_dict['left_top_on'], brightness, '{}', '{}', col, col + 2)
    for i in range(0, 4):
        cmd = tmp_cmd.format(i, i+1)
        print(cmd)
        ser.write(cmd.encode())
        time.sleep(0.5)
    ser.write(all_off_cmd)


def irritate_noise():
    # for 0:23 - 0:25
    cmd = cmd_template.format(cmd_dict['left_top_on'], 15, 2, 4, '{}', '{}')
    s = time.time()
    while time.time() - s < 2:
        ser.write(cmd.format(0, 1).encode())
        time.sleep(0.2)
        ser.write(all_off_cmd)
        ser.write(cmd.format(1, 2).encode())
        time.sleep(0.2)
        ser.write(all_off_cmd)


def r2d2_noise():
    cmd = cmd_template.format(cmd_dict['right_bottom_on'], 15, 2, 3, '{}', '{}')
    s = time.time()
    while time.time() - s < 2:
        ser.write(cmd.format(0, 1).encode())
        time.sleep(0.2)
        ser.write(all_off_cmd)
        ser.write(cmd.format(1, 2).encode())
        time.sleep(0.2)
        ser.write(all_off_cmd)


def warp_speed_effect():
    # go from back column to front column with all rows lit
    cmd = cmd_template.format(cmd_dict['all_on'], 15, 0, 3, '{}', '{}')
    for i in range(6, -1, -1):
        print(cmd.format(i, i+1))
        ser.write(cmd.format(i, i+1).encode())
        time.sleep(0.5)

    delay = 0.1
    ser.write(all_off_cmd)
    ser.write(cmd.format(1, 5).encode())
    time.sleep(delay)

    ser.write(all_off_cmd)
    ser.write(cmd.format(2, 4).encode())
    time.sleep(delay)

    ser.write(all_off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 15, 0, 2, 2, 4).encode())
    time.sleep(delay)

    ser.write(all_off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 15, 0, 2, 2, 3).encode())
    time.sleep(delay)

    ser.write(all_off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 15, 0, 1, 2, 3).encode())
    time.sleep(delay)

    ser.write(all_off_cmd)
    ser.write(cmd_template.format(cmd_dict['all_on'], 15, 0, 0, 2, 2).encode())
    time.sleep(delay)

    ser.write(all_off_cmd)


def rsl_gradient(jump):
    on_cmd = rsl_on_cmd.format(cmd_dict['ready_state_on'], '{}')
    for i in range(0, 256, jump):
        ser.write(on_cmd.format(i).encode())
        time.sleep(0.10)
    ser.write(rsl_off_cmd)


def run_effects_timing():
    s = time.time()
    time.sleep(23)
    irritate_noise()  # 0:24
    time.sleep(30)
    r2d2_noise()  # 0:58
    time.sleep(6)
    irritate_noise()
    irritate_noise()  # 1:09
    time.sleep(4)
    rsl_gradient(9)  # 1:15
    while time.time() - s < 82:  # 1:24
        single_laser_beam()
        time.sleep(0.2)
    time.sleep(8)  # 1:31
    ship_takeoff()  # 1:39
    time.sleep(24)  # 2:03
    rsl_gradient(6)  # 2:07
    time.sleep(12)  # 2:19
    while time.time() - s < 144:  # 2:24
        single_laser_beam()
    time.sleep(7)  # 2:31
    while time.time() - s < 165:  # 2:33
        single_laser_beam()
        time.sleep(random.randint(0, 3))
    time.sleep(3)  # 2:49
    warp_speed_effect()


if __name__ == '__main__':
    clip_url = 'https://www.youtube.com/watch?v=qPEB9PS5mOw'
    # play_clip(clip_url, True, 176)
    # time.sleep(177)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    s = time.time()
    play_clip(clip_url, True)
    time.sleep(2)
    run_effects_timing()
    print(time.time() - s)
    ser.close()
















