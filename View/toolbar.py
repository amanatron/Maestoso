""" THIS FILE HOLDS THE TOOLBAR CLASS"""
from tkinter import * 
from tkinter.ttk import Combobox as Combo, Style
from tkinter import ttk
from tkmacosx import Button as BT
import os, sys 
import multiprocessing
import threading 
import time 
from View import runexcept
from tkinter import messagebox


currentdir = os.path.dirname(os.path.realpath(__file__)) #current directory 
parentdir = os.path.dirname(currentdir) #parent directory 

#function that triggers render 
def render_in_background(success,main,preview):
    try:
        main.animate(preview) #main.animate 
        success.value = True 
    except:
        success.value = True #regardless of the outcome, returns true 

#the toolbar class 
class ToolBar:
    def __init__(self,root,main,videowindow):
        ###### assigns icons #########
        self.rhythmicon = PhotoImage(file = os.path.join(parentdir,'View/Resources/Icons/rhythm.png'))
        self.polyphonyicon = PhotoImage(file = os.path.join(parentdir,'View/Resources/Icons/polyphony.png'))
        self.monophonyicon = PhotoImage(file = os.path.join(parentdir,'View/Resources/Icons/monophony.png'))
        self.harmonyicon  = PhotoImage(file = os.path.join(parentdir,'View/Resources/Icons/harmony.png'))
        self.rendericon = PhotoImage(file = os.path.join(parentdir,'View/Resources/Icons/render.png'))
        self.shuffleicon = PhotoImage(file = os.path.join(parentdir,'MAESTOSO.png'))

        ####### create all the necessary frames ####### 

        self.parentframe = Frame(root,bg = "gray9", width = 1125, height = 70, border = 3, relief = SUNKEN) #the main frame 
        self.parentframe.place(x = 315, y = 0) 
        self.parentframe.pack_propagate(0)

####################################################################################################################################################

        class ThemeSelection: #creates a dropdown list for the category of theme selected 
            def __init__(self,parent):
                #### creates a list of all display names from themes stored in main.theme_data  #####
                self.RHYTHM = [i.display_name for i in main.theme_data if i.category == 'RHYTHM']
                self.HARMONY = [i.display_name for i in main.theme_data if i.category == 'HARMONY']
                self.POLYPHONY = [i.display_name for i in main.theme_data if i.category == 'POLYPHONIC']
                self.MONOPHONY = [i.display_name for i in main.theme_data if i.category == 'MONOPHONIC']
                self.parent = parent 
                self.textvar = StringVar()
                self.construct_combobox()

                def adjust_comboboxstyle():
                    self.combostyle = ttk.Style()
                    self.combostyle.theme_create('combostyle', parent='alt',
                                settings = {'TCombobox':
                                            {'configure':
                                            {'selectbackground': 'purple',
                                            'fieldbackground': 'gray8',
                                            'background': 'gray4',
                                            'foreground': 'white'
                                            }}})
                    self.combostyle.theme_use('combostyle')

                try:
                    adjust_comboboxstyle()
                except:
                    pass # in case theme style already exists in the system

            #function to construct the combobox drop down menu 
            def construct_combobox(self):
                self.theme_selector = Combo(self.parent,width = 30, textvariable = self.textvar, state = 'disabled')
                self.theme_selector.set('Select a theme category')
                self.theme_selector.place(x = 700, y = 22)
                self.theme_selector.bind("<<ComboboxSelected>>",self.get_selected_value)

            #update combobox with the values based on category selected 
            def update_combobox(self,category):
                selections = {'RHYTHM':self.RHYTHM,'MONOPHONY':self.MONOPHONY,'POLYPHONY':self.POLYPHONY,'HARMONY':self.HARMONY}
                self.theme_selector.config(state = 'readonly')
                selected_category = selections.get(category)
                self.theme_selector['values'] = selected_category  

            #retrieve the selected value 
            def get_selected_value(self,event):
                selected = self.textvar.get()
                main.selected_animation = selected 
