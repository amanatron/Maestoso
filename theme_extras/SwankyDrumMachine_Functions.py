import matplotlib.pyplot as plt 
import matplotlib.patches as patches 
from math import sqrt
import random

instrument_general_midi = {"Bass":(35,36),"Snare":(37,38,39,40),
    "Tom":(41,43,45,47,48,50),"HH":(42,46),"Crash":(52,51,53),
    "PercA":(54,58,56,80,82,72,70,69) #Will be used with diagonal shaker anim
    ,"PercB":(60,61,62,63) # Will be used with circular percussive anim
    ,"PercC":(76,77,73,74,75,56,65,66,64,67,68) # Will be used with triangle anim
    ,"SpecialFx":(44,49,55,27,28,29,30,31,32,34) #Sweeping Animations and their variations
    ,"SpecialFx2":(84,83,58) # Shimmer effects
    }

def find_instrument_shape(note_number):
    for k, v in instrument_general_midi.items():
        for j in v:
            if j == note_number:
                return k 
    return "default instrument"

def return_entity_height(width,category,height):
    if category == "Snare":
        return width 
    elif category == "HH" or category == "Crash":
        return width/4 
    elif category == "PercA":
        return width * 1.5 

    elif category == "default instrument":
        return width * (9/16)

    else:
        return height 

instrument_to_animation = {"Bass":["expand","bounce"],"Snare":["bounce","shake","slide"],
    "Tom":["bounce","shake","slide"],"HH":["shake","roll"],"Crash":["shake","roll"],
    "PercA":["shake","slide"] #Will be used with diagonal shaker anim
    ,"PercB":["expand","bounce","jump and roll"] # Will be used with circular percussive anim
    ,"PercC":["shake","roll","jump and roll","slide"] # Will be used with triangle anim
    ,"SpecialFx":["shake","slide"] #Sweeping Animations and their variations
    ,"SpecialFx2":["bounce","shake","slide"],"default instrument":["bounce","shake","slide"]} # Shimmer effects


def fetch_ideal_animation(note_number):
    shape = find_instrument_shape(note_number)
    lst = instrument_to_animation.get(shape)
    return random.choice(lst)

instrument_to_shape = {"Bass":"circle","Snare":"square",
    "Tom":"mid circle","HH":"ellipse","Crash":"ellipse",
    "PercA":"upright rectangle" 
    ,"PercB":"mid circle" 
    ,"PercC":"triangle"
    ,"SpecialFx":"square" 
    ,"SpecialFx2":"triangle", 
    "default instrument": "rectangle"}


def fetch_ideal_shape(note_number):
    shape = find_instrument_shape(note_number)
    return instrument_to_shape.get(shape)



############################

def create_rectangle(x,y,height,width,colour):
    return plt.Rectangle((x,y),width,height,linewidth = 1, edgecolor = colour,facecolor = colour) # can rotate 

def create_rectangle_upright(x,y,height,width,colour):
    return plt.Rectangle((x,y),width,height,linewidth = 1, edgecolor = colour,facecolor = colour) # can rotate 


def create_triangle(x,y,height,width,colour):
    points_a = [x,y]
    points_b = [x + (width/2), y + height]
    points_c = [x + width, y]
    points = [points_a,points_b,points_c]
    return plt.Polygon(points,color = colour) # can't rotate 

def create_circle(x,y,height,width,colour):
    radius = width/2 
    return plt.Circle((x,y),radius,edgecolor = colour,facecolor = colour)

def create_ellipse(x,y,height,width,colour):
    return patches.Ellipse((x,y),width,height, color = colour) # can rotate 

def create_square(x,y,height,width,colour):
    return plt.Rectangle((x,y),width,height,linewidth = 1, edgecolor = colour,facecolor = colour) # can rotate 

def create_circle_not_bass(x,y,height,width,colour):
    radius = width/4 
    return plt.Circle((x,y),radius,edgecolor = colour,facecolor = colour)

#################################


instrument_shape_mapping = {"circle":create_circle,
    "ellipse":create_ellipse,
    "upright rectangle":create_rectangle_upright
    ,"mid circle":create_circle_not_bass
    ,"square":create_square
    ,"triangle":create_triangle 
    ,"rectangle": create_rectangle}


