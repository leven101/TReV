import cv2
import os
import time
import serial
import pandas as pd
import numpy as np
from multiprocessing import Process

import headset.shared as shared
import headset.music.signals_to_headset as headset

thold = 0.85
template_right = cv2.imread('../cam/images/templates/happy-template-right.png', 0)
template_right = cv2.flip(template_right, 0)
w_right, h_right = template_right.shape[::-1]

template_left = cv2.imread('../cam/images/templates/happy-template-left.png', 0)
template_left = cv2.flip(template_left, 0)
w_left, h_left = template_left.shape[::-1]

emotions = ['Neutral', 'Positive']
current_emotion = emotions[0]

in_audio_path = '/Users/abby/work/TReV/music/audio-files/tones/100hz.wav'
in_signals_path = 'track-data/{}-track-data.csv'.format(os.path.basename(in_audio_path))


def process_frame(frame, cam_id):
    global current_emotion
    frame = cv2.flip(frame, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template = template_left if cam_id == 1 else template_right
    w = w_left if cam_id == 1 else w_right
    h = h_left if cam_id == 1 else w_left
    res = cv2.matchTemplate(template, frame, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thold)
    print(loc)
    if len(loc[0]) > 0:
        current_emotion = emotions[1]
        print('Happy')
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), 2)
            break
    else:
        current_emotion = emotions[0]
    print(current_emotion)
    return frame


def cam_capture(cam_id):
    vc = cv2.VideoCapture(cam_id)
    cam_id_str = str(cam_id)
    cv2.namedWindow("preview" + cam_id_str)
    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval, frame = False, None

    while rval:
        frame = process_frame(frame, cam_id)
        cv2.imshow("preview" + cam_id_str, frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    vc.release()
    cv2.destroyWindow("preview" + cam_id_str)


def start_cam():
    p0 = Process(target=cam_capture, args=(0,))
    p0.start()
    return p0


def stop_cam(process):
    process.terminate()
    process.join()


def get_light_intensity(row):
    emotion_factor = 2 if current_emotion == emotions[1] else 0
    # % of top
    top_intensity = max(0, row['top'] * shared.total_brightness - emotion_factor)
    # % of bottom
    bot_intensity = row['bottom'] * shared.total_brightness + emotion_factor
    print(emotion_factor, top_intensity, bot_intensity, top_intensity + bot_intensity)
    return top_intensity, bot_intensity


def run_track_program():
    df = pd.read_csv(in_signals_path, dtype=float)
    shared.play_track(in_audio_path, False)
    start_time = time.time()
    for _, row in df.iterrows():
        procs = []
        top_intensity, bot_intensity = get_light_intensity(row)
        s_t = time.time()
        procs.append(Process(target=headset.top, args=(ser, row, bot_intensity, s_t)))
        procs.append(Process(target=headset.bottom, args=(ser, row, top_intensity, s_t)))
        procs.append(Process(target=headset.ready_state_light, args=(ser, row, s_t)))
        [p.start() for p in procs]
        [p.join() for p in procs]
    end_time = time.time()
    print('run_track_program:', start_time, end_time, end_time-start_time)
    ser.write(shared.off_cmd)


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    p = start_cam()
    run_track_program()
    stop_cam(p)
    ser.close()
