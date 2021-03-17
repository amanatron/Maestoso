""" THIS FILE STORES THE MAIN CLASS - MAIN FUNCTIONS AS A CONFIG FILE AND BEHAVES AS AN INSTANCE OF THE ENTIRE PROJECT """

from init_tracklist import TrackList
from tracklist_functions import find_pitch_range, create_timecode_hash
from utility import initialize_colours, return_random, delete_frames
from theme_handler import return_filenames
from importlib import import_module
from tkinter import messagebox


class Main:
    def __init__(self):
        self.filedir = '' #the file directory of the selected midi file 
        self.project_name = ''
        self.tracklist = '' #tracklist object 
        self.project_tracklist = '' #tracklist.track_list object 
        self.number_of_instruments = ''
        self.outputdir = 'PNG_EXPORTS' #the outputdir for all frames 
        self.PPQN = ''
        self.fps = 30
        self.endtime = ''
        self.preview_time = 45
    
    #this method initializes the entire project. It's run from the import menu in maestoso.py 
    def initialize_project(self):
        delete_frames(self.outputdir) #deletes all the files in the outputdir 
        self.selected_animation = ''
        try:
            self.tracklist = TrackList(self.filedir) #create an instances of Tracklist from the selected filedir 
        except RuntimeWarning:
            messagebox.showwarning("Improper Midi","Tempo, Key or Time signature change events found on non-zero tracks.  This is not a valid type 0 or type 1 MIDI file.  Tempo, Key or Time Signature may be wrong.")
        finally:
            self.tracklist = TrackList(self.filedir)
        self.project_tracklist = self.tracklist.track_list
        self.number_of_instruments = len(self.project_tracklist)
        initialize_colours(self.project_tracklist,return_random) #initialize the random colours assigned to each instrument* type 
        self.endtime = self.tracklist.midifile.get_end_time()
        self.theme_data = return_filenames(self.tracklist) #create an instance of all the themes and store them in a list 
        self.PPQN = self.tracklist.PPQN

    #this method is called every time the render button from toolbar.py is selected. 
    def animate(self,preview):
        delete_frames(self.outputdir) #delete any file in the outputdir 
        for i in self.theme_data:
            if i.display_name == self.selected_animation:
                theme = i
        #run the ANIMATE() method from the selected theme instance 
        theme.ANIMATE(self.project_tracklist,self.PPQN,self.fps,self.outputdir,preview,self.preview_time)





    

    



    





