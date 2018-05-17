from tkinter import *
import tkinter as tk
from time import sleep

def drawObstaclesPath(obstacles,paths,bound_segments,waypoint_list,height,width,mapFilename):
    #This is a function that will draw all of the obstacles in the obstacle list and the segments of the path

    # visualization stuff
    master = Tk()
    master.attributes('-fullscreen', False)



    w = Canvas(master, width=width, height=height)
    w.pack()


    filename = PhotoImage(
        file=mapFilename)

    w.create_image(0, 0, image=filename, anchor=tk.NW)
    # draw the obstacles on the canvas
    for i in obstacles:
        w.create_oval(i.position.x + i.radius, i.position.y + i.radius, i.position.x - i.radius,
                      i.position.y - i.radius, fill="red")

    for wayp in waypoint_list:
        w.create_oval(wayp.x+5,wayp.y+5,wayp.x-5,wayp.y-5, fill = 'green')

    colors = ['orange','blue','green']
    for i in range(len(paths)):
        for segment in paths[i]:
            w.create_line(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y,fill=colors[i],width = 5)
            master.update()
            sleep(0.1)

    for segment in bound_segments:
        w.create_line(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y, fill='red')


    def closeWindow(event):
        master.destroy()

    master.bind("w", closeWindow)

    #master.mainloop()

    #while True:
    #    master.update()
    #    sleep(1)

