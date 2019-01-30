import time

time_delay = 2
letters = ['a', 'b', 'c', 'd', 'e']
i = 0
t_end = time.time() + time_delay
while 1:
    if time.time() < t_end:
        print("printing '{}' for {} seconds".format(letters[i], time_delay))
    else:
        time.sleep(1)
        t_end = time.time() + time_delay
        i = (i + 1) % len(letters)


