
cmd_dict = {'cmd_start': '<', 'cmd_end': '>', 'all_off': '0', 'all_on': '1',
            'ready_state_on': '2', 'ready_state_off': '3', 'bottom_on': '4',
            'right_bottom_on': '5', 'left_bottom_on': '6', 'bottom_off': '7',
            'top_on': '8', 'right_top_on': '9', 'left_top_on': '10', 'top_off': '11',
            'random': '12'}

off_cmd = (cmd_dict['cmd_start'] + cmd_dict['all_off'] + cmd_dict['cmd_end']).encode()

# <cmd code, brightness, row start, row end, col start, col end>
leds_cmd = '{} {} {} {}'
cmd_template = '{}{}{}{}'.format(cmd_dict['cmd_start'], '{} {} ', leds_cmd, cmd_dict['cmd_end'])


if __name__ == '__main__':
    print(cmd_template)
    print(cmd_template.format(cmd_dict['top_on'], 10, 3, 4, 3, 4))

