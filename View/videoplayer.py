""" THIS FILE HOLDS THE VIDEOPLAYER CLASS"""

from tkinter import * 
import cv2
from PIL import ImageTk, Image
from os import getcwd, listdir
from os.path import join 
from utility import max_frame_number, frame_rate_note

#create a videoplayer class 
class VideoPlayer:
    def __init__(self,root,outputdir,fps):
        self.parentframe = Frame(root,bg = "gray12", width = 1125, height = 830, relief = SUNKEN, bd = 5) #the main frame 
        self.parentframe.place(x = 315, y = 70, anchor = NW)
        self.parentframe.pack_propagate(0)
        self.bottomframe = Frame(self.parentframe,bg = "gray10", width = 1125, height = 110) #the frame that holds the slider 
        self.bottomframe.pack(side = BOTTOM)
        self.bottomframe.pack_propagate(0)
        self.slider = Scale(self.bottomframe, orient = HORIZONTAL, length = 1125, bg = "gray12", fg = "white",state = DISABLED) #create a slider 
        self.slider.pack(side = TOP)
        self.outputdir = join(getcwd(),outputdir) #create a path to the outputdir 

        self.generate_text_labels()

    #this method creates the appropriate text labels on the parent frame 
    def generate_text_labels(self, text = True):
        if text == True:
            content = "Everything seems so empty...why not do something about it?"
        else:
            content = ""
        self.rendertext = Label(self.parentframe,text = content , bg = "gray12", fg = "white")
        self.rendertext.place(x = 350, y = 450)
        self.loading_text = Label(self.parentframe,bg = "gray12", fg = "white")
        self.loading_text.place(x = 450, y = 600)


    #this method updates self.image_display depending on the val retrieved from self.slider 
    def update_image(self,val):
        self.frame.config(file = f'{self.outputdir}/frame_{val}.png')
        self.image_display.config(image = self.frame)

    #this method is called from toolbar.py when the animation is render 
    def display_video(self):
        self.slider.set(0) #set slider value to 0 
        self.slider.config(state = ACTIVE, command = lambda val : self.update_image(val)) #active slider
        self.max_frame = round(max_frame_number(self.outputdir)) #the max_frame count retrieved using the max_frame_number func from utility.py
        self.slider.config(from_=0, to = self.max_frame)
        self.frame = PhotoImage(file = f'{self.outputdir}/frame_0.png') 
        self.image_display = Label(self.parentframe, image = self.frame)
        self.image_display.pack()
        self.image_display.config(image = self.frame)

    #this function runs when render is called from toolbar.py... it disables the slider and destroys three widgets from the screen 
    def while_render(self):
        self.slider.config(state = DISABLED)
        try:
            self.loading_text.destroy()
            self.rendertext.destroy()
            self.image_display.destroy()
        except:
            pass 
            
    #the loading screen function
    def generate_loading_screen(self,main,preview):
        dir_size = len([f for f in listdir(self.outputdir)]) - 1 #retrieve the size of the directory 
        self.parentframe.after(5000) #wait for 5 seconds in order to avoid collision in case main.animate returns an error 
        if len([f for f in listdir(self.outputdir)]) - 1 == dir_size: #check if the main function returned an error 
            return 

        self.generate_text_labels(text = False) #create text labels 
        
        endtime = main.endtime 
        fps = main.fps 
        prev_time = main.preview_time 
        minimum_frames = 0.75 # a safe number to minimize bugs due to discrepencies
        self.rendertext.config(text = " " * 22 + "Rendering your animation...Please be patient.")
        if preview == True and prev_time <= endtime:
            est_frame_count = frame_rate_note(prev_time,fps)
        else:
            est_frame_count = frame_rate_note(endtime,fps)

        dir_size = len([f for f in listdir(self.outputdir)]) - 1
        while dir_size < est_frame_count * minimum_frames:
            prog_percentage = round((dir_size * 100)/(est_frame_count * minimum_frames))
            self.loading_text.config(text = f'-----------------{prog_percentage}% completed') #Update self.loading text with the prog_percentage val 
            dir_size = len([f for f in listdir(self.outputdir)]) - 1

        self.rendertext.config(text = " " * 22 + "Almost there....Just hang in there soldier.")


        



             















    

        




