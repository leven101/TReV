import serial
import time
from headset.shared import play_clip, all_off_cmd, flash_all, rsl_on_cmd, rsl_off_cmd
from headset.movies import special_effects


def play_effects(ser):
    ser.write(rsl_on_cmd.format(100).encode())
    time.sleep(5)
    ser.write(rsl_off_cmd)
    time.sleep(4)   # 9
    flash_all(ser)
    time.sleep(11)  # 20
    special_effects.explosion(ser, 'right_top_on', 2)
    time.sleep(25)  # 44
    special_effects.gun_shot(ser, 'left_top_on')
    time.sleep(2)  # 47
    special_effects.explosion(ser, 'right_top_on', 2)
    time.sleep(4)  # 52
    special_effects.gun_shot(ser, 'left_bottom_on')
    special_effects.gun_shot(ser, 'left_bottom_on')
    time.sleep(0.5)  # 53
    special_effects.gun_shot(ser, 'left_top_on')
    time.sleep(6)  # 60
    special_effects.gun_shot(ser, 'top_on')
    ser.write(all_off_cmd)


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    ser.write(all_off_cmd)
    clip_url = 'https://www.youtube.com/watch?v=2BKfE76hTJ8'
    time.sleep(2)  # url load time
    play_clip(clip_url, False)
    play_effects(ser)
    ser.close()