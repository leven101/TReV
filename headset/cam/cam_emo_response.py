import cv2
import time
import serial
import numpy as np
from multiprocessing import Process

import headset.shared as shared


thold = 0.90
template_right = cv2.imread('images/templates/happy-template-right.png', 0)
template_right = cv2.flip(template_right, 0)
w_right, h_right = template_right.shape[::-1]

template_left = cv2.imread('images/templates/happy-template-left.png', 0)
template_left = cv2.flip(template_left, 0)
w_left, h_left = template_left.shape[::-1]

rv_cmd = shared.cmd_template.format(shared.cmd_dict['all_on'], 100, 1, 1, 1, 1).encode()


def blink_led():
    ser.write(rv_cmd)
    time.sleep(0.1)
    ser.write(shared.off_cmd)


def process_frame(frame, cam_id):
    frame = cv2.flip(frame, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template = template_left if cam_id == 1 else template_right
    w = w_left if cam_id == 1 else w_right
    h = h_left if cam_id == 1 else w_left
    res = cv2.matchTemplate(template, frame, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thold)
    print(loc)
    if len(loc[0]) > 0:
        Process(target=blink_led()).start()
        print('Happy')
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), 2)
            break
    else:
        print('Neutral')
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


if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    cam_capture(1)
    ser.close()

