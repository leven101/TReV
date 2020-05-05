from multiprocessing import Process
import playsound
import time

cmd_dict = {'cmd_start': '<', 'cmd_end': '>', 'all_off': '0', 'all_on': '1',
            'ready_state_on': '2', 'ready_state_off': '3', 'bottom_on': '4',
            'right_bottom_on': '5', 'left_bottom_on': '6', 'bottom_off': '7',
            'top_on': '8', 'right_top_on': '9', 'left_top_on': '10', 'top_off': '11',
            'random': '12'}

# note is how long the beat should last. ie - how long the light should be on for each beat
note_dict = {'1/2': 0.5, '1/4': 0.25, '1/8': 0.125, '1/16': 0.0625}

# <cmd code, brightness, row start, row end, col start, col end>
leds_cmd = '{} {} {} {}'
cmd_template = '{}{}{}{}'.format(cmd_dict['cmd_start'], '{} {} ', leds_cmd, cmd_dict['cmd_end'])
rsl_on_cmd = '{}{} {}{}'.format(cmd_dict['cmd_start'], cmd_dict['ready_state_on'], '{}', cmd_dict['cmd_end'])

off_cmd = (cmd_dict['cmd_start'] + cmd_dict['all_off'] + cmd_dict['cmd_end']).encode()
rsl_off_cmd = '<3>'.encode()

total_brightness = 10


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


def play_track(path='/Users/abby/work/TReV/music/audio-files/b5.m4a', daemon=True):
    t1 = Process(target=playsound.playsound, daemon=daemon, args=(path,))
    t1.start()
    # playsound.playsound('../music/audio-files/b5.m4a')


def flash_all(ser, seconds=0.5, brightness=7):
    flash_cmd = cmd_template.format(cmd_dict['all_on'], brightness, 0, 4, 0, 7)
    ser.write(flash_cmd.encode())
    time.sleep(seconds)
    ser.write(off_cmd)


if __name__ == '__main__':
    print(beats_per_second(103.36))
    # play_track()

