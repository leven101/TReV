import time
import serial

import pandas as pd

import headset.shared as shared


in_signals_path = '~/work/TReV/music/out/test-1.csv'
in_audio_path = '/Users/abby/work/TReV/music/audio-files/dt_16bars_102rap.wav'
df = pd.read_csv(in_signals_path, index_col=0, dtype=float)


# shared.play_track(in_audio_path, False)

for _, row in df.iterrows():
    # print(row)
    db = row['top'] + row['bottom']
    top_intensity = round((row['top'] / db) * 15)  # % of top
    bot_intensity = round((row['bottom'] / db) * 15) # % of bottom
    print(top_intensity, bot_intensity, top_intensity + bot_intensity)

