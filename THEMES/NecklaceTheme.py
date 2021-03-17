import matplotlib.pyplot as plt
from utility import frame_rate_note, pick_random_colour
from tracklist_functions import create_drum_hash, find_all_drums
from math import pi, cos, sin
import matplotlib
from pretty_midi import note_number_to_drum_name

matplotlib.use("TkAgg")

class NecklaceTheme:
    def __init__(self,tracklist):
        self.category = 'RHYTHM'
        self.display_name = 'Toussaint'
        self.tracklist = tracklist 
        self.background_color = ["Background Colour","COLORBOX","black"]
        self.bass_effect = ["Bass Effect","DROPDOWN","FUNKY",["OFF","FUNKY","A LITTLE CRAZY!","SUPA-CRAZY!!"]]
        self.beads_color = ["Beads Colour","COLORBOX","#ffffff"]
        self.pulse_sensitivity = ["Accent Sensitivity","DROPDOWN","Moderate",["Off","Moderate","Intense","You must be kidding me!"]]
            
        self.customizable_elements = [self.background_color,self.bass_effect,self.beads_color,self.pulse_sensitivity]

        for i in find_all_drums(tracklist.track_list, name = True):
            self.customizable_elements.append([f"{i}","COLORBOX",f"{pick_random_colour()}","iterated"])

        self.theme_description = ["Inspired by the works of musicologist Godfried Toussaint, this theme offers a cyclic analysis of rhythm sections. The only drawback to using this theme is that it doesn't support changes in time signature.","Created by Aman Trivedi as part of the Maestoso Project."]


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
        height = 720
        width = 1280

        bass_effect_dir = {"FUNKY":0.98,"A LITTLE CRAZY!":0.90,"SUPA-CRAZY!!":0.80,"OFF":False}
        accent_sens_dir = {"Moderate":0.02,"Intense":0.05,"You must be kidding me!":0.08,"OFF":False}

        background_color = self.background_color[2]
        bass_effect = bass_effect_dir.get(self.bass_effect[2])
        beads_color = self.beads_color[2]
        pulse_sensitivity = accent_sens_dir.get(self.pulse_sensitivity[2])
        additional_colours = []

        for i in self.customizable_elements:
            try: 
                if i[3] == "iterated":
                    additional_colours.append((i[0],i[2]))
            except:
                continue

        rhythm_tracklist = create_drum_hash(project_tracklist)
            
        name_list = find_all_drums(project_tracklist,name=False)
        name_list.sort()

        if len(tracklist.ts_changes) == 1:
            pass 
        else:
            messagebox.showerror("Theme Error"," Multiple instances of time signature changes have been found. This theme doesn't support changes in time signature.")
            return 

        numerator = tracklist.ts_changes[0].numerator
        denominator = tracklist.ts_changes[0].denominator
        measure_duration = (4/denominator) * numerator

        pulse_array = [frame_rate_note(i,fps) for i in tracklist.pulse] #all the pulses of the track converted to frames 
        accent_array = [frame_rate_note(i,fps) for i in tracklist.accented_beats]


        def pix_to_inch(size):
            one_pix = 1/dpi 
            return one_pix * size 


        class GraphAnimation:
            def __init__(self):
                plt.ioff()
                self.fig, self.ax = plt.subplots(figsize=(pix_to_inch(1280),pix_to_inch(720)),dpi=dpi)
                plt.xlim([0,width])
                plt.ylim([0,height])
                plt.grid(False)
                self.ax.set_xticklabels([])
                self.ax.set_yticklabels([])
                self.ax.axis('off')
                self.fig.set_facecolor(background_color)
                self.ax.set_facecolor(background_color)

            def clear_patches(self):
                self.ax.patches = []


        class Polygon:
            def __init__(self,radius,colour,pitch):
                self.pitch = pitch 
                self.radius = radius
                self.colour = colour
                self.x = width/2
                self.y = height/2 
                self.inner_radius = self.find_inner_circle()
                self.frame = 0
                self.animating = False 
                self.pulse_size = 0

            def find_inner_circle(self):
                space = self.radius - (self.radius * 0.80)
                inner_radius = self.radius - (space/2) 
                return inner_radius

            def draw_polygon(self):
                circle = plt.Circle((self.x, self.y), self.radius, color=self.colour)
                return circle 


            def animate_polygon(self,image_number):
                if bass_effect == False:
                    return 
                shrink = bass_effect
                expand = 1 - shrink 
                for i in pulse_array:
                    if i == image_number:
                        try: 
                            self.pulse_size = pulse_array[pulse_array.index(i)+1] - i #in fps 
                        except:
                            self.pulse_size = round(fps * 0.6)
                        
                        if pulse_sensitivity != False:
                            for j in accent_array:
                                if j == i:
                                    shrink -= pulse_sensitivity

                        self.frame = i
                        self.animating = True 
                        self.shrink_rate = (self.radius - (self.radius * shrink))/round(self.pulse_size/2)
                        self.expand_rate = (self.radius - (self.radius * shrink))/(self.pulse_size - round(self.pulse_size/2))
                        self.shrink_time = self.frame + round(self.pulse_size/2)
                        self.expand_time = (self.frame + self.pulse_size)
                        break

                if self.animating == True:

                    if self.frame < self.shrink_time:
                        self.radius -= self.shrink_rate
                        self.inner_radius -= self.shrink_rate
                        self.frame += 1

                    elif self.frame >= self.shrink_time and self.frame < self.expand_time:
                        self.radius += self.expand_rate
                        self.inner_radius += self.expand_rate
                        self.frame += 1

                    elif self.frame >= self.frame + self.pulse_size:
                        self.animating = False


        def create_polygon_list():
            current_radius = width/4 
            polygon_list = []
            for i in name_list:
                drum_name = note_number_to_drum_name(i)
                for j in additional_colours:
                    if j[0] == drum_name:
                        inst_colour = j[1]
                polygon_list.append(Polygon(current_radius,inst_colour,i))
                current_radius = current_radius * 0.80
            
            current_radius = current_radius * 0.80
            polygon_list.append(Polygon(current_radius,background_color,'NONE'))

            return polygon_list

        polygon_list = create_polygon_list()

        class Point:
            def __init__(self,polygon_radius,inner_radius,angle,pitch):
                self.pitch = pitch 
                self.polygon_radius = polygon_radius
                self.space = (self.polygon_radius) - (self.polygon_radius * 0.80)
                self.radius = self.space/4
                self.origin = (width/2,height/2)
                self.inner_radius = inner_radius
                self.x = (self.inner_radius * sin(angle)) + self.origin[0]
                self.y = (self.inner_radius * cos(angle)) + self.origin[1]
                self.colour = beads_color
                self.angle = angle 

            def draw_point(self):
                circle = plt.Circle((self.x, self.y), self.radius, color=self.colour)
                return circle 
            
            def change_opacity(self):
                if self.colour == '#ffffff':
                    self.colour += '80'

            def readjust(self):
                self.space = (self.polygon_radius) - (self.polygon_radius * 0.80)
                self.radius = self.space/4
                self.x = (self.inner_radius * sin(self.angle)) + self.origin[0]
                self.y = (self.inner_radius * cos(self.angle)) + self.origin[1]


        def draw_polygons():
                for i in polygon_list:
                    plt.gca().add_patch(i.draw_polygon())

        def display_points(lst):
            for i in lst:
                plt.gca().add_patch(i.draw_point())

        



        def animate():
            graph = GraphAnimation()
            image_number = 0

            time_elapsed = 0 #variable to measure, measure based duration
            time_elapsed_seconds = 0 # variable to measure frame duration
            previous_tick = 0
            keys = list(rhythm_tracklist)
            points = []

            def create_points_list(v,polygon_list,angle): 
                for j in v:
                    for i in polygon_list:
                        if i.pitch == j.pitch:
                            polygon_radius = i.radius 
                            inner_radius = i.inner_radius
                            points.append(Point(polygon_radius,inner_radius,angle,i.pitch))


            def adjust_points_list():
                for i in points:
                    for j in polygon_list:
                        if i.pitch == j.pitch:
                            i.polygon_radius = j.radius
                            i.inner_radius = j.inner_radius
                            i.readjust()

            for k, v in rhythm_tracklist.items():
                time_elapsed += (v[0].start_ticks - previous_tick)/PPQN
                previous_tick = v[0].start_ticks 
                if time_elapsed >= measure_duration: # if cycle is complete 
                    time_elapsed -= measure_duration
                    graph.clear_patches()
                    points.clear()
                    
                angle = ((time_elapsed/measure_duration) * 360) * pi/180 # set value of angle 


                create_points_list(v,polygon_list,angle)


                frame = 0 
                current_frame = frame_rate_note(k,fps)

                if k != keys[-1]:
                    next_frame = frame_rate_note(keys[keys.index(k) + 1],fps)
                elif k == keys[-1]:
                    next_frame = frame_rate_note(5,fps)


                duration = next_frame - current_frame

                
                if k == keys[0] and k!= 0:
                    temp_frame = 0
                    draw_polygons() 
                    while temp_frame < current_frame:
                        plt.savefig(f'{output_dir}/frame_{image_number}.png')
                        image_number += 1
                        temp_frame += 1
                else:
                    draw_polygons()
                    display_points(points)
                    while frame < duration:
                        plt.savefig(f'{output_dir}/frame_{image_number}.png')
                        for i in polygon_list:
                            i.animate_polygon(image_number)
                        graph.clear_patches()
                        draw_polygons()
                        adjust_points_list()
                        display_points(points)
                        image_number += 1
                        frame += 1

    
                time_elapsed_seconds = k 

                for i in points:
                    i.change_opacity()
                graph.clear_patches()


                if preview == True and time_elapsed_seconds > preview_time:
                    return  
        animate()

        



            
