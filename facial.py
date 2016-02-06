import cv2
import os
import numpy as np
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

# auxiliary functions

# Facial Emotion Recognition inspired by Bikramjot Singh Hanzra
# http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html

# For face detection we will use the Haar Cascade provided by OpenCV.
CASCADE_PATH = "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)

# For face recognition we will the the LBPH Face Recognizer
RECOGNIZER = cv2.createLBPHFaceRecognizer()

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

def saveUserFace(dct):
    """saveUserFace(dct) -> None"""
    # Format of dct: {"ANDREW_ID":{"sad":nparray, ...} ...}
    for andrew_id in dct:
        info = dct[andrew_id]
        for emotion in info:
            cv2.imwrite("faces/%s.%s.png"%(andrew_id, emotion),
                info[emotion])
            print "Saved user <%s> in [%s] state."%(andrew_id, emotion)

def trainRecognizer(images, labels):
    pass
"""
    # Path to the Yale Dataset
    path = './yalefaces'
    # Call the get_images_and_labels function and get the face images and the
    # corresponding labels
    images, labels = get_images_and_labels(path)
    cv2.destroyAllWindows()

    # Perform the tranining
    recognizer.train(images, np.array(labels))

    # Append the images with the extension .sad into image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]
    for image_path in image_paths:
        predict_image_pil = Image.open(image_path).convert('L')
        predict_image = np.array(predict_image_pil, 'uint8')
        faces = faceCascade.detectMultiScale(predict_image)
        for (x, y, w, h) in faces:
            nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
            nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
            if nbr_actual == nbr_predicted:
                print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
            else:
                print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)
            cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
            cv2.waitKey(1000)
"""

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
    im = _getCameraRaw()
    cv2.imshow("image", im)
    cv2.waitKey(0)
    #saveUserFace({"haowensh":{"happy":im}})
    a = getImagesAndLabels("faces")
    #print a

    cv2.destroyAllWindows()
