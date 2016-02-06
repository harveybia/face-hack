from Tkinter import *
import cv2
from PIL import Image, ImageTk
import facial
import pyglet
import os
import threading

# Animation framework from CMU 15-112 course page:
# https://www.cs.cmu.edu/~112/notes/events-example0.py

########################################
# Modes
########################################
def init(data):
    data.center = 540,360
    data.timerDelay = 10
    data.mainCounter = 0
    data.terminate = False
    data.mode = "MAIN"
    data.utilPicPath = "Utility Pictures/"

def initModes(data):
    mainInit(data)

def exit(root, data):
    data.terminate = True
    root.destroy()
    facial.CAMERA.release()

def mousePressed(root, event, data):
    # use event.x and event.y
    if not data.terminate:
        pass

def keyPressed(root, event, data):
    if not data.terminate:
        # use event.char and event.keysym
        if event.keysym == "q":
            exit(root, data)

def timerFired(root, data):
    if not data.terminate:
        if data.mode == "MAIN":
            mainTimerFired(root, data)

def redrawAll(root, canvas, data):
    if not data.terminate:
        # test facial lib
        if data.mode == "MAIN":
            mainRedrawAll(root, canvas, data)


########################################
# Main Function: Emotion Recognition
########################################
def mainInit(data):
    data.mainWait = 1 # seconds
    data.mainEmotion = None
    data.mainBar = ImageTk.PhotoImage(file=data.utilPicPath+"no_signal.png")
    data.mainBarPos = (1000,500)
    loadEmotionPic(data)


def loadEmotionPic(data):
    data.sad = ImageTk.PhotoImage(file=data.utilPicPath+"test_sad.png")
    data.happy = ImageTk.PhotoImage(file=data.utilPicPath+"happy.png")
    data.angry = ImageTk.PhotoImage(file=data.utilPicPath+"angry.png")

def loadMP3(data):
    data.angryMP3 = {}
    for mp3 in os.listdir("music/angry"):
        if mp3.endswith("mp3"):
            data.angryMP3[mp3] = pyglet.media.load("music/angry/" + mp3,streaming=False)
            data.angryMP3[mp3].play()

    data.happyMP3 = {}
    for mp3 in os.listdir("music/happy"):
        if mp3.endswith("mp3"):
            data.happyMP3[mp3] = pyglet.media.load("music/happy/" + mp3,streaming=False)
    data.sadMP3 = {}
    for mp3 in os.listdir("music/sad"):
        if mp3.endswith("mp3"):
            data.sadMP3[mp3] = pyglet.media.load("music/sad/" + mp3,streaming=False)
    

def mainTimerFired(root, data):
    data.mainCounter = (data.mainCounter + 1) % 10000
    data.snapshot = facial.getCameraSnapShot()
    time = data.mainCounter * data.timerDelay / 1000 # in seconds
    if time % data.mainWait == 0:
        data.mainEmotion = facial.getUserEmotion()

def mainRedrawAll(root, canvas, data):
    canvas.create_image((540,360), image=data.snapshot)
    # implement bar at the right
    canvas.create_image(data.mainBarPos, image=data.mainBar)

    canvas.create_image(data.center, image=data.sad)
    canvas.image = data.sad
    # implement figure on the left
    if data.mainEmotion == facial.EMO_SAD:
        canvas.create_image(data.center, image=data.sad)
    if data.mainEmotion == facial.EMO_HAPPY:
        canvas.create_image(data.center, image=data.happy)
    if data.mainEmotion == facial.EMO_ANGRY:
        canvas.create_image(data.center, image=data.angry)
    # implement music

    # implement recommendations


########################################
# Run Function
########################################
def run(width=300, height=300):
    def mousePressedWrapper(root, event, canvas, data):
        if not data.terminate:
            mousePressed(root, event, data)
            redrawAllWrapper(root, canvas, data)

    def keyPressedWrapper(root, event, canvas, data):
        if not data.terminate:
            keyPressed(root, event, data)
            redrawAllWrapper(root, canvas, data)


    def redrawAllWrapper(root, canvas, data):
        if not data.terminate:
            canvas.delete(ALL)
            redrawAll(root, canvas, data)
            canvas.update()

    def timerFiredWrapper(root, canvas, data):
        if not data.terminate:
            timerFired(root, data)
            redrawAllWrapper(root, canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, root, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    initModes(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(root, event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(root, event, canvas, data))
    timerFiredWrapper(root, canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("Exited.")

if __name__ == '__main__':
    run(1080,720)
