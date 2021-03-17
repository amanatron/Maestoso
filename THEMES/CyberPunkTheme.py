import os, sys 
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) #import modules from parent folder 
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import mplcyberpunk 
from utility import frame_rate_note, frames_to_second
from tracklist_functions import find_pitch_range, create_timecode_hash
import matplotlib

matplotlib.use("TkAgg")

class CyberPunkTheme:
    def __init__(self,tracklist):
        self.category = 'POLYPHONIC'
        self.display_name = 'CyberPunk'
        self.tracklist = tracklist
        self.grid_on = ['Grid','CHECKBOX',True]
        self.grid_width = ['Grid Width','ENTRY',0.2,(0,10),"int"]
        self.background_colour = ['Background Colour','COLORBOX','blue']
        self.underglow_effect = ['Underglow Effect','CHECKBOX',True]
        self.neon_effect = ['Neon Effect','CHECKBOX',True]
        self.grid_colour = ['Grid Colour','COLORBOX','blue']
        self.camera_speed = ['Camera Speed','ENTRY',1,(1,10),"int"]
        self.view_size = ['Measures','ENTRY',4,(1,50),"int"]
        self.meter_grid = ["Grid Meter Display","CHECKBOX",True]

        self.customizable_elements = [self.grid_on,self.background_colour,self.underglow_effect,self.neon_effect,self.grid_colour,self.camera_speed,self.view_size,self.grid_width,self.meter_grid]
        self.theme_description = ['The most lit theme in the software - literally. This cyberpunk styled theme features a host of styling options including but not limited to neon like glows and underglows. This theme is an answer to the question: "what if cartesian geometry was a night club"?','Created by Aman Trivedi as part of the Maestoso Project.']

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
        underglow_effect = self.underglow_effect[2]
        neon_effect = self.neon_effect[2]
        grid_colour = self.grid_colour[2]
        camera_speed = float(self.camera_speed[2])
        view_size = float(self.view_size[2])
        grid_width = float(self.grid_width[2])
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


        measures = view_size # The number of measures to be displayed at any time in one camera frame
        chosen_note_height = 50 #height of every note 
        margin = 200 # space left 100 above and 100 below aesthetic purposes
        width = adjust_dimensions(pitch_range)[0] 
        height = adjust_dimensions(pitch_range)[1]

        base_pulse_size = width/(tracklist.ts_changes[0].numerator * measures) #pulse size 
        base_note_size = (tracklist.ts_changes[0].denominator/4) * base_pulse_size #quarter note size 

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

        def pix_to_inch(size):
            one_pix = 1/dpi 
            return one_pix * size 

        class GraphAnimation:
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

            def clear_plot(self):
                plt.cla()
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
                elif grid_on == False:
                    plt.grid(False)
                    self.ax.axis('off')
                self.ax.set_xticklabels([])
                self.ax.set_yticklabels([])
                self.fig.patch.set_facecolor(background_colour)
                self.ax.patch.set_facecolor(background_colour)


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

        def destroy_block(lst):
            for i in lst:
                if i.x < 0:
                    lst.remove(i)

        def move_camera(lst,camera):
            for i in lst:
                for j in range(len(i.x)):
                    i.x[j] = i.x[j] - (camera * camera_speed)

        def delete_items(lst):
            for i in lst:
                for j in i.x:
                    if j < 0:
                        i.y.remove(i.y[i.x.index(j)])
                        i.x.remove(j)
                    elif j > 0:
                        break 


        class LineGraph:
            def __init__(self,k,colour):
                self.specialcode = k
                self.x = []
                self.y = []
                self.colour = colour


        def create_plot(lst):
            for i in lst:
                plt.plot(i.x,i.y, color = i.colour, marker = 'o')

            
            if neon_effect == True:
                mplcyberpunk.make_lines_glow()
            if underglow_effect == True:
                mplcyberpunk.add_underglow()

        class CyberPunkThemeAnimation:
            def __init__(self,output_dir):
                self.time_elapsed = 0
                self.image_number = 0
                self.temp_list = []
                self.camera = Camera()
                self.output_dir = output_dir
                self.initialize_templist()


            def initialize_templist(self):
                for i in project_tracklist:
                    self.temp_list.append(LineGraph(i.specialcode,i.colour))

            def create_frames(self,k):
                create_plot(self.temp_list)
                plt.savefig(f'{self.output_dir}/frame_{self.image_number}.png')
                self.image_number += 1
                camera_movement = self.camera.calculate_camera_movement(self.image_number)
                move_camera(self.temp_list,camera_movement)


            def add_elements_to_temp(self,v):
                for i in v:
                    for j in self.temp_list:
                        if i.specialcode == j.specialcode:
                            j.x.append(box_location_x(i))
                            j.y.append(box_location_y(i))


            def animate_theme(self):
                graph = GraphAnimation()
                plt.ioff()
                keys = list(polyphonic_list)
                for k, v in polyphonic_list.items():
                    difference = k - self.time_elapsed
                    self.time_elapsed = k
                    if difference == 0:
                        self.add_elements_to_temp(v)
                        self.create_frames(k)
                        graph.clear_plot()
                    else:
                        frame = 0
                        current_onset = k 
                        previous_onset = k - difference 
                        while frame < frame_rate_note(current_onset,fps) - frame_rate_note(previous_onset,fps):
                            self.create_frames(k)
                            frame += 1
                            graph.clear_plot()
                        self.add_elements_to_temp(v)
                        delete_items(self.temp_list)

                        if k == keys[-1]: # if last note of the sequence 
                            frame = 0
                            while frame < frame_rate_note(5,fps):
                                self.create_frames(k)
                                frame += 1
                                graph.clear_plot()
                            self.time_elapsed += 5



                    if preview == True and self.time_elapsed > 45:
                        return 
    
        theme = CyberPunkThemeAnimation(output_dir)
        theme.animate_theme()