from Tkinter import *

# a = getUserEmotion()
# b = getCameraSnapShot()
# print a
# print b
class Struct(): pass

########################################
# Initialization
########################################
def init(root, data):
    data.width = 1920
    data.height = 1080
    root.after()

    pass

########################################
# Main Loop
########################################
def main(root, data):
     def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    root.mainloop()

    pass

########################################
# Clean Up
########################################
def cleanup(root, data):
    root.destroy()
    pass

if __name__ == '__main__':
    root = Tk()
    data = Struct()
    init(root, data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    main(root, data)
