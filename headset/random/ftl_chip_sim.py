import serial
import time
import random

from headset.shared import cmd_template, cmd_dict, all_off_cmd

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
ser.write(all_off_cmd)
bght=1
# slp=1/6
slp = 0.07615690449473558 / 8.049
print(slp)
r = 15
pt_a = 0
pt_b = 6
cmd = 'all_on'


def pta_to_ptb():
    start = time.time()
    # go from pt_a to pt_b
    for c in range(pt_a, pt_b + 1):
        ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 3, c, c).encode())
        time.sleep(slp)
        ser.write(all_off_cmd)
    print(time.time() - start)


def ptb_to_pta():
    start = time.time()
    # go from pt_b to pt_a
    for c in range(pt_b, pt_a - 1, -1):
        print(c)
        ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 3, c, c).encode())
        time.sleep(slp)
        ser.write(all_off_cmd)
    print(time.time() - start)


for _ in range(12):
    ptb_to_pta()
    time.sleep(slp)
    pta_to_ptb()
time.sleep(1)
ser.write(all_off_cmd)
# ser.close()