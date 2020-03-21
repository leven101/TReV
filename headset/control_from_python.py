import serial
import time


cmd_dict = {'cmd_start': '<', 'cmd_end': '>', 'all_off': '0', 'all_on': '1',
            'ready_state_off': '2', 'ready_state_on': '3'}


if __name__ == '__main__':
    on_cmd = cmd_dict['cmd_start'] + cmd_dict['all_on'] + '|2|0|1|2|3|' + cmd_dict['cmd_end']
    off_cmd = cmd_dict['cmd_start'] + cmd_dict['all_off'] + cmd_dict['cmd_end']
    print(on_cmd)
    print(off_cmd)

    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    time.sleep(2)
    ser.write(off_cmd.encode())
    while True:
        ser.write(on_cmd.encode())
        print(ser.readline())
        time.sleep(0.1)
        ser.write(off_cmd.encode())
        print(ser.readline())
        time.sleep(0.2)


    # time.sleep(3)
    # blink all on one second
    # all off
    # blink top on one second
    # all off
    # blink bottom on one second
    # all off
    # blink ready-state light on
    ser.close()
