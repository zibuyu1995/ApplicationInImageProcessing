# coding: utf-8

import cv2
import numpy as np

"""
两幅图片合并为一副
"""


def main():
    img1 = cv2.imread('./static/girl.png')
    img2 = cv2.imread('./static/rabbit.png')

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    combine = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)

    # combine 2 images
    combine[:h1, :w1, :3] = img1
    combine[:h2, w1:w1 + w2, :3] = img2
    cv2.imshow('combine_image', combine)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
