import serial
import time
import random

from headset.shared import cmd_template, cmd_dict, all_off_cmd


ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
ser.write(all_off_cmd)
bght=15
slp=0.1
start = time.time()

r=1
# for random column
for _ in range(5):
    c = random.randint(0, 6)
    c2 = random.randint(0, 6)
    l_v_r = random.choice(['left', 'right'])
    l_v_r2 = random.choice(['left', 'right'])
    bot_cmd = '{}_bottom_on'.format(l_v_r)
    bot_cmd2 = '{}_bottom_on'.format(l_v_r2)
    top_cmd = '{}_top_on'.format(l_v_r)
    top_cmd2 = '{}_top_on'.format(l_v_r2)
    for b_r_s in range(3, -1, -1):
        print('\nb_r_s:', b_r_s)
        # turns on one LED
        ser.write(cmd_template.format(cmd_dict[bot_cmd], bght, b_r_s, b_r_s, c, c).encode())
        ser.write(cmd_template.format(cmd_dict[bot_cmd2], bght, b_r_s, b_r_s, c2, c2).encode())
        time.sleep(slp)
        tmp_b = bght
        for b_r_e in range(b_r_s + 1, 4):
            print('b_r_e:', b_r_e, tmp_b)
            tmp_b -= 1
            ser.write(cmd_template.format(cmd_dict[bot_cmd], tmp_b, b_r_s, b_r_e, c, c).encode())
            ser.write(cmd_template.format(cmd_dict[bot_cmd2], tmp_b, b_r_s, b_r_e, c2, c2).encode())
            time.sleep(slp)
        ser.write(all_off_cmd)

    for t_r_s in range(4):
        print('\nt_r_s:', t_r_s)
        ser.write(cmd_template.format(cmd_dict[top_cmd], bght, t_r_s, t_r_s, c, c).encode())
        ser.write(cmd_template.format(cmd_dict[top_cmd2], bght, t_r_s, t_r_s, c2, c2).encode())
        time.sleep(slp)
        tmp_b = bght
        for t_r_e in range(t_r_s-1, -1, -1):
            print('t_r_e:', t_r_e)
            tmp_b -= 1
            ser.write(cmd_template.format(cmd_dict[top_cmd], tmp_b, t_r_e, t_r_s, c, c).encode())
            ser.write(cmd_template.format(cmd_dict[top_cmd2], tmp_b, t_r_e, t_r_s, c2, c2).encode())
            time.sleep(slp)
        for b_r in range(4):
            tmp_b -= 1
            ser.write(cmd_template.format(cmd_dict[bot_cmd], tmp_b, b_r, b_r, c, c).encode())
            ser.write(cmd_template.format(cmd_dict[bot_cmd2], tmp_b, b_r, b_r, c2, c2).encode())
            time.sleep(slp)
        ser.write(all_off_cmd)

ser.write(all_off_cmd)