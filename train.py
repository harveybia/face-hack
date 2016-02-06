
from tkinter import *
from PIL import ImageTk, Image
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
    data.imgCenter1 = (w / 2, 720 / 2)
    data.imgCenter2 = (w / 2 + w, 720 / 2)
    data.imgCenter3 = (w / 2 + 2*w, 720 / 2)
    data.imgCenter4 = (w / 2 + 3*w, 720 / 2)
    data.imgCenter5 = (w / 2 + 4*w, 720 / 2)
    
def loadImage(data):
    data.disgustBW = ImageTk.PhotoImage(Image.open("disgustBW.jpg"))
    data.happyBW = ImageTk.PhotoImage(Image.open("happyBW.jpg"))
    data.angerBW = ImageTk.PhotoImage(Image.open("angerBW.jpg"))
    data.fearBW = ImageTk.PhotoImage(Image.open("fearBW.jpg"))
    data.sadBW = ImageTk.PhotoImage(Image.open("sadBW.jpg"))
    data.sad = ImageTk.PhotoImage(Image.open("sad.jpg"))
    data.happy = ImageTk.PhotoImage(Image.open("happy.jpg"))
    data.anger = ImageTk.PhotoImage(Image.open("anger.jpg"))

def trainMousePressed(event, data):
    # use event.x and event.y

    if (event.x < data.margin3 and event.x > data.margin2): #Happy
        data.highLightHappy = not data.highLightHappy
        if (data.highLightHappy == True):
            data.highLightSad = False
            data.highLightAnger = False
    if (event.x < data.margin4 and event.x > data.margin3): #Sad
        data.highLightSad = not data.highLightSad
        if (data.highLightSad == True):
            data.highLightHappy = False
            data.highLightAnger = False
    if (event.x < data.margin5 and event.x > data.margin4): #anger
        data.highLightAnger = not data.highLightAnger
        if (data.highLightAnger == True):
            data.highLightHappy = False
            data.highLightSad = False

#def trainKeyPressed(event, data):
    # use event.char and event.keysym
    #if (data.highlightHappy):
     #   if (event.keysym == "c"):
      #      happyFace = facial._getCameraRaw()
       #     saveUserFace({"andrewID":{"happy":happyFace}})
    #if (data.highLightSad):
     #   if (event.keysym == "c"):
      #      sadFace = facial._getCameraRaw()
       #     saveUserFace({"andrewID":{"sad":sadFace}})
    #if (data.highLightAnger):
       # if (event.keysym == "c"):
        #    angerFace = facial._getCameraRaw()
         #   saveUserFace({"andrewID":{"anger":angerFace}})

def trainTimerFired(data):
    pass

def trainRedrawAll(canvas, data):
    # draw in canvas
    canvas.create_image(data.imgCenter1, image = data.disgustBW)
    canvas.create_image(data.imgCenter5, image = data.fearBW)
    # First Create the two that we won't change in this project
    if (data.highLightHappy):
        canvas.create_image(data.imgCenter2, image = data.happy)
    if (not data.highLightHappy):
        canvas.create_image(data.imgCenter2, image = data.happyBW)
    if (data.highLightSad):
        canvas.create_image(data.imgCenter3, image = data.sad)
    if (not data.highLightSad):
        canvas.create_image(data.imgCenter3, image = data.sadBW)
    if (data.highLightAnger):
        canvas.create_image(data.imgCenter4, image = data.anger)
    if (not data.highLightAnger):
        canvas.create_image(data.imgCenter4, image = data.angerBW)


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
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
