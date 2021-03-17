''' GENERAL FUNCTIONS ''' 

import random 
import os 

def frame_rate_note(note_duration,frame_rate):
    """[RETURNS THE NUMBER OF FRAMES THAT ADD UP TO ANY PARTICULAR NOTE DURATION]

    Args:
        note_duration ([int]): [note value obtained from tracklist.instrument.notes]

    Returns:
        [int]: [number of frames]
    """
    return round(frame_rate * note_duration)


def frames_to_second(frames,frame_rate):
    """[RETURNS THE INVERSE OF frame_rate_note]

    Args:
        frames ([int): [numbers of frames passed]
        frame_rate ([int]): [fps]

    Returns:
        [bool]: [seconds]
    """
    return (frames/frame_rate)

''' COLOUR PALLETE AND ASSIGNMENT FUNCTION ''' 

def return_random(number_of_instruments, itemslist):
    array = [i for i in range(len(itemslist))]
    n = len(array)
    for i in range(n-1,0,-1):
        j = random.randint(0,i+1)
        array[i],array[j] = array[j],array[i]

    return array[0:number_of_instruments]

# assigns randomc colours to instruments upon initialization 
def initialize_colours(project_tracklist,return_random):
    colour_pallete = ['#ff124f', '#ff00a0','#fe75fe','#7a04eb','#120458','#ff6e27','#fbf665','#00b3fe','#9cf862','#383e65','#defe47'] #colour pallete specific to the Maestoso style 
    number_of_instruments = len(project_tracklist)
    if number_of_instruments <= len(colour_pallete): 
        random_colour = return_random(number_of_instruments, colour_pallete)
        for i in range(number_of_instruments):
            project_tracklist[i].colour = colour_pallete[random_colour[i]]
    else:
        random_colour = []
        for i in range(number_of_instruments):
            random_colour.append(random.choice(range(len(colour_pallete))))
        for i in range(number_of_instruments):
            project_tracklist[i].colour = colour_pallete[random_colour[i]]

#picks and returns a random colour from the colour pallete 
def pick_random_colour():
    colour_pallete = ['#ff124f', '#ff00a0','#fe75fe','#7a04eb','#120458','#ff6e27','#fbf665','#00b3fe','#9cf862','#383e65','#defe47']
    return random.choice(colour_pallete)


def delete_frames(outputdir):
    #deletes all files titled "frame_{number}" from a given outputdir 
    path = os.path.join(os.getcwd(),outputdir)
    for count in range(len(os.listdir(path))-1):
        try: 
            os.remove(f'{path}/frame_{count}.png')
        except:
            pass 
        
def max_frame_number(outputdir):
    #returns the total size of the given outputdir 
    path = outputdir 
    return len(os.listdir(path)) - 2




