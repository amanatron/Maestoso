""" RUN THIS FILE TO START YOUR PROGRAM """


from tkinter import * 
import os
from os.path import join 
from tkinter import filedialog
from tkinter import messagebox
from main import Main 
from View import instrument_panel, toolbar, videoplayer, framerate_popup, theme_functions
from animator import Animator
from utility import delete_frames 
from theme_handler import import_theme 


# importing the MIDI file 
def open_file(): 
    file = filedialog.askopenfile(mode ='r', filetypes =[('Midi Files', '*.mid')]) 
    if file is not None: 
        filepath = file.name 
        filename = os.path.basename(filepath)
        main.filedir = filepath
        main.project_name = filename
        main.initialize_project() # run the initialization method from the initialize method in the main instance 
        root.title("Maestoso - {}".format(filename))
        filemenu.entryconfig(2, command = lambda: export_video(main.outputdir),state = ACTIVE)
        filemenu.entryconfig(3,command = lambda: [root.destroy(),delete_frames(main.outputdir)])
        preferences.entryconfig(1,state = ACTIVE)
        preferences.entryconfig(2,state = ACTIVE)
        
        #instance the three primary UI elements 

        instrumentpanel = instrument_panel.InstrumentPanel(root,main)
        videowindow = videoplayer.VideoPlayer(root,main.outputdir,main.fps)
        toolbar_project = toolbar.ToolBar(root,main,videowindow)

# export command - first checks the file size of the outputdir and then runs the animate function from Animator.py    
def export_video(outputdir):
    export_path = join(os.getcwd(),outputdir)
    if len([f for f in os.listdir(export_path)]) <= 1:
        messagebox.showerror("Export Error","Nothing to export")
        return 
    file = filedialog.asksaveasfilename(title = "Export Your Animation")
    if file is not None:
        animate = Animator(main.outputdir,main.fps,file)

if __name__ == "__main__":
    root = Tk()
    main = Main()
    icon = PhotoImage(file = f"{join(os.getcwd(),'MAESTOSO.png')}")
    root.iconphoto(False,icon)
    root.title("Maestoso")
    root.geometry("1440x900")
    root.configure(background='gray12')
    menubar = Menu(root)
    root.protocol("WM_DELETE_WINDOW",lambda: [root.destroy(),delete_frames(main.outputdir)])
    filemenu = Menu(menubar,tearoff = 0)
    preferences = Menu(menubar,tearoff=0)
    menubar.add_cascade(label='File',menu=filemenu)
    menubar.add_cascade(label = 'Preferences',menu = preferences)



    filemenu.add_command(label="Import Midi",command = lambda:open_file())
    filemenu.add_command(label="Import Theme", command = import_theme)
    filemenu.add_command(label="Export", state = DISABLED)
    filemenu.add_command(label="Exit",command = root.destroy)


    preferences.add_command(label = "Adjust Frame Rate",command = lambda: framerate_popup.create_render_toplevel(root,main))
    preferences.add_command(label = "Edit Selected Theme", command = lambda: theme_functions.customize_theme(root,main),state = DISABLED)
    preferences.add_command(label = "View Theme Description", command = lambda: theme_functions.display_theme_properties(root,main),state = DISABLED)

    root.configure(menu=menubar)
    root.resizable(0,0)


    root.mainloop()
