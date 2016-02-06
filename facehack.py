from Tkinter import *
import cv2
from PIL import Image, ImageTk
import facial
import pyglet
import os
import threading

#######################################
# Button Class
#######################################
class Data(object): pass

class Button(object):

    def __init__(self,x,y,f):
        self.x = x
        self.y = y
        self.function = f
        self.fill = None

class RoundButton(Button):
    def __init__(self, x, y, r, f):
        super(RoundButton,self).__init__(x,y,f)
        self.r = r

    def inBounds(self,x,y):
        return ((self.x - x)**2 + (self.y - y)**2)**0.5 <= self.r

    def draw(self,canvas,data):
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.fill,width=5)

class RectButton(Button):
    def __init__(self, x, y, width, height,f):
        super(RectButton,self).__init__(x,y,f)
        self.width = width
        self.height =height

    def inBounds(self,x,y):
        return ((self.x - self.width / 2 < x < self.x + self.width) and 
                (self.y - self.height / 2 < y < self.y + self.height / 2))

    def draw(self,canvas,data):
        canvas.create_rectangle(self.x-self.width//2,self.y-self.height//2,self.x+self.width//2,self.y+self.height//2,fill=self.fill,width=5)

def createButton(data):
    data.button = Data()
    data.button.BACK = RoundButton(912,44,25,BACK)
    data.button.EXIT = RoundButton(1033,44,25,EXIT)
    data.button.SETTINGS = RoundButton(791,44,25,SETTINGS)
    data.button.SIDEBAR1 = RectButton(903,160,300,68,SIDEBAR1)
    data.button.SIDEBAR2 = RectButton(903,293,300,68,SIDEBAR2)
    data.button.SIDEBAR3 = RectButton(903,428,300,68,SIDEBAR3)
    data.button.NEXTSONG = RoundButton(786,658,25,NEXTSONG)
    

    data.mainButtonList = [
    data.button.BACK,
    data.button.EXIT,
    data.button.SETTINGS,
    data.button.SIDEBAR1,
    data.button.SIDEBAR2,
    data.button.SIDEBAR3,
    data.button.NEXTSONG]

#######################################
# Button Functions
#######################################
def BACK(root,data):
    if data.prevMode != None:
        data.mode = data.prevMode

def EXIT(root,data):
    data.terminate = True
    exit(root,data)

def SETTINGS(root,data):
    data.prevMode = data.mode
    data.mode = "TRAIN"

def SIDEBAR1(root,data):
    if data.mainEmotion == facial.EMO_HAPPY:
        data.prevMode = data.mode
        data.mode = "HAPPYS1"
        happyS1Init(data)
    elif data.mainEmotion == facial.EMO_SAD:
        data.prevMode = data.mode
        data.mode = "SADS1"
        sadS1Init(data)
    elif data.mainEmotion == facial.EMO_ANGRY:
        data.prevMode = data.mode
        data.mode = "ANGRYS1"
        angryS1Init(data)

def SIDEBAR2(root,data):
    if data.mainEmotion == facial.EMO_HAPPY:
        data.prevMode = data.mode
        data.mode = "HAPPYS2"
        happyS2Init(data)
    elif data.mainEmotion == facial.EMO_SAD:
        data.prevMode = data.mode
        data.mode = "SADS2"
        sadS2Init(data)
    elif data.mainEmotion == facial.EMO_ANGRY:
        data.prevMode = data.mode
        data.mode = "ANGRYS2"
        angryS2Init(data)

def SIDEBAR3(root,data):
    if data.mainEmotion == facial.EMO_HAPPY:
        data.prevMode = data.mode
        data.mode = "HAPPYS3"
        happyS3Init(data)
    elif data.mainEmotion == facial.EMO_SAD:
        data.prevMode = data.mode
        data.mode = "SADS3"
        sadS3Init(data)
    elif data.mainEmotion == facial.EMO_ANGRY:
        data.prevMode = data.mode
        data.mode = "ANGRYS3"
        angryS3Init(data)

def NEXTSONG(root,data):
    pass

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
    data.prevMode = None
    data.utilPicPath = "utilitypic/"
    createButton(data)
    
def initModes(data):
    mainInit(data)

def exit(root, data):
    data.terminate = True
    root.destroy()
    facial.CAMERA.release()

def mousePressed(root, event, data):
    # use event.x and event.y
    if not data.terminate:
        # if data.mode == "TRAIN":
        #     trainMousePressed(root, event, data)
        if data.mode == "MAIN":
            mainMousePressed(root, event, data)

        if data.mode == "HAPPYS1":
            happyS1MousePressed(root, event, data)
        if data.mode == "HAPPYS2":
            happyS2MousePressed(root, event, data)
        if data.mode == "HAPPYS3":
            happyS3MousePressed(root, event, data)

        if data.mode == "SADS1":
            sadS1MousePressed(root, event, data)
        if data.mode == "SADS2":
            sadS2MousePressed(root, event, data)
        if data.mode == "SADS3":
            sadS3MousePressed(root, event, data)

        if data.mode == "ANGRYS1":
            angryS1MousePressed(root, event, data)
        if data.mode == "ANGRYS2":
            angryS2MousePressed(root, event, data)
        if data.mode == "ANGRYS3":
            angryS3MousePressed(root, event, data)
        pass

def keyPressed(root, event, data):
    if not data.terminate:
        # use event.char and event.keysym
        if event.keysym == "q":
            exit(root, data)
        # if data.mode == "TRAIN":
        #     trainKeyPressed(root, event, data)
        if data.mode == "MAIN":
            mainKeyPressed(root, event, data)

        if data.mode == "HAPPYS1":
            happyS1KeyPressed(root, event, data)
        if data.mode == "HAPPYS2":
            happyS2KeyPressed(root, event, data)
        if data.mode == "HAPPYS3":
            happyS3KeyPressed(root, event, data)

        if data.mode == "SADS1":
            sadS1KeyPressed(root, event, data)
        if data.mode == "SADS2":
            sadS2KeyPressed(root, event, data)
        if data.mode == "SADS3":
            sadS3KeyPressed(root, event, data)

        if data.mode == "ANGRYS1":
            angryS1KeyPressed(root, event, data)
        if data.mode == "ANGRYS2":
            angryS2KeyPressed(root, event, data)
        if data.mode == "ANGRYS3":
            angryS3KeyPressed(root, event, data)
        pass

def timerFired(root, data):
    if not data.terminate:
        # if data.mode == "TRAIN":
        #     trainTimerFired(root,data)
        if data.mode == "MAIN":
            mainTimerFired(root, data)

        if data.mode == "HAPPYS1":
            happyS1TimerFired(root, data)
        if data.mode == "HAPPYS2":
            happyS2TimerFired(root, data)
        if data.mode == "HAPPYS3":
            happyS3TimerFired(root, data)

        if data.mode == "SADS1":
            sadS1TimerFired(root, data)
        if data.mode == "SADS2":
            sadS2TimerFired(root, data)
        if data.mode == "SADS3":
            sadS3TimerFired(root, data)

        if data.mode == "ANGRYS1":
            angryS1TimerFired(root, data)
        if data.mode == "ANGRYS2":
            angryS2TimerFired(root, data)
        if data.mode == "ANGRYS3":
            angryS3TimerFired(root, data)
        pass

def redrawAll(root, canvas, data):
    if not data.terminate:
        # if data.mode == "TRAIN":
        #     trainRedrawAll(root, canvas, data)
        if data.mode == "MAIN":
            mainRedrawAll(root, canvas, data)

        if data.mode == "HAPPYS1":
            happyS1RedrawAll(root, canvas, data)
        if data.mode == "HAPPYS2":
            happyS2RedrawAll(root, canvas, data)
        if data.mode == "HAPPYS3":
            happyS3RedrawAll(root, canvas, data)

        if data.mode == "SADS1":
            sadS1RedrawAll(root, canvas, data)
        if data.mode == "SADS2":
            sadS2RedrawAll(root, canvas, data)
        if data.mode == "SADS3":
            sadS3RedrawAll(root, canvas, data)

        if data.mode == "ANGRYS1":
            angryS1RedrawAll(root, canvas, data)
        if data.mode == "ANGRYS2":
            angryS2RedrawAll(root, canvas, data)
        if data.mode == "ANGRYS3":
            angryS3RedrawAll(root, canvas, data)
        pass

########################################
# Main Function: Emotion Recognition
########################################
def mainInit(data):
    data.mainWait = 1 # seconds
    data.mainEmotion = None
    loadEmotionPic(data)


def loadEmotionPic(data):
    data.sad = ImageTk.PhotoImage(file=data.utilPicPath+"sad.png")
    data.happy = ImageTk.PhotoImage(file=data.utilPicPath+"happy.png")
    data.angry = ImageTk.PhotoImage(file=data.utilPicPath+"angry.png")

def loadMP3():
    global angryMP3 
    angryMP3 = {}
    for mp3 in os.listdir("music/angry"):
        if mp3.endswith("mp3"):
            angryMP3[mp3] = pyglet.media.load("music/angry/" + mp3,streaming=False)

    global happyMP3
    happyMP3 = {}
    for mp3 in os.listdir("music/happy"):
        if mp3.endswith("mp3"):
            happyMP3[mp3] = pyglet.media.load("music/happy/" + mp3,streaming=False)

    global sadMP3
    sadMP3 = {}
    for mp3 in os.listdir("music/sad"):
        print mp3
        if mp3.endswith("mp3"):
            sadMP3[mp3] = pyglet.media.load("music/sad/" + mp3,streaming=False)
    
# thread1 = threading.Thread(target=loadMP3())qq
# thread1.start()

def mainMousePressed(root, event, data):
    for button in data.mainButtonList:
        if button.inBounds(event.x,event.y):
            button.function(root,data)
            # if button.fill == None: button.fill="white"
            # elif button.fill == "white": button.fill = None


def mainKeyPressed(root, event, data):
    pass

def mainTimerFired(root, data):
    data.mainCounter = (data.mainCounter + 1) % 10000
    data.snapshot = facial.getCameraSnapShot()
    time = data.mainCounter * data.timerDelay / 1000 # in seconds
    if time % data.mainWait == 0:
        data.mainEmotion = "EMO_ANGRY"# facial.getUserEmotion()

def mainRedrawAll(root, canvas, data):
    canvas.create_image((540,360), image=data.snapshot)
    # implement figure on the left
    if data.mainEmotion == facial.EMO_SAD:
        canvas.create_image(data.center, image=data.sad)
    if data.mainEmotion == facial.EMO_HAPPY:
        canvas.create_image(data.center, image=data.happy)
    if data.mainEmotion == facial.EMO_ANGRY:
        canvas.create_image(data.center, image=data.angry)

########################################
# HAPPYS1
########################################
def happyS1Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def happyS1MousePressed(root, event, data):
    pass

def happyS1KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def happyS1TimerFired(root, data):
    pass

def happyS1RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# HAPPYS2
########################################
def happyS2Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def happyS2MousePressed(root, event, data):
    pass

def happyS2KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def happyS2TimerFired(root, data):
    pass

def happyS2RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# HAPPYS3
########################################
def happyS3Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def happyS3MousePressed(root, event, data):
    pass

def happyS3KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def happyS3TimerFired(root, data):
    pass

def happyS3RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# SADS1
########################################
def sadS1Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def sadS1MousePressed(root, event, data):
    pass

def sadS1KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def sadS1TimerFired(root, data):
    pass

def sadS1RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# SADS2
########################################
def sadS2Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def sadS2MousePressed(root, event, data):
    pass

def sadS2KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def sadS2TimerFired(root, data):
    pass

def sadS2RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# SADS3
########################################
def sadS3Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def sadS3MousePressed(root, event, data):
    pass

def sadS3KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def sadS3TimerFired(root, data):
    pass

def sadS3RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# ANGRYS1
########################################
def angryS1Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def angryS1MousePressed(root, event, data):
    pass

def angryS1KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def angryS1TimerFired(root, data):
    pass

def angryS1RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# angryS2
########################################
def angryS2Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def angryS2MousePressed(root, event, data):
    pass

def angryS2KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def angryS2TimerFired(root, data):
    pass

def angryS2RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))

########################################
# angryS3
########################################
def angryS3Init(data):
    exec("data.%sbg = ImageTk.PhotoImage(file=data.utilPicPath+'%s.png')" 
         % (data.mode, data.mode))

def angryS3MousePressed(root, event, data):
    pass

def angryS3KeyPressed(root, event, data):
    if event.keysym == "Escape":
        data.button.BACK.function(root,data)

def angryS3TimerFired(root, data):
    pass

def angryS3RedrawAll(root, canvas, data):
    canvas.create_image(data.center,image=eval("data.%sbg" % data.mode))


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
