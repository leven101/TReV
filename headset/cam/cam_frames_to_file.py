import cv2
import time

def save_cam_images():
    vidcap = cv2.VideoCapture(0)
    while True:
        success, frame = vidcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()
            vidcap.release()
            break
        elif k == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite("images/%d.png" % time.time(), frame)     # save frame as png file


save_cam_images()