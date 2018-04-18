from tkinter import *

def drawObstaclesPath(obstacles,paths,bound_segments,waypoint_list,height,width):
    #This is a function that will draw all of the obstacles in the obstacle list and the segments of the path

    # visualization stuff
    master = Tk()
    w = Canvas(master, width=width, height=height)
    w.pack()

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

    for segment in bound_segments:
        w.create_line(segment.startPos.x, segment.startPos.y, segment.endPos.x, segment.endPos.y, fill='red')
    mainloop()

