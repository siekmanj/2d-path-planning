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

def animate(obstacles, paths, bound_segments, waypoint_list, height, width):
    master = Tk()
    w = Canvas(master, width=width, height=height)
    w.pack()
    canvas_item_list = []
    for i in obstacles:
        item = w.create_oval(i.position.x + i.radius, i.position.y + i.radius, i.position.x - i.radius, i.position.y - i.radius, fill="red")
        canvas_item_list.append((i, item))
    move_obstacles(w, canvas_item_list)
    mainloop()

def move_obstacles(canvas, obstacle_list):
    for i in obstacle_list:
        i[0].position.x += i[0].xspd
        i[0].position.y += i[0].yspd
        canvas.move(i[1], i[0].position.x, i[0].position.y)
    canvas.after(100, move_obstacles(canvas, obstacle_list))
