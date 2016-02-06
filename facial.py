import cv2
from PIL import Image, ImageTk
# Author: Harvey Shi

# const
EMO_ANGRY = 100
EMO_SAD = 101
EMO_HAPPY = 102

# test purposes
ex_img = cv2.imread("no_signal.png", 1)

# auxiliary functions
def _toTkImage(img):
    # convert to RGB channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(img)
    # return a TkImage which could be used directly by Tkinter
    return ImageTk.PhotoImage(im)

# interface

def getUserEmotion():
    return EMO_SAD

def getCameraSnapShot():
    # getCameraSnapShot() -> TkImage
    return _toTkImage(ex_img)
