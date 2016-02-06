from Tkinter import *
import cv2
from PIL import Image, ImageTk
import time
import facial
import os
import threading
import tkSimpleDialog
import database as db
global canvas

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

    data.utilButtonList = [
    data.button.BACK,
    data.button.EXIT,
    data.button.SETTINGS]

#######################################
# Button Functions
#######################################
def BACK(root,data):
    print ":::Performing BACK Segue"
    if data.mode == "TRAIN":
        global canvas
        loadingFace = ImageTk.PhotoImage(Image.open(data.utilPicPath+"loadingFace.png"))
        canvas.delete(ALL)
        canvas.create_image(data.center,image=loadingFace)       
        canvas.update()
        train()
    if data.prevMode != []:
        data.mode = data.prevMode.pop(-1)
    


def EXIT(root,data):
    data.terminate = True
    exit(root,data)

def SETTINGS(root,data):
    data.prevMode.append(data.mode)
    data.mode = "TRAIN"
    trainInit(data)

def SIDEBAR1(root,data):
    if data.mainEmotion == facial.EMO_HAPPY:
        data.prevMode.append(data.mode)
        data.mode = "HAPPYS1"
        happyS1Init(data)
    elif data.mainEmotion == facial.EMO_SAD:
        data.prevMode.append(data.mode)
        data.mode = "SADS1"
        sadS1Init(data)
    elif data.mainEmotion == facial.EMO_ANGRY:
        data.prevMode.append(data.mode)
        data.mode = "ANGRYS1"
        angryS1Init(data)

def SIDEBAR2(root,data):
    if data.mainEmotion == facial.EMO_HAPPY:
        data.prevMode.append(data.mode)
        data.mode = "HAPPYS2"
        happyS2Init(data)
    elif data.mainEmotion == facial.EMO_SAD:
        data.prevMode.append(data.mode)
        data.mode = "SADS2"
        sadS2Init(data)
    elif data.mainEmotion == facial.EMO_ANGRY:
        data.prevMode.append(data.mode)
        data.mode = "ANGRYS2"
        angryS2Init(data)

def SIDEBAR3(root,data):
    if data.mainEmotion == facial.EMO_HAPPY:
        data.prevMode.append(data.mode)
        data.mode = "HAPPYS3"
        happyS3Init(data)
    elif data.mainEmotion == facial.EMO_SAD:
        data.prevMode.append(data.mode)
        data.mode = "SADS3"
        sadS3Init(data)
    elif data.mainEmotion == facial.EMO_ANGRY:
        data.prevMode.append(data.mode)
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
    data.prevMode = []
    data.utilPicPath = "utilitypic/"
    createButton(data)
    

def train():
    dct = facial.getImagesAndLabels("faces")
    facial.MAPPING = facial.trainRecognizer(dct)
    
def initModes(data):
    mainInit(data)

def exit(root, data):
    data.terminate = True
    root.destroy()
    facial.CAMERA.release()

def mousePressed(root, event, data):
    # use event.x and event.y
    if not data.terminate:
        if data.mode == "TRAIN":
            trainMousePressed(root, event, data)
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
        if data.mode == "TRAIN":
            trainKeyPressed(root, event, data)
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
        if data.mode == "TRAIN":
            trainTimerFired(root,data)
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
    if data.prevMode: print data.prevMode

def redrawAll(root, canvas, data):
    if not data.terminate:
        if data.mode == "TRAIN":
            trainRedrawAll(root, canvas, data)
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
# Train Mode
########################################
def enterAndrewId(data):
    data.andrewID = tkSimpleDialog.askstring("You Are ...", "AndrewID")


def trainInit(data):
    # load data.xyz as appropriate
    w = 1080 / 5
    data.width = 1080
    data.height = 720
    (data.margin1, data.margin2) = (0, w)
    (data.margin3, data.margin4) = (2 * w, 3 * w)
    (data.margin5, data.margin6) = (4 * w, 5 * w)
    data.highLightHappy = False
    data.highLightSad = False
    data.highLightAngry = False
    data.selectHappy = False
    data.selectSad = False
    data.selectAngry = False
    data.imgCenter1 = (w / 2, 720 / 2)
    data.imgCenter2 = (w / 2 + w, 720 / 2)
    data.imgCenter3 = (w / 2 + 2*w, 720 / 2)
    data.imgCenter4 = (w / 2 + 3*w, 720 / 2)
    data.imgCenter5 = (w / 2 + 4*w, 720 / 2)
    data.utilPicPath = "utilitypic/"
    data.happySaveSuccess = False
    data.sadSaveSuccess = False
    data.angrySaveSuccess = False
    loadImage(data)
    enterAndrewId(data)
    
def loadImage(data):
    data.disgustNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"disgustNewBW.jpg"))
    data.happyNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"happyNewBW.jpg"))
    data.angryNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"angryNewBW.jpg"))
    data.fearNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"fearNewBW.jpg"))
    data.sadNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"sadNewBW.jpg"))
    data.sadNew = ImageTk.PhotoImage(Image.open(data.utilPicPath+"sadNew.jpg"))
    data.happyNew = ImageTk.PhotoImage(Image.open(data.utilPicPath+"happyNew.jpg"))
    data.angryNew = ImageTk.PhotoImage(Image.open(data.utilPicPath+"angryNew.jpg"))

