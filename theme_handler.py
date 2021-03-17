""" THIS FILE HANDLES ALL THE IMPORTS AND INITIALIZATIONS OF THEMES FROM THE "THEMES" DIRECTORY """

from os import listdir, replace
from os.path import isfile, join, dirname, abspath,basename
from importlib import import_module
from tkinter import filedialog, messagebox

#this function initializes all files within the "THEMES" directory 
def return_filenames(tracklist):
    current_path = dirname(abspath(__file__))
    mypath = join(current_path,'THEMES')
    filelist = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #list of themes 
    theme_list = []
    #list of themes that failed to load 
    errored_themes = []
    for i in filelist:
        if i != '__init__.py' and i != '.DS_Store':
            try:
                #replace the file extension from the theme file name 
                filename = i.replace('.py','')
                mod = import_module(f'.{filename}',package='THEMES') # import module 
                #get the class attr 
                mod_class = getattr(mod,filename)
                theme = mod_class(tracklist)
                theme_list.append(theme)
            except:
                #append themes that failed to errored_themes 
                errored_themes.append(filename)

    if len(errored_themes) > 0:
        messagebox.showwarning("Import Error", "The following themes failed to import: {}".format(errored_themes))
                
    return theme_list 

# this function handles the import of themes. It takes a selected theme and places it in the "THEME" directory 
def import_theme():
    file = filedialog.askopenfile(mode ='r', filetypes =[('Maestoso Themes', '*.py')])
    if file is not None:
        import_warning  = messagebox.askokcancel("Import Warning", "Maestoso themes are directly imported as .py scripts. Never import an unknown script or one that hasn't been directly downloaded from www.maestoso.app - Do you still wish to continue?")
        if import_warning == 0:
            return 
        filepath = file.name 
        filename = basename(filepath)
        current_path = dirname(abspath(__file__))
        mypath = join(current_path,'THEMES')
        new_theme_path = join(mypath,filename)
        replace(filepath,new_theme_path)







