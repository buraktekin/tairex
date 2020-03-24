# -*- coding: utf-8 -*-
"""
Helper method implementations for saving, loading 
models and image processing and displaying
"""

from io import BytesIO
from PIL import Image

import os
import cv2
import base64
import pickle
import numpy as np


# use canvas directly to get current state's image rather using libraries taking screenshot
getbase64Script = "canvasRunner = document.getElementById('game-area'); \
return canvasRunner.toDataURL().substring(22)"


def save_logs(obj, name):
    with open('../logs/' + name + '.pkl', 'wb+') as f:
        # set protocol to HIGHEST to faten pickle
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_logs(name):
    with open('../logs/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def grab_screen(_driver=None):
    image_b64 = _driver.execute_script(getbase64Script)
    screen = np.array(Image.open(BytesIO(base64.b64decode(image_b64))))
    image = process_img(screen)
    return image


def process_img(image):
    # GRAYSCALE?
    image = image[:300, :500]  # Crop Region of Interest(ROI)
    image = cv2.resize(image, (80, 80))
    image = cv2.Canny(image, threshold1=100, threshold2=200)  # edge detection
    return image


def show_img(graphs=False):
    """@Coroutine"""
    while True:
        screen = (yield)
        window_title = "logs" if graphs else "game_play"
        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
        cv2.imshow(window_title, screen)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break
