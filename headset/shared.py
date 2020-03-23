import threading
import playsound


cmd_dict = {'cmd_start': '<', 'cmd_end': '>', 'all_off': '0', 'all_on': '1',
            'ready_state_on': '2', 'ready_state_off': '3', 'bottom_on': '4',
            'right_bottom_on': '5', 'left_bottom_on': '6', 'bottom_off': '7',
            'top_on': '8', 'right_top_on': '9', 'left_top_on': '10', 'top_off': '11',
            'random': '12'}

note_dict = {'1/2': 0.5, '1/4': 0.25, '1/8': 0.125, '1/16': 0.0625}

# <cmd code, brightness, row start, row end, col start, col end>
leds_cmd = '{} {} {} {}'
cmd_template = '{}{}{}{}'.format(cmd_dict['cmd_start'], '{} {} ', leds_cmd, cmd_dict['cmd_end'])
rsl_template = '{}{} {}{}'.format(cmd_dict['cmd_start'], cmd_dict['ready_state_on'], '{}', cmd_dict['cmd_end'])

off_cmd = (cmd_dict['cmd_start'] + cmd_dict['all_off'] + cmd_dict['cmd_end']).encode()
rsl_off_cmd = '<3>'.encode()


def get_tempo_delay(bpm, ms=False):
    if ms: return 60/bpm * 1000
    return 60/bpm


def play_track(path='/Users/abby/Documents/TREV/sound/b5.m4a'):
    t1 = threading.Thread(target=playsound.playsound, daemon=True,
                          args=(path,))
    t1.start()
    # playsound.playsound('/Users/abby/Documents/TREV/sound/b5.m4a')


if __name__ == '__main__':
    print(get_tempo_delay(103.36))
