import serial
import time
import random

from headset.shared import cmd_template, cmd_dict, all_off_cmd, rsl_on_cmd

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
ser.write(all_off_cmd)
bght=7
start = time.time()
ser.write(rsl_on_cmd.format(250).encode())
time.sleep(1)
for _ in range(1):
    for r in range(4):
        for c in range(6):
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r, r, c, c).encode())
            time.sleep(0.05)
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r+1, r+1, c+1, c+1).encode())
            time.sleep(0.05)
            ser.write(all_off_cmd)
            time.sleep(0.25)

for _ in range(1):
    for r in range(4):
        for c in range(6):
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r, r, c, c).encode())
            time.sleep(0.05)
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r+1, r+1, c+1, c+1).encode())
            time.sleep(0.05)
            ser.write(all_off_cmd)
            time.sleep(0.01)
bght=15
for _ in range(2):
    for r in range(4):
        for c in range(6):
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r, r, c, c).encode())
            time.sleep(0.01)
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r+1, r+1, c+1, c+1).encode())
            time.sleep(0.01)
            ser.write(all_off_cmd)
            time.sleep(0.01)

for _ in range(2):
    for r in range(4):
        for c in range(6):
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r, r, c, c).encode())
            time.sleep(0.01)
            ser.write(cmd_template.format(cmd_dict['all_on'], bght, r+1, r+1, c+1, c+1).encode())
            time.sleep(0.01)
            ser.write(all_off_cmd)
            time.sleep(0.001)

# while time.time() - start < 10:
#     ser.write(cmd_template.format(cmd_dict['bottom_on'], bght, 2, 3, 3, 6).encode())
#     time.sleep(.2)
#     ser.write(all_off_cmd)



print(time.time()-start)
ser.write(all_off_cmd)
ser.close()