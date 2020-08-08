import os
import time
import playsound
from subprocess import Popen
from multiprocessing import Process

cmd_dict = {'all_off': '0', 'all_on': '1',
            'ready_state_on': '2', 'ready_state_off': '3', 'bottom_on': '4',
            'right_bottom_on': '5', 'left_bottom_on': '6', 'bottom_off': '7',
            'top_on': '8', 'right_top_on': '9', 'left_top_on': '10', 'top_off': '11',
            'random': '12', 'left_top_off': '13', 'right_top_off': '14',
            'left_bottom_off': '15', 'right_bottom_off': '16'}

# note is how long the beat should last. ie - how long the light should be on for each beat
note_dict = {'1/2': 0.5, '1/4': 0.25, '1/8': 0.125, '1/16': 0.0625}

# <cmd code, brightness, row start, row end, col start, col end>
leds_cmd = '{} {} {} {}'
cmd_template = '<{}{}>'.format('{} {} ', leds_cmd)
rsl_on_cmd = '<{} {}>'.format(cmd_dict['ready_state_on'], '{}')

rsl_off_cmd = '<3>'.encode()
off_cmd = '<{}>'
all_off_cmd = off_cmd.format(cmd_dict['all_off']).encode()
total_brightness = 15


# tempo is number of times the light blinks
def beats_per_second(bpm, ms=False):
    if ms: return 60/bpm * 1000
    return 60/bpm


# tempo: how many times the lights blink a second
# note: how long each light is on for
def get_tempo(bpm, note):
    if bpm > 0:
        tempo = beats_per_second(bpm)
        return tempo - note
    else:
        return 0


def play_track(path, daemon=True):
    t1 = Process(target=playsound.playsound, daemon=daemon, args=(path,))
    t1.start()
    # playsound.playsound(path)


def flash_all(ser, seconds=0.5, brightness=7):
    flash_cmd = cmd_template.format(cmd_dict['all_on'], brightness, 0, 4, 0, 7)
    ser.write(flash_cmd.encode())
    time.sleep(seconds)
    ser.write(all_off_cmd)


def play_clip(url, daemon=True, secs=None, youtube=True):
    if youtube:
        import pafy  # importing paft globally breaks play_track with multiprocess.Process???
        video = pafy.new(url)
        best = video.getbest()
        url = best.url
    cmd = '/Applications/VLC.app/Contents/MacOS/VLC --no-video-title "{}"'.format(url)
    t1 = Process(target=play_media_thread, args=(cmd, secs), daemon=daemon)
    t1.start()


def play_media_thread(cmd, secs):
    process = Popen(cmd, shell=True)
    if secs:
        time.sleep(secs)
        process.kill()


if __name__ == '__main__':
    # print(beats_per_second(103.36))
    play_track('/Users/abby/work/TReV/music/audio-files/simple-hip-hop-beat_170bpm.wav', False)