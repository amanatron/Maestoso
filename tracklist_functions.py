''' FUNCTIONS ASSOCIATED WITH TRACKLIST ''' 

from pretty_midi import note_number_to_drum_name, note_number_to_name
from pychord import note_to_chord

def find_pitch_range(tracklist): 
    """[RETURNS AN ORDERED NON-REPEATING LIST OF ALL PITCHES THAT LIE BETWEEN THE MIN AND MAX PITCH IN TRACKLIST]

    Args:
        tracklist ([Project_Tracklist class])

    Returns:
        [list]: [ordered pitches in the tracklist]
    """
    notes = []
    for i in tracklist:
        if i.isdrum == False:
            for j in i.notes:
                notes.append(j.pitch)

    max_note = max(notes)
    min_note = min(notes)
    pitch_range = [i for i in range(min_note,max_note + 1)]
    return pitch_range


def find_pitch_range_monophonic(monophonic):
    """[RETURNS AN ORDERED NON-REPEATING LIST OF ALL PITCHES THAT LIES BETWEEN THE MIN AND MAX PITCH IN A MONOPHONIC MELODY]

    Args:
        monophonic ([list]): [Monophonic]

    Returns:
        [list]: [pitch range]
    """
    notes = [i.pitch for i in monophonic] 
    max_note = max(notes)
    min_note = min(notes)
    pitch_range = [i for i in range(min_note,max_note + 1)]
    return pitch_range 


def create_timecode_hash(tracklist): # creates a polyphonic dictionary
    """[CREATES A POLYPHONIC DICTIONARY WHERE ALL NOTES THAT OCCUR ON THE SAME ONSET ARE STORED AS VALUES IN THE ONSET KEY]

    Args:
        tracklist ([tracklist.track_list): [tracklist attr of Tracklist]

    Returns:
        [dict]: [key:value pairs where key = onset and values = all notes that occur at the onset]
    """
    polyphonic_hash = {}
    timecodes = []

    for i in tracklist:
        if i.active == True:
            if i.isdrum == False:
                for j in i.notes:
                    timecodes.append(j.start_time)
                    j.colour = i.colour # add note colour attribute to Note class 
                    j.specialcode = i.specialcode #add a unique identifier to each note 
    timecodes_nonrepeating = list(set(timecodes))
    timecodes_nonrepeating.sort()
    for i in timecodes_nonrepeating:
        polyphonic_hash.update({i:[]})
    
    for i in tracklist:
        if i.active == True:
            if i.isdrum == False:
                for j in i.notes:
                    polyphonic_hash[j.start_time].append(j)
    
    return polyphonic_hash
    

def create_monophonic(polyphonic_hash):
    """[DERIVES A MONOPHONIC MELODY FROM A POLYPHONIC DICTIONARY]

    Args:
        polyphonic_hash ([dict): [polyphonic map created from the create_timecode_hash func]

    Returns:
        [list]: [all the notes that best fit the monophonic layout of the music]
    """
    monophonic_list = []
    for k, v in polyphonic_hash.items():
        temp_list = []
        for note in v:
            temp_list.append(note.pitch)
        temp_list = list(set(temp_list)) #remove all repeating pitch values 
        index = temp_list.index(max(temp_list))
        monophonic_list.append(v[index])
    return monophonic_list


def create_drum_hash(tracklist): 
    """[CREATES A DRUM MAP OF ALL PERCUSSIVE NOTES THAT OCCUR AT THE SAME ONSET]

    Args:
        tracklist ([tracklist.track_list): [tracklist attr of Tracklist]

    Returns:
        [dict]: [key:value pairs where key = onset and values = all notes that occur at the onset]
    """
    drum_hash = {}
    timecodes = []

    for i in tracklist:
        if i.isdrum == True and i.active == True:
            for j in i.notes:
                timecodes.append(j.start_time)
                j.colour = i.colour #assigns the note colour from selected instrument colour 
    #isolate only the non-repeating onsets 
    timecodes_nonrepeating = list(set(timecodes))
    timecodes_nonrepeating.sort()
    for i in timecodes_nonrepeating:
        drum_hash.update({i:[]})

    for i in tracklist:
        if i.isdrum == True and i.active == True:
            for j in i.notes:
                drum_hash[j.start_time].append(j)

    return drum_hash 


