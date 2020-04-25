import glob
import cv2
import sys
import numpy as np
from sklearn.metrics import mean_squared_error
from skimage.measure import compare_ssim


def full_image_similarty_example(img1, img2):
    # MSE increases the images are less similar
    # SSIM smaller values indicate less similarity
    ssim = compare_ssim(img1, img2)
    print('SSIM', ssim)
    mse = mean_squared_error(img1, img2)
    print('MSE', mse)


def show_image(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def template_matching_example():
    # read in the images and templates
    images = glob.glob('images/*.png')
    print(images)
    # for each image find if template matches
    for idx in range(len(images)):
        print('Checking ', images[idx])
        img = cv2.imread(images[idx], 0)
        res = cv2.matchTemplate(template, img, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= thold)
        print(loc)
        if len(loc[0]) > 0:
            print('found match')
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), 2)
                break
            show_image('res.png', img)


def process_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(template, frame, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thold)
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


def emo_rec_cam(cam_id):
    vc = cv2.VideoCapture(cam_id)
    cam_id_str = str(cam_id)
    cv2.namedWindow("preview" + cam_id_str)
    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        frame = process_frame(frame)
        cv2.imshow("preview" + cam_id_str, frame)
        key = cv2.waitKey(100)
        rval, frame = vc.read()
        if key == 27:  # exit on ESC
            break
    vc.release()
    cv2.destroyWindow("preview" + cam_id_str)


thold = 0.9225
template = cv2.imread('images/templates/happy-template-front.png', 0)
w, h = template.shape[::-1]
emo_rec_cam(0)

# thold = 0.91
# template = cv2.imread('images/templates/happy-template-right.png', 0)
# w, h = template.shape[::-1]
# emo_rec_cam(0)
#
# template = cv2.imread('images/templates/happy-template-left.png', 0)
# w, h = template.shape[::-1]
# emo_rec_cam(1)


# full_image_similarty_example()
# template_matching_example()