#######################################################################################################################################################
#initialize all buttons on top of the toolbar 


        self.combo_themes = ThemeSelection(self.parentframe) #combobox object containing all theme names  

        self.shufflebutton = BT(self.parentframe,image = self.shuffleicon, borderwidth = 0, height = 48, width = 48, borderless = TRUE, bg = "gray6", state = DISABLED)
        self.shufflebutton.pack(side = LEFT, padx = 30)

        self.rhythmbutton = BT(self.parentframe,image = self.rhythmicon, borderwidth = 0, height = 48, width = 48,borderless = TRUE, command = lambda:self.combo_themes.update_combobox('RHYTHM'))
        self.rhythmbutton.place(x = 400, y = 5.5)

        self.polyphonybutton = BT(self.parentframe,image = self.polyphonyicon, borderwidth = 0, height = 48, width = 48,borderless = TRUE,command = lambda:self.combo_themes.update_combobox('POLYPHONY'))
        self.polyphonybutton.place(x = 460, y = 5.5)

        self.monophonybutton= BT(self.parentframe,image = self.monophonyicon, borderwidth = 0, height = 48, width = 48,borderless = TRUE,command = lambda:self.combo_themes.update_combobox('MONOPHONY'))
        self.monophonybutton.place(x = 520, y = 5.5)

        self.harmonybutton = BT(self.parentframe,image = self.harmonyicon, borderwidth = 0, height = 48, width = 48,borderless = TRUE,command = lambda:self.combo_themes.update_combobox('HARMONY'))
        self.harmonybutton.place(x = 580, y = 5.5)

        self.renderbutton = BT(self.parentframe,image = self.rendericon, borderwidth = 0, height = 48, width = 48,borderless = TRUE, command = lambda:self.if_render_click(root,main,videowindow))
        self.renderbutton.pack(side = RIGHT, padx = 20)


#######################################################################################################################################################

    def if_render_click(self,root,main,videowindow): #if the render button is clicked 
        if not runexcept.check_typerror_render(main): #run the check_typerror func from runexcept.py 
            return 
        else:
            self.render_toplevel(root,main,videowindow) #else run the render_toplevel method 

        
    def render_toplevel(self,root,main,videowindow): # creates the top level pop when render is clicked 
        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()
        x_pos = root_x + 500
        y_pos = root_y + 200

        top = Toplevel(bg = 'gray9') 
        top.geometry(f'500x300+{x_pos}+{y_pos}')
        top.resizable(0,0)
        top.title("Render Animation")
        top.grab_set()

        def start_render(preview):
            top.destroy()
            self.renderbutton.config(state = DISABLED)
            videowindow.while_render()

            try:
                multiprocessing.set_start_method('spawn')
            except:
                pass 
            success = multiprocessing.Value('i',False)
            process = multiprocessing.Process(target = render_in_background,args = (success,main,preview)) #run the render in background function on a seperate process 
            process.start()

            t1 = threading.Thread(target = videowindow.generate_loading_screen, args = (main,preview)) #thread the loading screen func 
            t1.start()

            while True:
                root.update_idletasks()
                root.update()
                if success.value:
                    break 
            try:
                videowindow.display_video()
                messagebox.showinfo("RENDER SUCCESFUL","RENDER SUCCESFUL! Scroll through the frames to see your animation.")
                self.renderbutton.config(state = ACTIVE) 
            except:
                messagebox.showerror("Render Error", "There was some issue running your animation. Please try using another theme. You can report the bug on github.com")
                self.renderbutton.config(state = ACTIVE) 
                return 

        #############################################################################################################################
        #create the toplevel popup when render is clicked 

        def select_time(*args):
            main.preview_time = self.clicked.get() #select preview time 

        toptitleframe = Frame(top,height = 50, width = 500, bg = "gray6")
        toptitleframe.pack(side = TOP)
        toptitleframe.propagate(0)
        topcenterframe = Frame(top,height = 200, width = 500, bg = "gray9")
        topcenterframe.pack(side = TOP)
        topcenterframe.propagate(0)
        topbottomframe = Frame(top,height = 50, width = 500, bg = "gray6")
        topbottomframe.pack(side = BOTTOM)
        topbottomframe.propagate(0)

        top_title = Label(toptitleframe, text = "Select the Type of Render", bg = "gray6", fg = "white")
        top_title.pack(side = TOP)

        self.previewbutton = BT(topcenterframe, borderwidth = 0, height = 48, width = 80,borderless = TRUE, text = "Preview", bg = "gray6", fg = "white", relief = GROOVE, command = lambda: start_render(preview = True))
        self.previewbutton.place(x = 160, y = 60) #the commands defer by the value of preview 

        self.fullrenderbutton = BT(topcenterframe, borderwidth = 0, height = 48, width = 80,borderless = TRUE, text = "Full Render", bg = "gray6", fg = "white", relief = GROOVE,command = lambda: start_render(preview = False))
        self.fullrenderbutton.place(x = 260, y = 60)

        preview_time_label = Label(topcenterframe,text = "Choose a preview duration (in seconds)", bg = "gray9", fg = "white")
        preview_time_label.pack(side = BOTTOM)


        self.clicked = IntVar()
        self.clicked.set(main.preview_time)

        self.items = [3,5,10,15,30,45,60] #all the preview values 

        self.preview_time = Combo(topbottomframe,width = 30, textvariable = self.clicked)
        self.preview_time['values'] = self.items 
        self.preview_time.bind("<<ComboboxSelected>>",select_time)
        self.preview_time.pack(side = TOP)



        
    


