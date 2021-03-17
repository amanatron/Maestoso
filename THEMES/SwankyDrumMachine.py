import os, sys 
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) #import modules from parent folder 

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
from utility import frame_rate_note, pick_random_colour
from tracklist_functions import create_drum_hash, find_all_drums
from theme_extras import SwankyDrumMachine_Functions as SDF
from pretty_midi import drum_name_to_note_number, note_number_to_drum_name
from math import pi 
import random 


class SwankyDrumMachine:
    def __init__(self,tracklist):
        self.category = 'RHYTHM'
        self.display_name = 'Swanky Machine'
        self.tracklist = tracklist 

        self.grid_on = ['Grid','CHECKBOX',True]
        self.background_colour = ['Background Colour','COLORBOX','blue']
        self.grid_colour = ['Grid Color','COLORBOX',"white"]
        self.grid_width = ['Grid Width','ENTRY',0.2,(0,10),"int"] # Entry widgets take 4 arguments...[3][0] describes the starting limit of the entry..(if none, use '') at 3[1] max lmit entry...if type == str, only define max limit in [3],[4] describes the type.. if it's an int, the limit is defined by max number or tuple describing the range and if its a str, the max range is defined by character limit.
        self.camera_speed = ["Camera Speed","ENTRY",1,(1,10),"int"]
        self.view_size = ['Measures','ENTRY',2,(1,30),"int"]
        self.meter_grid = ["Grid Meter Display","CHECKBOX",True]
        self.random_flight = ["Random Flight","CHECKBOX",True]
        self.random_flight_chances = ["Chance of Flight","ENTRY",2,(1,5),"int" ]

        self.customizable_elements = [self.grid_on,self.background_colour,self.grid_colour,self.grid_width,self.camera_speed,self.view_size,self.meter_grid,self.random_flight,self.random_flight_chances] # always use the following attribute name and type
        count = 1
        for i in find_all_drums(self.tracklist.track_list, name = False):
            midi_number = i 
            try:
                midi_name = note_number_to_drum_name(midi_number)
            except:
                midi_name = f'Drum {count}'
                count += 1
            self.customizable_elements.append([f"{midi_name}","COLORBOX",f"{pick_random_colour()}","colour"])
            self.customizable_elements.append([f"{midi_name} Animation","DROPDOWN",SDF.fetch_ideal_animation(midi_number),["bounce","slide","shake","roll","jump and roll","expand","random"],"animation"])
            self.customizable_elements.append([f"{midi_name} Shape","DROPDOWN",SDF.fetch_ideal_shape(midi_number),["square","triangle","circle","mid circle","upright rectangle","ellipse","rectangle","random"],"shape"])

        self.theme_description = ["The classic piano roll styled theme inspired by the works of Stephen Malinowski. As they say: when in doubt, go with the classics - and there's nothing more classic than a piano roll theme.","Created by Aman Trivedi as part of the Maestoso Project."]


    def ANIMATE(self,upd_project_tracklist,upd_PPQN,upd_fps,upd_output_dir,upd_preview,upd_preview_time):
        tracklist = self.tracklist
        project_tracklist = upd_project_tracklist
        PPQN = upd_PPQN
        fps = upd_fps
        output_dir = upd_output_dir
        preview = upd_preview
        preview_time = upd_preview_time
        dpi = 120 
        aspect_ratio = (16,9)
        rhythm_tracklist = create_drum_hash(project_tracklist) 
        name_list = find_all_drums(project_tracklist,name=False)

        grid_on = self.grid_on[2]
        background_colour = self.background_colour[2]
        grid_colour = self.grid_colour[2]
        grid_width = self.grid_width[2]
        camera_speed = float(self.camera_speed[2])
        view_size = float(self.view_size[2])
        grid_meter = self.meter_grid[2]
        random_flight = self.random_flight[2]
        random_flight_chances = self.random_flight_chances[2]

        measures = view_size

        # if len(tracklist.ts_changes) > 1:
        #     return 
        
        item_map = {}
        for i in self.customizable_elements:
            try:
                if i[3] == "colour":
                    item_map.update({i[0]:[i[2]]})
            except:
                continue 

        for i in self.customizable_elements:
            try:
                if i[4] == "animation":
                    upd_name = i[0].replace(' Animation','')
                    item_map[upd_name].append(i[2])
                elif i[4] == 'shape':
                    upd_name = i[0].replace(' Shape','')
                    item_map[upd_name].append(i[2])
            except:
                continue 
    
        chosen_note_height = 60
        margin = 200

        def adjust_dimensions(pitch_range):
            height = (chosen_note_height * len(pitch_range)) + margin + int(margin/2)
            width = round((height * aspect_ratio[0])/aspect_ratio[1])
            return (width,height)

        width = adjust_dimensions(name_list)[0]
        height = adjust_dimensions(name_list)[1]
        base_pulse_size = width/(tracklist.ts_changes[0].numerator * measures) #pulse size 
        base_note_size = (tracklist.ts_changes[0].denominator/4) * base_pulse_size #quarter note size 

        def box_length(note):
            nx = ((4/tracklist.ts_changes[0].denominator)/note.note_length) # calculates note ratio against quarter note length -- quarter = 1 (PPQN/PPQN)
            box_length = width / (nx * (tracklist.ts_changes[0].numerator * measures))
            return box_length

        def box_location_x(note):
            if note.start_ticks == 0:
                x_pos = width/2
                return x_pos # if note onset is 0 ticks 
            else:
                distance_length = note.start_ticks/PPQN #The total distance that occurs before the note 
                nx = (4/tracklist.ts_changes[0].denominator)/distance_length
                x_pos = (width / (nx * (tracklist.ts_changes[0].numerator * measures))) + width/2 
                return x_pos

        def create_ypos_hierarchy():
            returning_dict = {} #a dictionary containing hierarchal seperation 
            temp_lst = find_all_drums(project_tracklist,name= False) 
            counter = len(temp_lst)
            while counter >= 1:
                max_note = max(temp_lst)
                returning_dict.update({max_note:counter})
                max_index = temp_lst.index(max_note)
                temp_lst.remove(temp_lst[max_index])
                counter -= 1
            return returning_dict

        returning_dict = create_ypos_hierarchy()

        def box_location_y(note):
            max_position = height - (margin/2)
            max_note = max(name_list)
            max_pos = len(name_list)
            difference = max_pos - returning_dict.get(note)
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

        class NoteBlock:
            def __init__(self,note):
                self.note = note
                self.width = box_length(self.note)
                self.x = box_location_x(self.note)
                self.y = box_location_y(self.note.pitch)
                self.instrument_name = note_number_to_drum_name(self.note.pitch)
                self.colour = item_map.get(self.instrument_name)[0]
                self.category = SDF.find_instrument_shape(self.note.pitch)
                self.height = SDF.return_entity_height(self.width,self.category,chosen_note_height)
                self.starting_frame = frame_rate_note(self.note.start_time,fps)
                self.note_duration = frame_rate_note(self.note.return_duration(),fps) * 2
                if self.note_duration == 0:
                    self.note_duration = fps 
                self.intensity = self.note.velocity 
                self.colour_on = self.colour 
                self.colour_off = self.colour + '80'
                self.randomselection = False 
        
                if item_map.get(self.instrument_name)[1] == "random":
                    self.animation_name = SDF.fetch_ideal_animation(self.note.pitch)
                else:
                    self.animation_name = item_map.get(self.instrument_name)[1]

                if item_map.get(self.instrument_name)[2] == "random":
                    self.shape = SDF.fetch_ideal_shape(self.note.pitch)
                else:
                    self.shape = item_map.get(self.instrument_name)[2]

                if self.shape == "ellipse":
                    self.angle = 180 
                else:
                    self.angle = 0

            def draw_shape(self,frame):
                entity = SDF.draw_shape(self.x,self.y,self.height,self.width,self.colour,self.shape)
                if self.animation_name == "shake" or self.animation_name == "roll" or self.animation_name == "jump and roll" and frame > self.starting_frame and self.randomselection == False:
                    angle_rad = self.angle * (pi/180)
                    x_center = self.x + (self.width/2)
                    y_center = self.y + (self.height/2)
                    transform = matplotlib.transforms.Affine2D().rotate_around(x_center,y_center,angle_rad)
                    entity.set_transform(transform)
                plt.gca().add_patch(entity)

            def animate_object(self,frame):
                if self.randomselection == True:
                    SDF.animate_entity(frame,self.starting_frame,self.note_duration,self.height,self,
                    self.intensity,height,randomselection = True)
                else:
                    SDF.animate_entity(frame,self.starting_frame,self.note_duration,self.height,self,
                    self.intensity,height,randomselection = False)
                SDF.change_colour(object = self,current_frame = frame, starting_frame = self.starting_frame, note_duration = self.note_duration)


            def select_a_random_note(self,onsets,fps):
                keys = list(onsets.keys())
                if keys[-1] == self.note.start_time:
                    self.randomselection = False 
                    return 
                current_index = keys.index(self.note.start_time)
                try:
                    selection = keys[current_index + 1:current_index + 10]
                    ideal_indexes = []
                    for i in selection:
                        if frame_rate_note(i,fps) - self.starting_frame >= frame_rate_note(1,fps):
                            temp_list = onsets.get(i)
                            if box_location_x(temp_list[0]) - self.x <= (width/(measures * 2)):
                                ideal_indexes.append(selection.index(i))
                    if len(ideal_indexes) == 0:
                        self.randomselection = False 
                        return
                    else:
                        lucky_val = random.randint(0,10)
                        if lucky_val < (random_flight_chances/10):
                            selected_index = random.choice(ideal_indexes)
                            selected_onset = selection[selected_index]
                            values_in_selection = onsets.get(selected_onset)
                            selected_note = random.choice(values_in_selection)
                            self.landing_values = [frame_rate_note(selected_note.start_time,fps), box_location_x(selected_note), box_location_y(selected_note.pitch),box_length(selected_note),SDF.return_entity_height(box_length(selected_note), SDF.find_instrument_shape(selected_note.pitch),chosen_note_height)] #[0] = starting frame, [1] = x loc, [2] = y loc, [3] = length, [4] = height
                            self.randomselection = True 
                        else:
                            self.randomselection = False 
                except:
                    self.randomselection = False 




            
        def animate_animation():
            graph = GraphAnimation()
            camera = Camera()
            block_list = []

            time_keys = list(rhythm_tracklist.keys())

            if preview == True and preview_time < time_keys[-1]:
                end_time = preview_time
            else:
                end_time = time_keys[-1]

            for k, v in rhythm_tracklist.items():
                for i in v:
                    block_list.append(NoteBlock(i))
            
            if random_flight == True:
                for i in block_list:
                    i.select_a_random_note(rhythm_tracklist,fps)

            image_number = 0 

            def create_drawings(camera_movement):
                for i in block_list:
                    i.draw_shape(image_number)
                    i.x -= (camera_movement * camera_speed)
        
            while image_number < frame_rate_note(end_time,fps):
                camera_movement = camera.calculate_camera_movement(image_number)
                create_drawings(camera_movement)
                for i in block_list:
                    i.animate_object(image_number)
                plt.savefig(f'{output_dir}/frame_{image_number}.png')
                graph.clear_patches()
                image_number += 1
                
        animate_animation()
            
