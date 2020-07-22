import cv2
from multiprocessing import Process


def cv2_cam_capture_example():
    cap = cv2.VideoCapture(0)
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def duel_cam_capture_single_thread():
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(1)

    while True:
        # Capture frame-by-frame
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        # Our operations on the frame come here
        frame1 = process_frame(frame1)
        frame2 = process_frame(frame2)
        # Display the resulting frame
        cv2.imshow('frame1', frame1)
        cv2.imshow('frame2', frame2)
        if cv2.waitKey(1) & 0xFF == 27:  # exit on ESC
            break
    # When everything done, release the capture
    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()


def process_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
        frame = process_frame(frame)
        cv2.imshow("preview" + cam_id_str, frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    vc.release()
    cv2.destroyWindow("preview" + cam_id_str)


def dual_cam_capture_multi_thread():
    p0 = Process(target=cam_capture, args=(0,))
    p0.start()
    p1 = Process(target=cam_capture, args=(1,))
    p1.start()
    # if not (p0.is_alive() and p1.is_alive()):
    #     p0.terminate()
    #     p1.terminate()
    #     p0.join()
    #     p1.join()


if __name__ == '__main__':
    dual_cam_capture_multi_thread()


