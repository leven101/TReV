import glob
import cv2
import sys
import numpy as np
from skimage.measure import compare_ssim as ssim

# import headset.cam.cam_duel as cam_cap

def mse(x, y):
    return np.linalg.norm(x - y)
'''
Todo:
- Get 3 images from headset cams
    - normal 
    - scowl/frown
    - happy
- For each frame get closest template
'''

templates = glob.glob('template-images/*')
print(templates)

# MSE increases the images are less similar
# SSIM smaller values indicate less similarity

for idx1 in range(len(templates)):
    img1 = cv2.imread(templates[idx1], 0)
    h1, w1 = img1.shape
    top_ssim = -1
    best_ssim_img = -1
    lowest_mse = sys.float_info.max
    best_mse_img = -1
    for idx2 in range(len(templates)):
        if idx1 == idx2: continue
        img2 = cv2.imread(templates[idx2], 0)
        h2, w2 = img2.shape
        h = min(h1, h2)
        w = min(w1, w2)
        img11 = img1[:h, :w]
        img2 = img2[:h, :w]
        # print(img11.shape, img2.shape)
        img_sim = ssim(img11, img2)
        # print('\nSSIM', templates[idx1], templates[idx2], img_sim)
        if img_sim > top_ssim:
            top_ssim = img_sim
            best_ssim_img = idx2
        img_mse = mse(img11, img2)
        # print('MSE', templates[idx1], templates[idx2], img_mse)
        if img_mse < lowest_mse:
            lowest_mse = img_mse
            best_mse_img = idx2
    print('\n\n', templates[idx1])
    print('Best image SSIM:', templates[best_ssim_img], top_ssim)
    print('Best image MSE:', templates[best_mse_img], lowest_mse)
    # break