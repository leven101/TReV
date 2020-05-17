import cv2
import numpy as np

r_thold = 0.85
template_right = cv2.imread('images/templates/happy-template-right.png', 0)
w_right, h_right = template_right.shape[::-1]

l_thold = 0.90
template_left = cv2.imread('images/templates/happy-template-left.png', 0)
w_left, h_left = template_left.shape[::-1]


def process_frame(frame, cam_id):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template = template_left if cam_id == 1 else template_right
    w = w_left if cam_id == 1 else w_right
    h = h_left if cam_id == 1 else w_left
    res = cv2.matchTemplate(template, frame, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= (l_thold if cam_id == 1 else r_thold))
    print(loc)
    if len(loc[0]) > 0:
        print('Happy')
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), 2)
            cv2.putText(frame, 'ABBY is HAPPY', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            break
    else:
        print('Neutral')
    return frame


def duel_cam_capture_single_thread():
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(1)

    while True:
        # Capture frame-by-frame
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        # Our operations on the frame come here
        frame1 = process_frame(frame1, 0)
        frame2 = process_frame(frame2, 1)
        # Display the resulting frame
        cv2.imshow('frame1', frame1)
        cv2.imshow('frame2', frame2)
        if cv2.waitKey(1) & 0xFF == 27:  # exit on ESC
            break
    # When everything done, release the capture
    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()

duel_cam_capture_single_thread()