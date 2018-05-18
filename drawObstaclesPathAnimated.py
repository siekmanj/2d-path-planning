from tkinter import *
import tkinter as tk
from time import sleep

def drawObstaclesPathAnimated(obstacles,paths,bound_segments,waypoint_list,height,width,mapFilename,posTimes,height_latitude, width_longitude, top_latitude, left_longitude):
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

    for segment in bound_segments:
        w.create_line(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y, fill='red')

    colors = ['orange','blue','green']
#    for i in range(len(paths)):
#        for segment in paths[i]:
#            print('Drawing line from ({0},{1}) to ({2},{3})'.format(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y))
#            w.create_line(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y,fill=colors[i],width = 5)
#            master.update()
#            sleep(0.1)

    for i in range(posTimes[0].size):
        scale_x = width / width_longitude
        scale_y = height / height_latitude
        x = -1*scale_x*(posTimes[0][i] - left_longitude)
        y = -1*scale_y*(posTimes[1][i] - top_latitude)

        if (i < posTimes[0].size - 1):
            dtime = posTimes[3][i + 1] - posTimes[3][i]

        print('Processing point ({0},{1}) with velocity {2} and time {3}'.format(x, y, posTimes[2][i], posTimes[3][i]))
        w.create_oval(x - 2, y - 2, x + 2, y + 2, fill='cyan',width=1)
        master.update()
        sleep(dtime)
        



    def closeWindow(event):
        master.destroy()

    master.bind("w", closeWindow)

    #mainloop is still needed because it blocks the window from closing
    master.mainloop()

    #while True:
    #    master.update()
    #    sleep(1)


