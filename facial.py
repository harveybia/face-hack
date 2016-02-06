import cv2
import os
import numpy as np
from PIL import Image, ImageTk
# Author: Harvey Shi

# const
EMO_ANGRY = "EMO_ANGRY"
EMO_SAD = "EMO_SAD"
EMO_HAPPY = "EMO_HAPPY"
EMO_DISGUST = "EMO_DISGUST"
EMO_FEAR = "EMO_FEAR"
EMO_NORMAL = "EMO_NORMAL"

CAMERA_PORT = 0
# Number of frames to throw away while the camera adjusts to light levels
RAMP_FRAMES = 1

CAMERA = cv2.VideoCapture(CAMERA_PORT)

# auxiliary functions

# Facial Emotion Recognition inspired by Bikramjot Singh Hanzra
# http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html

# For face detection we will use the Haar Cascade provided by OpenCV.
CASCADE_PATH = "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)
FACE_PATH    = "faces/"

# For face recognition we will the the LBPH Face Recognizer
RECOGNIZER = cv2.createLBPHFaceRecognizer()
INITIALIZED = False
MAPPING = {}

def needsRecognizer(func):
    # A decorator which initializes recognizer before use
    def f(*args, **kwargs):
        if not INITIALIZED:
            print "Init recognizer"
            dct = getImagesAndLabels("faces")
            MAPPING = trainRecognizer(dct)
        return func(*args, **kwargs)
    INITIALIZED = True
    return f

def getImagesAndLabels(path):
    # Append all the absolute image paths in a list image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not \
        f.endswith('.DS_Store')]

    dct = {}

    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        fname = os.path.split(image_path)[1]
        andrew_id = fname.split(".")[0]
        emotion = fname.split(".")[1]

        # Detect the face in the image
        faces = FACE_CASCADE.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            if andrew_id not in dct.keys(): dct[andrew_id] = {}
            dct[andrew_id][emotion] = image[y:y+h, x:x+w]
            cv2.imshow("Facial Recognition in progress...",
                dct[andrew_id][emotion])
            cv2.waitKey(10)

    return dct

def trainRecognizer(dct):
    images = []
    hashed_labels = []
    mapping = {}
    for andrew_id in dct.keys():
        for emotion in dct[andrew_id].keys():
            fname = andrew_id + "." + emotion + ".png"
            # Mapping: __hash__ : fname
            mapping[fname.__hash__()%2000000] = fname
            images.append(dct[andrew_id][emotion])
            hashed_labels.append(fname.__hash__()%2000000)
    RECOGNIZER.train(images, np.array(hashed_labels))
    print "Trained"
    return mapping

def saveUserFace(dct):
    """saveUserFace(dct) -> None"""
    # Format of dct: {"ANDREW_ID":{"sad":nparray, ...} ...}
    for andrew_id in dct:
        info = dct[andrew_id]
        for emotion in info:
            cv2.imwrite("faces/%s.%s.png"%(andrew_id, emotion),
                info[emotion])
            print "Saved user <%s> in [%s] state."%(andrew_id, emotion)

@needsRecognizer
def recognizeImage(img):
    # recognizeImage(img) -> Bool
    faces = FACE_CASCADE.detectMultiScale(img)
    for (x, y, w, h) in faces:
        nbr_predicted, prob = RECOGNIZER.predict(img[y:y+h, x:x+w])
    return nbr_predicted, prob

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

@needsRecognizer
def getUserEmotion():
    def getEmotionFromName(name):
        return name.split(".")[1]
    predict, prob = recognizeImage(cv2.cvtColor(_getCameraRaw(),
        cv2.COLOR_BGR2GRAY))
    print predict
    emotion = getEmotionFromName(MAPPING[predict])
    emo_mapping = {
        "happy":EMO_HAPPY,
        "sad":EMO_SAD,
        "fear":EMO_FEAR,
        "angry":EMO_ANGRY,
        "disgust":EMO_DISGUST,
        "normal":EMO_NORMAL
    }
    return emo_mapping[emotion]

def getCameraSnapShot():
    # getCameraSnapShot() -> TkImage
    im = _getCameraRaw()
    # This should be executed after Tk() is called
    im = _toTkImage(im)
    return im

# unit test code
if __name__ == "__main__":
    import time

    dct = getImagesAndLabels("faces")
    MAPPING = trainRecognizer(dct)
    print MAPPING
    print getUserEmotion()
    im = _getCameraRaw()
    cv2.imshow("image", im)
    cv2.waitKey(0)
    """
    cv2.imshow("image", im)
    cv2.waitKey(0)
    saveUserFace({"henryzh47":{"happy":im}})
    time.sleep(1)

    im = _getCameraRaw()
    cv2.imshow("image", im)
    cv2.waitKey(0)
    saveUserFace({"henryzh47":{"normal":im}})
    time.sleep(1)

    im = _getCameraRaw()
    cv2.imshow("image", im)
    cv2.waitKey(0)
    saveUserFace({"henryzh47":{"angry":im}})
    time.sleep(1)

    im = _getCameraRaw()
    cv2.imshow("image", im)
    cv2.waitKey(0)
    saveUserFace({"henryzh47":{"fear":im}})
    """
    #a = getImagesAndLabels("faces")
    #print a

    cv2.destroyAllWindows()
