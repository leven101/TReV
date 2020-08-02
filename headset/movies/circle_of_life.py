import serial
import time
import pandas as pd

from headset.shared import play_clip, all_off_cmd, flash_all
from headset.movies import special_effects
from headset.music.stereo_signals_to_headset import run_track_program


def play_effects(ser):
    special_effects.sunrise(ser, 11)  # 11
    time.sleep(15)
    flash_all(ser)   # 25
    run_track_program(df[df['cum_secs'].between(25, 51, inclusive=True)], ser)  # 50
    time.sleep(33)
    flash_all(ser, 0.5, 5)
    time.sleep(1)
    ser.write(special_effects.random_cmd)  # 1:28
    time.sleep(8)
    run_track_program(df[df['cum_secs'].between(97, 133, inclusive=True)], ser)  # 2:12
    time.sleep(3)
    special_effects.circle_of_light(ser, 1, 3, 7)
    time.sleep(1)
    flash_all(ser)


if __name__ == '__main__':
    clip_url = 'https://www.youtube.com/watch?v=GibiNy4d4gc'
    play_clip(clip_url, False, 143)
    time.sleep(144)
    signals_path = "/Users/abby/work/TReV/headset/music/track-data/circle-of-life.wav-stereo.csv"
    df = pd.read_csv(signals_path, dtype=float)
    df['cum_secs'] = df['seconds'].cumsum()

    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    play_clip(clip_url, False, 143)
    time.sleep(1.3)

    play_effects(ser)
    ser.write(all_off_cmd)
    ser.close()


