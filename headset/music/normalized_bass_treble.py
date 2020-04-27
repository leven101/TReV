import time
import serial

import pandas as pd

import headset.shared as shared


in_signals_path = '~/work/TReV/music/out/test-1.csv'
in_audio_path = '/Users/abby/work/TReV/music/audio-files/dt_16bars_102rap.wav'
df = pd.read_csv(in_signals_path, index_col=0, dtype=float)

total_brightness = 15
# shared.play_track(in_audio_path, False)

for _, row in df.iterrows():
    # print(row)
    top_intensity = row['top'] * total_brightness  # % of top
    bot_intensity = row['bottom'] * total_brightness  # % of bottom
    print(top_intensity, bot_intensity, top_intensity + bot_intensity)

