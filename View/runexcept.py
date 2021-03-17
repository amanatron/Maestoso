""" THIS FILE CONTAINS THE CHECK_TYPERROR_RENDER FUNCTION""" 

from tkinter import messagebox
from tracklist_functions import create_chord_list

def check_typerror_render(main):
    if main.selected_animation == '':
        messagebox.showerror("Render Error", "No animation has been selected.")
        return False 
    
    #check if the file contains the relevent information for the animation to even run... This function is called to avoid scripts incapable of processing the necessary data from running 
    for i in main.theme_data:
        if i.display_name == main.selected_animation:
            if i.category == 'RHYTHM':
                if not check_if_rhythmic(main,state = True):
                    messagebox.showerror("Theme Error ","No drum track was found. Please select a more suitable theme.")
                    return False 
                else:
                    return True 
            elif i.category == 'POLYPHONIC' or i.category == 'MONOPHONIC':
                if not check_if_pitch_based(main):
                    messagebox.showerror("Theme Error ","No pitch based track was found. Please select a more suitable theme.")
                    return False 
                else:
                    return True 
            else:
                if not check_if_harmonic(main):
                    messagebox.showerror("Theme Error ","No harmonic information was detected. Please select a more suitable theme.")
                    return False 
                else:
                    return True 

#check if the midi file contains even a single drum track - an easy alternative to this function would be to simply check the drum_count attr from tracklist 
def check_if_rhythmic(main,state = True):
    counter = 0 
    for i in main.project_tracklist:
        if i.isdrum:
            counter += 1 

    if state == True:
        if counter == 0:
            return False
        else:
            return True 
    else: 
        return counter 

#check if the midi file contains only drum tracks - an easy alternative to this function would be to simply check the drum_count attr from tracklist 
def check_if_pitch_based(main):
    if check_if_rhythmic(main,state = False) == main.number_of_instruments:
        return False
    else:
        return True 

#check if the midi file contains any harmonic information
def check_if_harmonic(main):
    if len(create_chord_list(main.project_tracklist,main.PPQN)) == 0:
        return False
    else:
        return True 
    

