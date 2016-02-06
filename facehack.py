from Tkinter import *
from facial import *

# Animation framework from CMU 15-112 course page:
# https://www.cs.cmu.edu/~112/notes/events-example0.py

########################################
# Modes
########################################
def init(data):
    data.timerDelay = 10
    data.counter = 0
    data.terminate = False
    data.mode = "MAIN"

def exit(root, data):
    global CAMERA
    data.terminate = True
    root.destroy()
    CAMERA.release()

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
        data.counter += 1
        data.snapshot = getCameraSnapShot()

def redrawAll(root, canvas, data):
    if not data.terminate:
        # test facial lib
        if data.mode == "MAIN":
            mainRedrawAll(root, canvas, data)
    

########################################
# Main Function: Emotion Recognition
########################################

def mainRedrawAll(root, canvas, data):
    canvas.create_image((540,360), image=data.snapshot)

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