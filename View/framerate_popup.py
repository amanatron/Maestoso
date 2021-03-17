""" THIS FILE CREATES THE SELECT FRAME RATE TOP LEVEL"""

from tkinter import * 

def create_render_toplevel(root,main):
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    x_pos = root_x + 500
    y_pos = root_y + 200
    top = Toplevel(bg = 'gray9')
    top.geometry(f'500x300+{x_pos}+{y_pos}')
    top.resizable(0,0)
    top.title("Adjust Frame Rate")
    top.grab_set()

    descriptiontop = Label(top,text = "Select the desired frame rate", bg = "gray9", fg = "white")
    descriptiontop.pack(side = TOP)

    framerates = [24,25,30,60]

    def selected():
        selection = var.get()
        main.fps = selection
        notification = Label(top, text = f"{selection} fps has been selected. Close this window when you're satisfied.",bg = "gray9", fg = "white")
        notification.place(y = 200, x = 50)

    var = IntVar()
    add = 0 
    for i in framerates:
        rb = Radiobutton(top, text = f'{i} fps', variable = var, value = i, command = selected,bg = "gray9", fg = 'white')
        rb.place(x = 10 + add, y = 150)
        add += 125