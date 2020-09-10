import serial
import time
import random
from multiprocessing import Process

from headset.shared import cmd_template, cmd_dict, all_off_cmd

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
ser.write(all_off_cmd)
bght=5
rr=0.07615690449473558
weight_ratio = rr/1.5


def pta_to_ptb(pt_a, pt_b, r, cmd):
    slp = weight_ratio / (pt_b - pt_a)
    start = time.time()
    # go from pt_a to pt_b
    for c in range(pt_a, pt_b + 1):
        ser.write(cmd_template.format(cmd_dict[cmd], bght, r[0], r[1], c, c).encode())
        time.sleep(slp)
        ser.write(cmd_template.format(cmd_dict[cmd], 0, r[0], r[1], c, c).encode())
    print(time.time() - start)


def ptb_to_pta(pt_a, pt_b, r, cmd):
    slp = weight_ratio / (pt_b - pt_a)
    start = time.time()
    # go from pt_b to pt_a
    for c in range(pt_b, pt_a - 1, -1):
        ser.write(cmd_template.format(cmd_dict[cmd], bght, r[0], r[1], c, c).encode())
        time.sleep(slp)
        ser.write(cmd_template.format(cmd_dict[cmd], 0, r[0], r[1], c, c).encode())
    print(time.time() - start)


# pta_to_ptb(1, 3, [1, 1])
for _ in range(150):
    c1 = random.randint(0, 4)
    r11 = random.randint(0, 3)
    r12 = r11 if random.random() >= 0.5 else r11 + 1
    c2 = random.randint(0, 3)
    r21 = random.randint(0, 3)
    r22 = r21 if random.random() < 0.5 else r21 + 1
    print(c1, r11, r12, c2, r21, r22)
    p1 = Process(target=ptb_to_pta, args=(c1, c1+2, [r11, r12], 'top_on'))
    p1.start()
    p2 = Process(target=pta_to_ptb, args=(c2, c2+3, [r21, r22], 'bottom_on'))
    p2.start()
    p1.join()
    p2.join()
    time.sleep(rr)
ser.flush()
time.sleep(0.5)
ser.write(all_off_cmd)
# ser.close()