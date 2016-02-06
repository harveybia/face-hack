import cv2
from PIL import Image, ImageTk
# Author: Harvey Shi

# const
EMO_ANGRY = 100
EMO_SAD = 101
EMO_HAPPY = 102

CAMERA_PORT = 0
# Number of frames to throw away while the camera adjusts to light levels
RAMP_FRAMES = 1

CAMERA = cv2.VideoCapture(CAMERA_PORT)

# test purposes
ex_img = cv2.imread("no_signal.png", 1)

# auxiliary functions
def _toTkImage(img):
    # convert to RGB channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(img)
    # return a TkImage which could be used directly by Tkinter
    return ImageTk.PhotoImage(im)

def _getCameraRaw():
    focusCamera()
    retval, img = CAMERA.read()
    return img

# interface

def focusCamera():
    for i in xrange(RAMP_FRAMES):
        CAMERA.read()

def getUserEmotion():
    return EMO_SAD

def getCameraSnapShot():
    # getCameraSnapShot() -> TkImage
    im = _getCameraRaw()
    # This should be executed after Tk() is called
    im = _toTkImage(im)
    return im

# unit test code
if __name__ == "__main__":
    print getUserEmotion()
    cv2.imshow("image", _getCameraRaw())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