def draw_shape(x,y,height,width,colour,shape): 
    return instrument_shape_mapping[shape](x,y,height,width,colour)

##########################################################################
    """ALL ANIMATION FUNCTIONS GO HERE """


def bounce(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']: #intialize all important values
        kwargs['object'].distance = (kwargs['intensity']/127) * (kwargs['height'] * 0.75 )  #how much the note goes high is dependent on the notes velocity -- 127 === max velocity that will lead the note towards a height of note_height * 0.75 
        kwargs['object'].time = kwargs['note_duration'] #time spent going up 
        kwargs['object'].upward_acceleration = (2 * kwargs['object'].distance)/(kwargs['object'].time ** 2) 
        kwargs['object'].velocity = kwargs['object'].upward_acceleration
        kwargs['object'].downward_velocity = (kwargs['object'].distance * -1)/kwargs['object'].time 
        kwargs['object'].y += kwargs['object'].velocity

    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < (kwargs['starting_frame'] + (kwargs['note_duration'])):
        kwargs['object'].velocity += kwargs['object'].upward_acceleration
        kwargs['object'].y += kwargs['object'].velocity

    elif kwargs['current_frame'] >= kwargs['starting_frame'] + kwargs['note_duration'] and kwargs['current_frame'] < kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        kwargs['object'].y += kwargs['object'].downward_velocity 

def change_colour(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        kwargs['object'].colour = kwargs['object'].colour_off 
        return 
    else:
        kwargs['object'].colour = kwargs['object'].colour_on 


def expand(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']: #intialize all important values
        kwargs['object'].expansion_rate = (kwargs['intensity']/127) * 2 #describes the expansion rate - i.e, the rate at which the radius or block will grow in size 
        kwargs['object'].width += kwargs['object'].expansion_rate

    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < (kwargs['starting_frame'] + (kwargs['note_duration'])):
        kwargs['object'].width += kwargs['object'].expansion_rate

    elif kwargs['current_frame'] >= kwargs['starting_frame'] + kwargs['note_duration'] and kwargs['current_frame'] < kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        kwargs['object'].width -= kwargs['object'].expansion_rate


def shake(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 4):
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']:
        kwargs['object'].cycles = round((kwargs['intensity']/127) * 4)
        kwargs['object'].single_cycle = round(((kwargs['note_duration'] * 4)/kwargs['object'].cycles))
        kwargs['object'].onset_list = []
        kwargs['object'].final_onset_duration = (kwargs['note_duration'] * 4) - (kwargs['object'].single_cycle * (kwargs['object'].cycles - 1))
        for i in range(kwargs['object'].cycles):
            if i == 0:
                kwargs['object'].onset_list.append(kwargs['starting_frame'])
            else:
                kwargs['object'].onset_list.append(kwargs['starting_frame'] + (kwargs['object'].single_cycle * i))
        kwargs['object'].max_rotation = (kwargs['intensity']/127) * 60 
        kwargs['object'].current_index = 0
        kwargs['object'].current_rotation = (1/(kwargs['object'].current_index + 1)) * kwargs['object'].max_rotation #reduce angle of rotation with each repetition to show loss of energy 
        kwargs['object'].rate_of_rot = kwargs['object'].current_rotation/round((kwargs['object'].single_cycle/2)) #divide each cycle into two parts 
        kwargs['object'].angle += kwargs['object'].rate_of_rot
    
    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < kwargs['starting_frame'] + (kwargs['note_duration'] * 4):
        if kwargs['object'].current_index != len(kwargs['object'].onset_list) -1:
            if kwargs['current_frame'] < kwargs['object'].onset_list[kwargs['object'].current_index + 1]:
                time_clockwise = kwargs['object'].onset_list[kwargs['object'].current_index] + round((kwargs['object'].single_cycle)/2)
                if kwargs['current_frame'] < time_clockwise: 
                    kwargs['object'].angle += kwargs['object'].rate_of_rot 
                else:
                    time_anticlockwise = (kwargs['object'].onset_list[kwargs['object'].current_index] + kwargs['object'].single_cycle) - time_clockwise
                    kwargs['object'].rate_of_rot = kwargs['object'].current_rotation/time_anticlockwise
                    kwargs['object'].angle -= kwargs['object'].rate_of_rot 
            else:
                kwargs['object'].current_index += 1 
                kwargs['object'].current_rotation = (1/(kwargs['object'].current_index + 1)) * kwargs['object'].max_rotation
                kwargs['object'].rate_of_rot = kwargs['object'].current_rotation/round((kwargs['object'].single_cycle)/2)
                kwargs['object'].angle += kwargs['object'].rate_of_rot
        else:
            time_clockwise = kwargs['object'].onset_list[-1] + round((kwargs['object'].final_onset_duration)/2)
            kwargs['object'].current_rotation = (1/(kwargs['object'].current_index + 1)) * kwargs['object'].max_rotation
            kwargs['object'].rate_of_rot = kwargs['object'].current_rotation/round((kwargs['object'].final_onset_duration)/2)
            if kwargs['current_frame'] < time_clockwise: 
                kwargs['object'].angle += kwargs['object'].rate_of_rot 
            else:
                time_anticlockwise = (kwargs['object'].onset_list[kwargs['object'].current_index] + kwargs['object'].single_cycle) - time_clockwise
                kwargs['object'].rate_of_rot = kwargs['object'].current_rotation/time_anticlockwise
                kwargs['object'].angle -= kwargs['object'].rate_of_rot 


def slide(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']:
        kwargs['object'].xdistance = (kwargs['intensity']/127) * 10
        kwargs['object'].xacceleration = (2 * kwargs['object'].xdistance)/(kwargs['note_duration'] ** 2)
        kwargs['object'].xvelocity_forward = kwargs['object'].xacceleration
        kwargs['object'].xvelocity_behind = kwargs['object'].xacceleration
        kwargs['object'].x += kwargs['object'].xvelocity_forward 

    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < (kwargs['starting_frame'] + (kwargs['note_duration'])):
        kwargs['object'].xvelocity_forward += kwargs['object'].xacceleration
        kwargs['object'].x += kwargs['object'].xvelocity_forward 

    elif kwargs['current_frame'] >= kwargs['starting_frame'] + kwargs['note_duration'] and kwargs['current_frame'] < kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        kwargs['object'].x -= kwargs['object'].xvelocity_behind
        kwargs['object'].xvelocity_behind += kwargs['object'].xacceleration


def roll(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']: #intialize all important values
        kwargs['object'].roll_rate = 360/(kwargs['note_duration'] * 2)
        kwargs['object'].angle += kwargs['object'].roll_rate

    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        kwargs['object'].angle += kwargs['object'].roll_rate

def bounce_and_roll(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']: #intialize all important values
        kwargs['object'].distance = (kwargs['intensity']/127) * (kwargs['height'] * 0.75)  #how much the note goes high is dependent on the notes velocity -- 127 === max velocity that will lead the note towards a height of note_height * 0.75 
        kwargs['object'].time = kwargs['note_duration'] #time spent going up 
        kwargs['object'].upward_acceleration = (2 * kwargs['object'].distance)/(kwargs['object'].time ** 2) 
        kwargs['object'].velocity = kwargs['object'].upward_acceleration
        kwargs['object'].downward_velocity = (kwargs['object'].distance * -1)/kwargs['object'].time 
        kwargs['object'].y += kwargs['object'].velocity
        kwargs['object'].roll_rate = 360/(kwargs['note_duration'] * 2)
        kwargs['object'].angle += kwargs['object'].roll_rate

    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < (kwargs['starting_frame'] + (kwargs['note_duration'])):
        kwargs['object'].velocity += kwargs['object'].upward_acceleration
        kwargs['object'].y += kwargs['object'].velocity
        kwargs['object'].angle += kwargs['object'].roll_rate

    elif kwargs['current_frame'] >= kwargs['starting_frame'] + kwargs['note_duration'] and kwargs['current_frame'] < kwargs['starting_frame'] + (kwargs['note_duration'] * 2):
        kwargs['object'].y += kwargs['object'].downward_velocity 
        kwargs['object'].angle += kwargs['object'].roll_rate


def flight(**kwargs):
    if kwargs['current_frame'] < kwargs['starting_frame'] or kwargs['current_frame'] > kwargs['object'].landing_values[0]:
        return 

    elif kwargs['current_frame'] == kwargs['starting_frame']:
        kwargs['object'].xdistance = (kwargs['object'].landing_values[1] + (kwargs['object'].landing_values[3]/2)) - kwargs['object'].x 
        max_ver_dis = (kwargs['intensity']/127) * ((kwargs['screen_height'] - kwargs['object'].height) - kwargs['object'].y) #maximum vertical distance based on velocity 
        max_ver_pos = kwargs['object'].y + max_ver_dis #the y point of the vertex 
        kwargs['object'].time = kwargs['object'].landing_values[0] - kwargs['current_frame']
        if max_ver_pos > (kwargs['object'].landing_values[2] + kwargs['object'].landing_values[4]): #if max position is greater than paired objects y position 
            kwargs['object'].parabola = True 
            kwargs['object'].vertex = (kwargs['object'].xdistance/2, max_ver_pos)
            kwargs['object'].a = (kwargs['object'].y - kwargs['object'].vertex[1])/((kwargs['object'].vertex[0] - kwargs['object'].x)**2)
            kwargs['object'].time_a = round(kwargs['object'].time * 0.6)
            kwargs['object'].time_b =  kwargs['object'].time -  kwargs['object'].time_a 
            kwargs['object'].xspeed = (kwargs['object'].vertex[0] - kwargs['object'].x)/kwargs['object'].time_a 
            kwargs['object'].acceleration = (kwargs['object'].xdistance - (2 * (kwargs['object'].xspeed * kwargs['object'].time_b)))/(kwargs['object'].time_b **2)
            
            kwargs['object'].x += kwargs['object'].xspeed 
            kwargs['object'].y = (kwargs['object'].a * ((kwargs['object'].x - kwargs['object'].vertex[0])**2)) + kwargs['object'].vertex[1]

        else:
            kwargs['object'].parabola = False 
            kwargs['object'].xspeed = kwargs['object'].xdistance/kwargs['object'].time 
            kwargs['object'].gradient = (kwargs['object'].landing_values[2] - kwargs['object'].y)/(kwargs['object'].landing_values[1] - kwargs['object'].x)
            kwargs['object'].b = kwargs['object'].y - (kwargs['object'].gradient * kwargs['object'].x)
            kwargs['object'].x += kwargs['object'].xspeed 
            kwargs['object'].y = (kwargs['object'].gradient * kwargs['object'].x) + kwargs['object'].b 

    elif kwargs['current_frame'] > kwargs['starting_frame'] and kwargs['current_frame'] < kwargs['object'].landing_values[0]:
        if kwargs['object'].parabola == True:
            if kwargs['current_frame'] < (kwargs['starting_frame'] + kwargs['object'].time_a):
                kwargs['object'].x += kwargs['object'].xspeed 
                kwargs['object'].y = (kwargs['object'].a * ((kwargs['object'].x - kwargs['object'].vertex[0])**2)) + kwargs['object'].vertex[1]
            else:
                kwargs['object'].xspeed += kwargs['object'].acceleration 
                kwargs['object'].x += kwargs['object'].xspeed 
                kwargs['object'].y = (kwargs['object'].a * ((kwargs['object'].x - kwargs['object'].vertex[0])**2)) + kwargs['object'].vertex[1]
        else:
            kwargs['object'].x += kwargs['object'].xspeed 
            kwargs['object'].y = (kwargs['object'].gradient * kwargs['object'].x) + kwargs['object'].b 
                


animation_map = {"slide":slide, "bounce":bounce,"roll":roll,"jump and roll":bounce_and_roll,"shake":shake,"expand":expand,"flight":flight} 

def animate_entity(frame,starting_frame,note_duration, height,obj,intensity,screen_height,randomselection = False):
    if randomselection == False:
        an_nam = obj.animation_name
    else:
        an_nam = "flight"
    return animation_map[an_nam](current_frame = frame,starting_frame = starting_frame, note_duration = note_duration,height = height, object = obj, intensity = intensity, screen_height = screen_height)


    
        

    






    







    

    






    
    



    
        





    

    





