def trainMousePressed(root, event, data):
    # use event.x and event.y

    if (event.x < data.margin3 and event.x > data.margin2): #Happy
        data.selectHappy = not data.selectHappy
        if (data.selectHappy == True):
            data.selectSad = False
            data.selectAngry = False
    elif (event.x < data.margin4 and event.x > data.margin3): #Sad
        data.selectSad = not data.selectSad
        if (data.selectSad == True):
            data.selectHappy = False
            data.selectAngry = False
    elif (event.x < data.margin5 and event.x > data.margin4): #angry
        data.selectAngry = not data.selectAngry
        if (data.selectAngry == True):
            data.selectHappy = False
            data.selectSad = False
    if (event.x < data.margin3 and event.x > data.margin2): #Happy
        data.highLightHappy = not data.highLightHappy
        if (data.highLightHappy == True):
            data.highLightSad = False
            data.highLightAngry = False
    elif (event.x < data.margin4 and event.x > data.margin3): #Sad
        data.highLightSad = not data.highLightSad
        if (data.highLightSad == True):
            data.highLightHappy = False
            data.highLightAngry = False
    elif (event.x < data.margin5 and event.x > data.margin4): #angry
        data.highLightAngry = not data.highLightAngry
        if (data.highLightAngry == True):
            data.highLightHappy = False
            data.highLightSad = False
    if data.happySaveSuccess: data.highLightHappy = True
    if data.sadSaveSuccess: data.highLightSad = True
    if data.angrySaveSuccess: data.highLightAngry = True

def trainKeyPressed(root,event, data):
    # use event.char and event.keysym
    if (data.selectHappy):
       if (event.keysym == "c"):
           happyFace = facial._getCameraRaw()
           facial.saveUserFace({data.andrewID:{"happy":happyFace}})
           data.happySaveSuccess = True
    if (data.selectSad):
       if (event.keysym == "c"):
           sadFace = facial._getCameraRaw()
           facial.saveUserFace({data.andrewID:{"sad":sadFace}})
           data.sadSaveSuccess = True
    if (data.selectAngry):
       if (event.keysym == "c"):
           angryFace = facial._getCameraRaw()
           facial.saveUserFace({data.andrewID:{"angry":angryFace}})
           data.angrySaveSuccess = True
    if (event.keysym == "Escape"):
        data.button.BACK.function(root, data)



def trainTimerFired(root,data):
    pass

def trainRedrawAll(root,canvas, data):
    # draw in canvas
    canvas.create_image(data.imgCenter1, image = data.disgustNewBW)
    canvas.create_image(data.imgCenter5, image = data.fearNewBW)
    # First Create the two that we won't change in this project
    if (data.highLightHappy):
        canvas.create_image(data.imgCenter2, image = data.happyNew)
    if (not data.highLightHappy):
        canvas.create_image(data.imgCenter2, image = data.happyNewBW)
    if (data.highLightSad):
        canvas.create_image(data.imgCenter3, image = data.sadNew)
    if (not data.highLightSad):
        canvas.create_image(data.imgCenter3, image = data.sadNewBW)
    if (data.highLightAngry):
        canvas.create_image(data.imgCenter4, image = data.angryNew)
    if (not data.highLightAngry):
        canvas.create_image(data.imgCenter4, image = data.angryNewBW)

########################################
# Main Function: Emotion Recognition
########################################
def mainInit(data):
    data.mainWait = 0.5 # seconds
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
    
    data.snapshot = facial.getCameraSnapShot()
    time = data.mainCounter * data.timerDelay # in milli seconds
    if time % (data.mainWait * 1000) == 0:
        print 98765467897654678654123123
        emotion, prob = facial.getUserEmotion()# facial.EMO_SAD #
        if emotion != facial.EMO_NOTFOUND or prob > 0.5:
            data.mainEmotion = emotion
        print data.mainEmotion
    data.mainCounter = (data.mainCounter + 1) % 10000

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    data.HAPPYS3flag = True

def happyS3MousePressed(root, event, data):
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)
    if data.HAPPYS3flag: 
        db.newBrowserTab("http://www.rottentomatoes.com")
        data.HAPPYS3flag = False

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    data.SADS3flag = True

def sadS3MousePressed(root, event, data):
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)
    if data.SADS3flag:
        db.newBrowserTab("https://www.youtube.com/watch?v=Zwef7-CuZlg")
        data.SADS3flag = False

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    for button in data.utilButtonList:
        if button.inBounds(event.x, event.y):
            button.function(root,data)

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
    init(data)
    # create the root and the canvas
    root = Tk()
    root.title("Outside In")
    initModes(data)

    global canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    loadingFace = ImageTk.PhotoImage(Image.open(data.utilPicPath+"NAME.png"))
    canvas.delete(ALL)
    canvas.create_image(data.center,image=loadingFace)       
    canvas.update()
    train()
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
