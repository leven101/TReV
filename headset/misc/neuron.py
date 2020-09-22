import serial
import time
import random


from headset.shared import cmd_template, cmd_dict, all_off_cmd, rsl_on_cmd

#
ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
ser.write(all_off_cmd)
bght=10
slp=0.01

start=0
end=4
cmd = 'left_top_on'

# ser.write(rsl_on_cmd.format(200).encode())
while start != end:
    print(start, end)
    # light start column
    ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 3, start, start).encode())
    time.sleep(slp)
    # go to end
    for c in range(start+1, end):
        ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 0, c, c).encode())
        time.sleep(slp)
        ser.write(cmd_template.format(cmd_dict[cmd], 0, 0, 0, c, c).encode())
    # light end column
    ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 3, end, end).encode())
    time.sleep(slp)
    # go back to start
    for c in range(end-1, start, -1):
        ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 0, c, c).encode())
        time.sleep(slp)
        ser.write(cmd_template.format(cmd_dict[cmd], 0, 0, 0, c, c).encode())
    start += 1
    end -= 1
ser.write(cmd_template.format(cmd_dict[cmd], bght, 0, 3, 3, 3).encode())
time.sleep(3)
ser.write(all_off_cmd)
