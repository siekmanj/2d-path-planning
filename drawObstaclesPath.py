from tkinter import *

def drawObstaclesPath(obstacles,paths,height,width):
    #This is a function that will draw all of the obstacles in the obstacle list and the segments of the path

    # visualization stuff
    master = Tk()
    w = Canvas(master, width=width, height=height)
    w.pack()

    # draw the obstacles on the canvas
    for i in obstacles:
        w.create_oval(i.position.x + i.radius, i.position.y + i.radius, i.position.x - i.radius,
                      i.position.y - i.radius, fill="red")


    colors = ['orange','blue','green']
    for i in range(len(paths)):
        for segment in paths[i]:
            print("DRAWING AT " + str(segment.startPos.x) + ", " + str(segment.startPos.y) + " TO " + str(segment.endPos.x) + ", " + str(segment.endPos.y))
            w.create_line(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y,fill=colors[i])

    mainloop()

