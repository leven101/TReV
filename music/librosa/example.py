# Beat tracking example
from __future__ import print_function
import librosa
import numpy

# 1. Get the file path to the included audio example
# filename = librosa.util.example_audio_file()
filename = '/Users/alevenberg/Documents/trev/prototype/sound/looperman-l-2942130-0147507-simple-rap-drum.wav'
# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load(filename)

# 3. Run the default beat tracker
tempo, beat_times = librosa.beat.beat_track(y=y, sr=sr, units='time', hop_length=5000)
print(beat_times)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
beat_times_diff = numpy.diff(beat_times)
print(beat_times_diff)
# # 3. Run the default beat tracker
# tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#
# # 4. Convert the frame indices of beat events into timestamps
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)
#
# print('Saving output to beat_times.csv')
# print(beat_times)
# librosa.output.times_csv('beat_times_2.csv', beat_times)