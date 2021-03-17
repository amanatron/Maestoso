'''BASIC THEME - ALSO KNOWN AS CLASSIC THEME'''
import os, sys 
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) #import modules from parent folder 
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from utility import frame_rate_note, frames_to_second
from tracklist_functions import create_timecode_hash, find_pitch_range 

matplotlib.use('TkAgg')

class BasicTheme:
    def __init__(self,tracklist):
        self.category = 'POLYPHONIC'
        self.display_name = 'Classic'
        self.tracklist = tracklist

        self.grid_on = ['Grid','CHECKBOX',True]
        self.background_colour = ['Background Colour','COLORBOX','blue']
        self.grid_colour = ['Grid Color','COLORBOX',"white"]
        self.grid_width = ['Grid Width','ENTRY',0.2,(0,10),"int"] # Entry widgets take 4 arguments...[3][0] describes the starting limit of the entry..(if none, use '') at 3[1] max lmit entry...if type == str, only define max limit in [3],[4] describes the type.. if it's an int, the limit is defined by max number or tuple describing the range and if its a str, the max range is defined by character limit.
        self.camera_speed = ["Camera Speed","ENTRY",2,(1,10),"int"]
        self.view_size = ['Measures','ENTRY',30,(1,30),"int"]
        self.note_opacity = ["Note Opacity","CHECKBOX",True]
        self.meter_grid = ["Grid Meter Display","CHECKBOX",True]
        self.customizable_elements = [self.grid_on,self.background_colour,self.grid_colour,self.grid_width,self.camera_speed,self.view_size,self.note_opacity,self.meter_grid] # always use the following attribute name and type 
        self.theme_description = ["The classic piano roll styled theme inspired by the works of Stephen Malinowski. As they say: when in doubt, go with the classics - and there's nothing more classic than a piano roll theme.","Created by Aman Trivedi as part of the Maestoso Project."]

    def ANIMATE(self,upd_project_tracklist,upd_PPQN,upd_fps,upd_output_dir,upd_preview,upd_preview_time):
        tracklist = self.tracklist
        project_tracklist = upd_project_tracklist

     
        pitch_range = find_pitch_range(project_tracklist)

        
        PPQN = upd_PPQN
        polyphonic_list = create_timecode_hash(project_tracklist)
        fps = upd_fps
        output_dir = upd_output_dir
        preview = upd_preview
        preview_time = upd_preview_time

        grid_on = self.grid_on[2]
        background_colour = self.background_colour[2]
        grid_colour = self.grid_colour[2]
        grid_width = self.grid_width[2]
        camera_speed = float(self.camera_speed[2])
        view_size = float(self.view_size[2])
        note_opacity = self.note_opacity[2]
        grid_meter = self.meter_grid[2]


        ''' CONSTRUCTING POLYPHONIC ANIMATION ''' 
        aspect_ratio = (16,9) 
        dpi = 120

        def adjust_dimensions(pitch_range):
            """[ADJUSTS THE DIMENSIONS OF ALL FRAMES IN THE POLYPHONIC ANIMATION]

            Args:
                pitch_range ([list]): [function within init_project.py]

            Returns:
                [tuple]: [width and height]
            """
            height = (chosen_note_height * len(pitch_range)) + margin + int(margin/2)
            width = round((height * aspect_ratio[0])/aspect_ratio[1])
            return (width,height)
        
        margin = 200 # space left 100 above and 100 below aesthetic purposes
        chosen_note_height = 50 #height of every note
        width = adjust_dimensions(pitch_range)[0] 
        height = adjust_dimensions(pitch_range)[1]
        measures = view_size # The number of measures to be displayed at any time in one camera frame
        base_pulse_size = width/(tracklist.ts_changes[0].numerator * measures) #pulse size 
        base_note_size = (tracklist.ts_changes[0].denominator/4) * base_pulse_size #quarter note size 
       
        def box_length(note):
            """[OBTAIN THE LENGTH OF BLOCKS BASED ON NOTE DURATION]

            Args:
                note ([Note class]): [initialized in init_tracklist.py]

            Returns:
                [float]: [length of the block]
            """
            nx = ((4/tracklist.ts_changes[0].denominator)/note.note_length) # calculates note ratio against quarter note length -- quarter = 1 (PPQN/PPQN)
            box_length = width / (nx * (tracklist.ts_changes[0].numerator * measures))
            return box_length

        def box_location_x(note):
            """[LOCATION OF THE BLOCK ALONG THE X-AXIS IN ACCORDANCE WITH THE NOTE ONSET ]

            Args:
                note ([Note class]): [initialized in init_tracklist.py]

            Returns:
                [float]: [location along the x-axis]
            """
            if note.start_ticks == 0:
                x_pos = 0 + width/2 
                return x_pos # if note onset is 0 ticks 
            else:
                distance_length = note.start_ticks/PPQN #The total distance that occurs before the note 
                nx = (4/tracklist.ts_changes[0].denominator)/distance_length
                x_pos = (width / (nx * (tracklist.ts_changes[0].numerator * measures))) + width/2 
                return x_pos

        def box_location_y(note):
            """[LOCATION OF THE BLOCK ALONG THE Y-AXIS IN ACCORDANCE WITH PITCH RANGE]

            Args:
                note ([Note class]): [initialized in init_tracklist.py]

            Returns:
                [float]: [location along the y-axis]
            """
            max_position = height - (margin/2) # location of highest note in pitchrange will always be at margin/2
            max_note = max(pitch_range)
            difference = max_note - note.pitch # find difference current note value and max note value to obtain it's position in acccordance to margin/2 
            location = max_position - (difference * chosen_note_height)
            return location 

        def pix_to_inch(size): #function to convert pixels to inch 
            one_pix = 1/dpi  
            return one_pix * size 

        class GraphAnimation: #initialize graph 
            def __init__(self):
                plt.ioff()
                self.fig, self.ax = plt.subplots(figsize=(pix_to_inch(1280),pix_to_inch(720)),dpi=dpi)
                plt.xlim([0,width])
                plt.ylim([0,height])
                if grid_on == True:
                    if grid_meter == True:
                        grd_space = plticker.MultipleLocator(base = base_pulse_size)
                        self.ax.yaxis.set_major_locator(grd_space)
                        self.ax.xaxis.set_major_locator(grd_space)
                    plt.grid(which = 'major', color = grid_colour,linewidth = grid_width)
                    self.ax.spines['right'].set_visible(False)
                    self.ax.spines['left'].set_visible(False)
                    self.ax.spines['top'].set_visible(False)
                    self.ax.spines['bottom'].set_visible(False)
                else:
                    plt.grid(False)
                    self.ax.axis('off')
                self.ax.set_xticklabels([])
                self.ax.set_yticklabels([])
                self.fig.patch.set_facecolor(background_colour)
                self.ax.patch.set_facecolor(background_colour)


            def clear_patches(self):
                self.ax.patches = []

                
        class Camera: 
            def __init__(self):
                self.quarter_length = base_note_size
                self.tempo_changes = self.construct_tempo_map()
                self.current_tempo = self.tempo_changes.get(0.0)
                self.camera_movement = self.calculate_camera_movement(0.0)

            def construct_tempo_map(self):
                tempo_changes = {}
                for i in range(len(tracklist.tempo_changes[0])):
                    tempo_changes.update({frame_rate_note(tracklist.tempo_changes[0][i],fps):tracklist.tempo_changes[1][i]})
                return tempo_changes


            def calculate_camera_movement(self,frame_number):
                try:
                    self.current_tempo = self.tempo_changes.get(frame_number)
                    nqps = self.current_tempo/60 
                    self.camera_movement = (self.quarter_length * nqps)/fps 
                    return self.camera_movement
                except:
                    return self.camera_movement



        class Block:
            def __init__(self,note):
                self.note = note
                self.height = chosen_note_height
                self.width = box_length(self.note)
                self.x = box_location_x(self.note)
                self.y = box_location_y(self.note)
                self.colour = self.note.colour 
                self.duration = self.note.return_duration()
                self.start_time = self.note.start_time
                self.endtime = self.note.end_time
                self.ON = True 
                if note_opacity == True:
                    self.set_alpha()
                

            def block_draw(self):
                return plt.Rectangle((self.x,self.y),self.width,self.height,linewidth = 1, edgecolor = self.colour,facecolor = self.colour)

            def set_alpha(self):
                if len(self.colour) == 7:
                    alpha_value = '80'
                    self.colour = self.colour + alpha_value


        def create_plot(lst):
            for i in lst:
                plt.gca().add_patch(i.block_draw())

        def destroy_block(lst):
            for i in lst:
                if i.width + i.x < 0:
                    lst.remove(i)

        def move_camera(lst,camera):
            for i in lst:
                i.x -= (camera * camera_speed)


        class BasicThemeAnimation:
            def __init__(self,output_dir):
                self.time_elapsed = 0
                self.image_number = 0
                self.temp_list = []
                self.output_dir = output_dir
                self.preview_time = preview_time
                self.camera = Camera()


            def create_frames(self,k):
                create_plot(self.temp_list)
                plt.savefig(f'{self.output_dir}/frame_{self.image_number}.png')
                self.image_number += 1
                camera_movement = self.camera.calculate_camera_movement(self.image_number)
                move_camera(self.temp_list,camera_movement)

            def detect_note_off(self,frame,k):
                    for i in self.temp_list:
                            if i.start_time < k + frames_to_second(frame,fps) and i.endtime >= k + frames_to_second(frame,fps):
                                i.set_alpha()

            def animate_theme(self):
                graph = GraphAnimation()
                keys = list(polyphonic_list)
                for k, v in polyphonic_list.items():
                    difference = k - self.time_elapsed
                    self.time_elapsed = k
                    if difference == 0:
                        for i in v:
                            self.temp_list.append(Block(i))
                        self.create_frames(k)
                        graph.clear_patches()
                    else:
                        frame = 0
                        current_onset = k
                        previous_onset = (k - difference)
                        while frame < frame_rate_note(current_onset,fps) - frame_rate_note(previous_onset,fps):
                            self.create_frames(k)
                            frame += 1
                            graph.clear_patches()
                            destroy_block(self.temp_list)
                        for i in v:
                            self.temp_list.append(Block(i))
                        
                        if k == keys[-1]:
                            frame = 0
                            while frame < frame_rate_note(5,fps):
                                self.create_frames(k)
                                frame += 1
                                graph.clear_patches()
                                destroy_block(self.temp_list)

                            self.time_elapsed += 5


                    if preview == True and self.time_elapsed > preview_time:
                        return 
    
        theme = BasicThemeAnimation(output_dir)
        theme.animate_theme()


                    
            

             

    




    
