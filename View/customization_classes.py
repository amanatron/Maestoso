""" THIS FILE HOLDS ALL THE CUSTOMIZABLE CLASSES FOR THEMES"""

from tkinter import * 
from tkmacosx import Button as BT
from tkinter import colorchooser

"""
All widgets created in this file follow a pattern that must be followed for a seamless functionality across various scripts. 

1) Their attributes must all be the same: the standard attr are self.name, self.default_val, self.selection, self.r, self.c, and self.parent_frame 
2) They must all contain a self.construct() method 


"""
# THE COLORBOX WIDGET 
class ColorButton:
    def __init__(self,name,default_val,r,c,parent_frame):
        self.name = name #the name of the widget - used as a label in the theme_functions.py file 
        self.default_val = default_val #the default value of the widget 
        self.selection = '' #the attr the selected value is assigned to 
        self.r = r #row  
        self.c = c #column
        self.parent_frame = parent_frame #the parent frame that holds the widget 

    #all widgets must have a construct method that creates the entire widget to be called from theme_functions.py 
    def construct(self):
        self.colour_box = BT(self.parent_frame, bg = self.default_val, height = 20, width = 20, borderless = TRUE, command = lambda: self.change_colour())
        self.colour_box.grid(row = self.r, column = self.c, sticky = W)
        self.colourlabel = Label(self.parent_frame,text = self.name, bg = "gray9", fg = 'white')
        self.colourlabel.grid(row = self.r, column = self.c + 1, sticky = W)

    #changes colour of the widget and adds that value to the self.selection attr 
    def change_colour(self):
        color_code = colorchooser.askcolor(title = " Select Colour")
        self.selection = color_code[1]
        self.colour_box.config(bg = self.selection)

#THE DROPDOWN WIDGET 
class Dropdown:
    def __init__(self,name,default_val,items,r,c,parent_frame):
        self.name = name
        self.default_val = default_val 
        self.items = items 
        self.clicked = StringVar()
        self.clicked.set(self.default_val)
        self.selection = ''
        self.r = r 
        self.c = c
        self.parent_frame = parent_frame

    def construct(self):
        self.dropdown = OptionMenu(self.parent_frame, self.clicked,*self.items, command = self.change_selection)
        self.dropdown["menu"].config(bg = "gray9")
        self.dropdown.grid(row = self.r, column = self.c, sticky = W)
        self.dropdownlabel = Label(self.parent_frame,text = self.name, bg = "gray9", fg = 'white')
        self.dropdownlabel.grid(row = self.r, column = self.c + 1, sticky = W)

    #sets the value of self.selection to the selected item 
    def change_selection(self,event):
        self.selection = self.clicked.get()

#THE CHECKBOX WIDGET 
class CheckBox:
    def __init__(self,name,default_val,r,c,parent_frame):
        self.name = name 
        self.default_val = default_val
        self.checkvar = IntVar()
        self.selection = ''
        self.r = r
        self.c = c
        self.parent_frame = parent_frame

    def construct(self):
        self.checkbox = Checkbutton(self.parent_frame, variable = self.checkvar, bg = "gray9", fg = "white", onvalue = 1, offvalue = 0, command = self.change_value)
        if self.default_val == True:
            self.checkbox.select()
        self.checkbox.grid(row = self.r, column = self.c, sticky = W)
        self.checklabel = Label(self.parent_frame,text = self.name, bg = "gray9", fg = 'white')
        self.checklabel.grid(row = self.r, column = self.c + 1, sticky = W)

    def change_value(self):
        if self.checkvar.get() == 1:
            self.selection = True 
        elif self.checkvar.get() == 0:
            self.selection = False 

#THE ENTRY BOX WIDGET 
        """
        The entry widget allows for both str and int type values. self.type holds the entry type
        """
class EntryBox:
    def __init__(self,name,default_val,r,c,parent_frame,entry_limit,entry_range,entry_type):
        self.name = name 
        self.default_val = default_val 
        self.r = r 
        self.c = c 
        self.parent_frame = parent_frame
        self.range = entry_range #the range of digits - stored as a tuple() where range[0] is the starting value and range[1] is the max value
        self.type = entry_type
        if entry_limit < 2: #the number of chars that are allowed 
            self.limit = 2
        else:
            self.limit = entry_limit
            
        self.selection = ''
        self.checkvar = StringVar()
        if self.type == 'int':
            self.checkvar.trace('w',self.limit_range) #call this method for integer values 
        elif self.type == 'str':
            self.checkvar.trace('w',self.limit_entry) #call this method for str values 

        self.checkvar.set(self.default_val)

    def construct(self):
        self.entry = Entry(self.parent_frame,bg = "gray9", fg = "white", textvariable = self.checkvar,width = self.limit)
        self.entry.grid(row = self.r, column = self.c, sticky = W)
        self.entrylabel = Label(self.parent_frame,text = self.name, bg = "gray9", fg = 'white')
        self.entrylabel.grid(row = self.r, column = self.c + 1, sticky = W)
    
    def limit_entry(self,*args):
        value = self.checkvar.get()
        try:
            float(value)
            self.checkvar.set("") #if the inserted value is an int 
        except:
            if len(value) > self.limit: # if lenth of letters is greater than self.limit 
                self.checkvar.set(value[:self.limit])

    def limit_range(self,*args):
        value = self.checkvar.get()
        try: 
            float(value) #if the value is either a float or an int 
        except: 
            self.checkvar.set("") #if value is not an int or float 
            return 
        if float(value) < float(self.range[0]) or float(value) > float(self.range[1]):
            self.checkvar.set(0)




