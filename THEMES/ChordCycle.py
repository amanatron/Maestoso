import matplotlib.pyplot as plt
from utility import frame_rate_note, pick_random_colour
from tracklist_functions import create_chord_list, create_timecode_hash
from math import sin, cos, pi 
import matplotlib

matplotlib.use('TkAgg')

class ChordCycle:
    def __init__(self,tracklist):
        self.category = 'HARMONY'
        self.display_name = 'Circle of Fifths'
        self.tracklist = tracklist
        self.background_color = ['Background Colour','COLORBOX','black']
        self.circle_color = ['Circle Colour','COLORBOX','white']
        self.beads_colour = ['Beads Colour','COLORBOX','white']
        self.grid_on = ['Grid','CHECKBOX',True]
        self.display_chords = ['Display Chords','CHECKBOX',True]
        self.grid_color = ['Grid Colour','COLORBOX','white']
        self.grid_width = ['Grid Width','ENTRY',0.1,(0,1),"int"]

        self.customizable_elements = [self.background_color,self.circle_color,self.beads_colour,self.grid_on,self.display_chords,self.grid_color,self.grid_width]

        self.theme_description = ["HARMONY! - that's all I have to say. This theme identifies and analyses the chords present in your MIDI file to create a chord based animation. Although, the algorithm is still not fully accurate and therefore it'd be best to use this theme with a bit of caution. Conversely, until the algorithm is developed further, you could feed an only chord MIDI file to get a more accurate output.","Created by Aman Trivedi as part of the Maestoso Project"]
        

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
        chord_list = create_chord_list(project_tracklist,PPQN)

            
        circle_of_fifths = ['C','G','D','A','E','B','F#','C#','G#','D#','A#','F']


        background_colour = self.background_color[2]
        circle_colour = self.circle_color[2]
        beads_colour = self.beads_colour[2]
        grid_on = self.grid_on[2]
        display_chords = self.display_chords[2]
        grid_color = self.grid_color[2]
        grid_width = self.grid_width[2]


        def pix_to_inch(size):
            one_pix = 1/dpi 
            return one_pix * size 
        
    
        class GraphAnimation:
            def __init__(self):
                plt.ioff()
                self.fig, self.ax = plt.subplots(figsize=(pix_to_inch(1280),pix_to_inch(720)),dpi=dpi)
                self.initialize_plot()

            def clear_patches(self):
                self.ax.patches = []

            def initialize_plot(self):
                plt.xlim([0,width])
                plt.ylim([0,height])
                if grid_on == True:
                    plt.grid(color = grid_color,linewidth = grid_width)
                elif grid_on == False:
                    plt.grid(False)
                self.ax.set_xticklabels([])
                self.ax.set_yticklabels([])
                self.fig.patch.set_facecolor(background_colour)
                self.ax.patch.set_facecolor(background_colour)
                self.ax.axis('off')

        class Circle:
            def __init__(self):
                self.center = (width/2,height/2)
                self.radius = width/4.5
                
            def draw(self):
                circle = plt.Circle((self.center[0], self.center[1]), self.radius, color=circle_colour,fill=False)
                plt.gca().add_patch(circle) 


        class Beads:
            def __init__(self,pitch,index):
                self.pitch = pitch 
                self.index = index 
                self.angle  = ((360/len(circle_of_fifths)) * self.index) * pi/180 
                self.x = ((width/4.5) * sin(self.angle)) + width/2 
                self.y = ((width/4.5) * cos(self.angle)) + height/2 
                self.radius = 10

            def draw(self):
                bead = plt.Circle((self.x, self.y), self.radius, color=beads_colour)
                plt.gca().add_patch(bead)
                annotate_x = (((width/4.5) * 1.2) * sin(self.angle)) + width/2 
                annotate_y = (((width/4.5) * 1.2) * cos(self.angle)) + height/2 
                plt.annotate(self.pitch,(annotate_x,annotate_y),color = circle_colour)


        class Chord:
            def __init__(self,chord,beads_list):
                self.notes = chord.notes 
                self.colour = pick_random_colour()
                self.index = [circle_of_fifths.index(i) for i in self.notes]
                self.index.sort()
                self.lines = self.form_lines(beads_list)


            def draw(self):
                plt.plot(self.lines[0],self.lines[1], color = self.colour,marker= 'o')


            def form_lines(self,beads_list):
                x_coords = []
                y_coords = []
                for i in self.index:
                    current_index = self.index.index(i)
                    current_coords = (beads_list[i].x, beads_list[i].y)
                    x_coords.append(current_coords[0])
                    y_coords.append(current_coords[1])
                    if i != self.index[-1]:
                        next_coords = (beads_list[self.index[current_index + 1]].x, beads_list[self.index[current_index + 1]].y)
                    else:
                        next_coords = (beads_list[self.index[0]].x, beads_list[self.index[0]].y)
                    x_coords.append(next_coords[0])
                    y_coords.append(next_coords[1])

                chord_coords = [x_coords,y_coords]
                return chord_coords

            def change_colour(self):
                if len(self.colour) == 7:
                    self.colour = self.colour + '4D'

                
        def animate():
            graph = GraphAnimation()
            circle = Circle()
            beads_list = []
            image_number = 0 
            time_elapsed = 0 
            chord_diagrams = []


            for i in circle_of_fifths:
                    beads_list.append(Beads(i,circle_of_fifths.index(i)))


            def initialize_drawings():
                circle.draw()
                for i in beads_list:
                    i.draw()

            def chord_name_annotation(chord_name):
                if display_chords == True:
                    ypos = height/2 
                    xpos = (width/2) + 400 
                    plt.annotate(chord_name,(xpos,ypos),color = beads_colour)
                else:
                    return 

            initialize_drawings()
            
            for i in chord_list:
                if len(chord_diagrams) == 3: # if chords within the diagram equate to 3 
                    chord_diagrams.clear()

                time_elapsed = i.start_time 

                if i.start_time == 0:
                    current_frame = 0 
                    next_frame = frame_rate_note(chord_list[chord_list.index(i) + 1].start_time,fps)
                else:
                    current_frame = frame_rate_note(i.start_time,fps)
                    if i != chord_list[-1]:
                        next_frame = frame_rate_note(chord_list[chord_list.index(i) + 1].start_time,fps)
                    else:
                        next_frame = frame_rate_note(5,fps)

                if i == chord_list[0] and i.start_time != 0:
                    pass 
                else:
                    chord_name_annotation(i.name)
                    chord_diagrams.append(Chord(i,beads_list))
                    for j in chord_diagrams:
                        j.draw()

                frame = 0 

                while frame < next_frame - current_frame:
                    plt.savefig(f'{output_dir}/frame_{image_number}.png')
                    image_number += 1
                    frame += 1 

                plt.cla()
                graph.initialize_plot()
                initialize_drawings()
                for j in chord_diagrams:
                    j.change_colour()
                if preview == True and time_elapsed > preview_time:
                    return 
        animate()










        

        

            