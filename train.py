from Tkinter import *
from PIL import ImageTk, Image
import tkSimpleDialog
import facial


####################################
# customize these functions
####################################
def init(data):
    trainInit(data)
def timerFired(data):
    trainTimerFired(data)
def mousePressed(event, data):
    trainMousePressed(event, data)
def redrawAll(canvas, data):
    trainRedrawAll(canvas, data)

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
    data.highLightAnger = False
    data.selectHappy = False
    data.selectSad = False
    data.selectAnger = False
    data.imgCenter1 = (w / 2, 720 / 2)
    data.imgCenter2 = (w / 2 + w, 720 / 2)
    data.imgCenter3 = (w / 2 + 2*w, 720 / 2)
    data.imgCenter4 = (w / 2 + 3*w, 720 / 2)
    data.imgCenter5 = (w / 2 + 4*w, 720 / 2)
    data.utilPicPath = "face-hack/utilitypic/"
    data.happySaveSuccess = False
    data.sadSaveSuccess = False
    data.angerSaveSuccess = False
    
def loadImage(data):
    data.disgustNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"disgustNewBW.jpg"))
    data.happyNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"happyNewBW.jpg"))
    data.angerNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"angerNewBW.jpg"))
    data.fearNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"fearNewBW.jpg"))
    data.sadNewBW = ImageTk.PhotoImage(Image.open(data.utilPicPath+"sadNewBW.jpg"))
    data.sadNew = ImageTk.PhotoImage(Image.open(data.utilPicPath+"sadNew.jpg"))
    data.happyNew = ImageTk.PhotoImage(Image.open(data.utilPicPath+"happyNew.jpg"))
    data.angerNew = ImageTk.PhotoImage(Image.open(data.utilPicPath+"angerNew.jpg"))

def trainMousePressed(event, data):
    # use event.x and event.y

    if (event.x < data.margin3 and event.x > data.margin2): #Happy
        data.selectHappy = not data.selectHappy
        if (data.selectHappy == True):
            data.selectSad = False
            data.selectAnger = False
    elif (event.x < data.margin4 and event.x > data.margin3): #Sad
        data.selectSad = not data.selectSad
        if (data.selectSad == True):
            data.selectHappy = False
            data.selectAnger = False
    elif (event.x < data.margin5 and event.x > data.margin4): #anger
        data.selectAnger = not data.selectAnger
        if (data.selectAnger == True):
            data.selectHappy = False
            data.selectSad = False
    if (event.x < data.margin3 and event.x > data.margin2): #Happy
        data.highLightHappy = not data.highLightHappy
        if (data.highLightHappy == True):
            data.highLightSad = False
            data.highLightAnger = False
    elif (event.x < data.margin4 and event.x > data.margin3): #Sad
        data.highLightSad = not data.highLightSad
        if (data.highLightSad == True):
            data.highLightHappy = False
            data.highLightAnger = False
    elif (event.x < data.margin5 and event.x > data.margin4): #anger
        data.highLightAnger = not data.highLightAnger
        if (data.highLightAnger == True):
            data.highLightHappy = False
            data.highLightSad = False
    if data.happySaveSuccess: data.highLightHappy = True
    if data.sadSaveSuccess: data.highLightSad = True
    if data.angerSaveSuccess: data.highLightAnger = True

def trainKeyPressed(event, data):
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
    if (data.selectAnger):
       if (event.keysym == "c"):
           angerFace = facial._getCameraRaw()
           facial.saveUserFace({data.andrewID:{"anger":angerFace}})
           data.angerSaveSuccess = True

def trainTimerFired(data):
    pass

def trainRedrawAll(canvas, data):
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
    if (data.highLightAnger):
        canvas.create_image(data.imgCenter4, image = data.angerNew)
    if (not data.highLightAnger):
        canvas.create_image(data.imgCenter4, image = data.angerNewBW)


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        trainRedrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        trainMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
            trainKeyPressed(event, data)
            redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        trainTimerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    loadImage(data)
    enterAndrewId(data)
    

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run(1640, 500)
