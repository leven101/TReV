import serial
import time

cmd_dict = {'cmd_start': '<', 'cmd_end': '>', 'all_off': '0', 'all_on': '1',
            'ready_state_on': '2', 'ready_state_off': '3', 'bottom_on': '4',
            'bottom_off': '7', 'top_on': '8', 'top_off': '11', 'random': '12'}

'''
Time steps
0:00 - all off
 0:01- 0:03 - ready state light increases from lowest to highest

0:04 - 0:012 - each second we “sparkle” the rows from bottom row of bottom LEDS to top row of top LEDs

0:13 - 0:17 - all lights off

0:17 - all LEDs lights flash

0:18 - 0:19 - random sparkle
'''

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)

start_time = time.time()
off_cmd = cmd_dict['cmd_start'] + cmd_dict['all_off'] + cmd_dict['cmd_end']
print('off_cmd', off_cmd)
ser.write(off_cmd.encode())
time.sleep(2)

ready_state_cmd = cmd_dict['cmd_start'] + cmd_dict['ready_state_on'] + ' {}' + cmd_dict['cmd_end']
print('ready_state_cmd', ready_state_cmd)

for i in range(0, 256, 9):
    ser.write(ready_state_cmd.format(i).encode())
    print(i, ready_state_cmd.format(i))
    time.sleep(0.1)
ser.write(off_cmd.encode())
print('off_cmd', off_cmd)

on_cmd = cmd_dict['cmd_start'] + '{} 10 {} {} 0 7' + cmd_dict['cmd_end']
for i in range(4, -1, -1):
    ser.write(on_cmd.format(cmd_dict['bottom_on'], i, i+1).encode())
    print('on_cmd', on_cmd.format(cmd_dict['bottom_on'], i, i+1))
    time.sleep(1)
    ser.write(off_cmd.encode())
    print('off_cmd', off_cmd)
for i in range(0, 4):
    ser.write(on_cmd.format(cmd_dict['top_on'], i, i+1).encode())
    print('on_cmd', on_cmd.format(cmd_dict['top_on'], i, i+1))
    time.sleep(1)
    ser.write(off_cmd.encode())
    print('off_cmd', off_cmd)

ser.write(off_cmd.encode())
print('off_cmd', off_cmd)
time.sleep(4)
#
on_cmd = cmd_dict['cmd_start'] + cmd_dict['all_on'] + ' 14 0 4 0 7' + cmd_dict['cmd_end']
ser.write(on_cmd.encode())
print('all on', on_cmd)
time.sleep(1)

random_cmd = cmd_dict['cmd_start'] + cmd_dict['random'] + ' 2' + cmd_dict['cmd_end']
ser.write(random_cmd.encode())
print('random_cmd', random_cmd)
time.sleep(2)

ser.write(off_cmd.encode())
print('off_cmd', off_cmd)

# close()
print(time.time() - start_time)