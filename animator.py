""" THIS FILE CONTAINS THE ANIMATOR CLASS"""


import cv2
import numpy as np
import glob
import os 
from tkinter import messagebox

#animator class 
class Animator:
    #combines all frames within the outputdir and writes them into video 
    def __init__(self,image_folder,fps,filenameuser):
        try:
            path = image_folder
            img_array = []
            filenames = []
            for count in range(len(os.listdir(path))-1):
                filename = f'{path}/frame_{count}.png'
                filenames.append(filename) #append filename to filenames list 
                img = cv2.imread(filename) #read the image file 
                height, width, layers = img.shape #retrieve height, width from img 
                size = (width,height)
                img_array.append(img) #add img to the img_array list 
            out = cv2.VideoWriter(f'{filenameuser}.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size) #filename = user assigned file name 
            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()
            messagebox.showinfo("EXPORT SUCCESSFUL!","EXPORT SUCCESSFUL!")
        except:
            messagebox.showerror("Export Error","No Animation to Export")


    








