import cv2


def save_cam_images():
    vidcap = cv2.VideoCapture(0)
    count = 0
    while True:
        input()
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        success, frame = vidcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        cv2.imwrite("template-images/frame%d.jpg" % count, frame)     # save frame as JPEG file
        count += 1

