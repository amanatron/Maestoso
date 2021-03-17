""" THIS FILE CONTAINS THE INSTRUMENTPANEL AND INSTRUMENTBLOCK CLASSES""" 

from tkinter import * 
from tkmacosx import Button as BT
import tkinter.font 
from tkinter import colorchooser
import os, sys 
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 
from utility import return_random, initialize_colours
from View import scrollable_frame 

#the main panel 
class InstrumentPanel:
    def __init__(self,root,main):
        #create a vertical scrollable canvas 
        self.scrollable = scrollable_frame.VerticalScrolledFrame(root, height = 900, width = 305, bg = 'gray12')
        self.scrollable.place(x = 0, y = 0, anchor = NW)
        self.create_panel(main)

    #create instrument panels from InstrumentBlock objects 
    def create_panel(self,main):
        for i in main.project_tracklist:
            instrument = InstrumentBlock(self.scrollable,main,i)



class InstrumentBlock:
    def __init__(self,parent,main,instrument):
        self.name = instrument.name
        self.colour = instrument.colour
        self.specialcode = instrument.specialcode #specialcode relating to the instrument class in init_tracklist.py 
        self.frame = Frame(parent,bg = "gray9", height = 100, width = 300, border = 1, relief = RIDGE)
        self.frame.pack(side = TOP)
        self.frame.pack_propagate(0)
        self.nametag = Label(self.frame,text = self.name,bg = "gray9", fg = "white")
        self.nametag.pack(side = TOP)
        self.lower_frame = Frame(self.frame, width = 300, height = 20, bg = "gray9") #the lower frame holding the colour and checkbox widgets 
        self.lower_frame.pack(side = BOTTOM)
        self.lower_frame.pack_propagate(0)
        self.create_colour_box(main)
        self.create_check_box(main)


    def create_colour_box(self,main):
        self.colour_box = BT(self.lower_frame, bg = self.colour, height = 20, width = 20, borderless = TRUE, command = lambda: self.change_colour(main))
        self.colour_box.pack(side = RIGHT)

    def create_check_box(self,main):
        self.checkvar = IntVar()
        self.check_box = Checkbutton(self.lower_frame, variable = self.checkvar, text = "Active", bg = "gray9", fg = "white", onvalue = 1, offvalue = 0, command = lambda: self.make_inactive(main))
        self.check_box.pack(side = RIGHT)
        self.check_box.select()

    def change_colour(self,main):
        color_code = colorchooser.askcolor(title = " Select Colour") 
        for i in main.project_tracklist:
            if i.specialcode == self.specialcode:
                i.colour = color_code[1]
                self.colour = i.colour
                self.colour_box.config(bg = self.colour)

    def make_inactive(self,main):
        for i in main.project_tracklist:
            if i.specialcode == self.specialcode:
                if self.checkvar.get() == 1:
                    i.active = True
                elif self.checkvar.get() == 0:
                    i.active = False 











    
























    







