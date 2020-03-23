# -*- coding: utf-8 -*-
"""
Helper method implementations for saving, loading 
models and image processing and displaying
"""


def save_obj(obj, name):
    with open('objects/' + name + '.pkl', 'wb') as f:  # dump files into objects folder
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('objects/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def grab_screen(_driver=None):
    screen = np.array(ImageGrab.grab(bbox=(40, 180, 440, 400)))  # bbox = region of interset on the entire screen
    image = process_img(screen)  # processing image as required
    return image


def process_img(image):
    # game is already in grey scale canvas, canny to get only edges and reduce unwanted objects(clouds)
    image = cv2.resize(image, (0, 0), fx=0.15, fy=0.10)  # resale image dimensions
    image = image[2:38, 10:50]  # img[y:y+h, x:x+w] #crop out the dino agent from the frame
    image = cv2.Canny(image, threshold1=100, threshold2=200)  # apply the canny edge detection
    return image


def show_img(graphs=False):
    """
    @Coroutine
    """
    while True:
        screen = (yield)
        window_title = "logs" if graphs else "game_play"
        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
        imS = cv2.resize(screen, (800, 400))
        cv2.imshow(window_title, screen)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break