def find_all_drums(tracklist,name = False): # finds all the unique drum samples within the tracklist if array = True else returns the number of drum samples
    """[FINDS ALL THE UNIQUE DRUM SAMPLES FROM DRUM INSTRUMENTS]

    Args:
        tracklist ([Tracklist.track_list]): [tracklist attr of Tracklist]
        name (bool, optional): [set to true if you want the function to return a list with name instead of pitch values]. Defaults to False.

    Returns:
        [list]: [all unique drum names/pitches]
    """
    midi_list = []
    count = 1
    for i in tracklist:
        if i.isdrum == True:
            if i.active == True:
                for j in i.notes:
                    if name == True:
                        try:
                            midi_list.append(note_number_to_drum_name(j.pitch))
                        except:
                            midi_list.append(f"Drum {count}")
                            count += 1
                    else:
                        midi_list.append(j.pitch)

    update_list = list(set(midi_list))
    return update_list



def create_chord_list(project_tracklist,PPQN):
    """[CREATES A LIST OF CHORDS FROM LIST]

    Args:
        project_tracklist ([Tracklist.track_list]): [tracklist attr of Tracklist]
        PPQN ([int]): [PPQN value required to estimate note duration]

    Returns:
        [list]: [returns a chord object list]
    """
    polyphonic_hash = create_timecode_hash(project_tracklist) #create a polyphonic hash from the create_timecode_hash func 
    chord_list = []
    # create a chord class 
    class Chord:
        def __init__(self,name,notes,start_time,end_time):
            self.name = name #chord name 
            self.notes = notes #list of notes within the chord 
            self.start_time = start_time
            self.end_time = end_time 

    # this function converts pitch numbers to pitch names
    def convert_number_to_note(pitch_list):
        final_name_list = []
        for i in pitch_list:
            note_name = note_number_to_name(i)
            if len(note_name) == 3:
                #remove the octave value from the str
                upd_note_name = note_name.replace(note_name[2],'')
            elif len(note_name) == 2:
                upd_note_name = note_name.replace(note_name[1],'')
            final_name_list.append(upd_note_name)

        return final_name_list
    
    #this function evaluates the weight of the given note - this is done to reduce chances of errors in chord retrieval 
    def evaluate_note_weight(lst):
        counter = 0 
        for i in lst:
            tick_duration = (i.end_ticks - i.start_ticks)/PPQN
            if tick_duration >= 0.25: #if note value is greater than 0.25 - or quaver 
                counter += 1 
        if counter == len(lst):
            return True 
        else:
            return False 

    for k, v in polyphonic_hash.items():
        if len(set(v)) > 2: #if there are more than 2 unique pithces in a given value list 
            if evaluate_note_weight(v) == True: #if all notes are greater than or equal to eight note value 
                pitch_list = [i.pitch for i in v] #create a list of pitches 
                pitch_list.sort() #sort the pitches in order 
                chord_pitches = list(set(convert_number_to_note(pitch_list))) #convert pitch_list to a list of notes 
                if len(chord_pitches) > 2:
                    if len(note_to_chord(chord_pitches)) != 0:
                        chord_name = note_to_chord(chord_pitches)[0]._chord #obtain chord name using the note_to_chord function in pychord 
                    else:
                        chord_name = ''
                    end_time = max([i.end_time for i in v])
                    chord_list.append(Chord(chord_name,chord_pitches,k,end_time))
                else:
                    continue 
            else:
                continue 
        else:
            continue 

    return chord_list 


            




    


            





        


