# coding: utf-8

import cv2
import numpy as np


def cover_t():
    origin_image = cv2.imread('./static/rabbit.png')
    h, w = origin_image.shape[:2]
    new_image = np.zeros((h, w, 3), np.uint8)
    for i in range(1, int(h / 100)):
        for j in range(1, int(w / 100)):
            cut_image = origin_image[(i - 1) * 100:i * 100, (j - 1) * 100:j * 100]
            new_image[(i - 1) * 100:i * 100, (j - 1) * 100:j * 100] = cut_image
    cv2.imshow('pm', new_image)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    cover_t()