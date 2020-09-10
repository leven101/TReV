import random
import serial
import time


from headset.shared import cmd_template, cmd_dict, all_off_cmd, rsl_on_cmd

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
ser.write(all_off_cmd)
ser.write(rsl_on_cmd.format(250).encode())
bght=15
for _ in range(11):
    col = random.randint(0, 7)
    ser.write(cmd_template.format(cmd_dict['left_bottom_on'], bght, 0, 3, col, col).encode())
    print(_, "got the stick!")
    time.sleep(random.uniform(0.5, 4))
    ser.write(all_off_cmd)
    time.sleep(random.uniform(0.5, 2))

ser.write(all_off_cmd)
ser.close()