import matplotlib.pyplot as plt
import mplcyberpunk 
import matplotlib.image as image 
from utility import frame_rate_note
from tracklist_functions import create_monophonic, find_pitch_range_monophonic, create_timecode_hash
import matplotlib

matplotlib.use("TkAgg")


class VideoGameTheme:
    def __init__(self,tracklist):
        self.category = 'MONOPHONIC'
        self.display_name = 'Arcade Game'
        self.tracklist = tracklist 

        self.grid_colour = ['Grid Colour','COLORBOX','#d600ff']
        self.grid_width = ["Grid Width","ENTRY",0.3,(0,1),"int"]
        self.background_colour = ['Background Colour','COLORBOX',"black"]
        self.line_colour = ['Line Colour','COLORBOX','#00b8ff']
        self.line_react = ['Line React','CHECKBOX',True] 
        self.line_highlight = ['Line Highlight','COLORBOX','#FFFFFF']
        self.box_colour = ['Box Colour','COLORBOX','#d600ff']
        self.grid_line_style = ["Grid Line Style","DROPDOWN","solid",["solid","dashed","dotted","extra dotted"]]
        self.obstacle_line_style = ["Obstacle Line Style","DROPDOWN","solid",["solid","dashed","dotted","extra dotted"]]
        self.grid_on = ['Grid','CHECKBOX',True] 

        self.customizable_elements = [self.grid_colour,self.grid_width,self.background_colour,self.line_colour,self.line_react,self.line_highlight,self.box_colour,self.grid_line_style,self.obstacle_line_style,self.grid_on]

        self.theme_description = ["Music is an art form flooding with information just waiting to be visualized in exciting ways. This theme is my attempt at visualizing something as simple as a single melody line and turning it into a run and dodge video game level. The algorithm automatically analyses the melodic line from the MIDI file and creates the animation for you. But, in case you aren't satisfied with the outcome you can always manually disable instruments from the instrument panel. Note that there are an extra 4 seconds added at the beginning of the Animation.","Created by Aman Trivedi as part of the Maestoso Project."]

    def ANIMATE(self,upd_project_tracklist,upd_PPQN,upd_fps,upd_output_dir,upd_preview,upd_preview_time):
        tracklist = self.tracklist
        project_tracklist = upd_project_tracklist

        PPQN = upd_PPQN
        polyphonic_list = create_timecode_hash(project_tracklist)
        monophonic_list = create_monophonic(polyphonic_list)
        pitch_range = find_pitch_range_monophonic(monophonic_list)
        fps = upd_fps
        output_dir = upd_output_dir
        preview = upd_preview
        preview_time = upd_preview_time
        dpi = 120 
        aspect_ratio = (16,9)
        margin = 200 
        yspace = 20
        measures = 1
        base_note_length = 4 #quarter note


        line_styles = {"solid":"solid","dotted":"dotted","dashed":"dashed","extra dotted":(0,(1,10))}

        grid_colour = self.grid_colour[2]
        grid_width = float(self.grid_width[2])
        background_colour = self.background_colour[2]
        line_colour = self.line_colour[2]
        line_react = self.line_react[2]
        line_highlight = self.line_highlight[2]
        box_colour = self.box_colour[2]
        grid_line_style = line_styles.get(self.grid_line_style[2])
        obstacle_line_style = line_styles.get(self.obstacle_line_style[2])
        grid_on = self.grid_on[2]

        def pix_to_inch(size):
            one_pix = 1/dpi 
            return one_pix * size 


        def adjust_dimensions(pitch_range):
            height = (len(pitch_range) * yspace) + margin + int(margin/2)
            width = round((height * aspect_ratio[0])/aspect_ratio[1])
            return (width,height)


        width = adjust_dimensions(pitch_range)[0]
        height = adjust_dimensions(pitch_range)[1]
        character_height = 80


        def box_location_x(note):
            if note.start_ticks == 0:
                x_pos = 0 + width
                return x_pos # if note onset is 0 ticks 
            else:
                distance_length = note.start_ticks/PPQN #The total distance that occurs before the note 
                nx = 1/distance_length
                x_pos = (width / (nx * (base_note_length * measures))) + width
                return x_pos

        def box_location_y(note):
            max_position = height - (margin/2) # location of highest note in pitchrange will always be at margin/2
            max_note = max(pitch_range)
            difference = max_note - note.pitch # find difference current note value and max note value to obtain it's position in acccordance to margin/2 
            location = max_position - (difference * yspace)
            return location 


        class VerticalLines:
            def __init__(self,x,y,start_time):
                self.x = x 
                self.y = y 
                self.start_time = start_time 
                self.colour = line_colour


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
                self.verticallines = []
                self.image_number = 0
                self.boxlocationx = width/2
                self.gridxloc = []
                self.gridyloc = []
                self.fig.set_facecolor(background_colour)
                self.ax.set_facecolor(background_colour)

                for j in monophonic_list:
                    self.verticallines.append(VerticalLines(box_location_x(j),box_location_y(j),j.start_time))

                self.construct_gridlines()

            def construct_gridlines(self):
                x_end = self.verticallines[-1].x
                y_end = height 
                x_interval = width/8 
                y_interval = height/8 
                x = 0
                y = 0
                while x < x_end:
                    self.gridxloc.append(x)
                    x += x_interval

                while y < y_end:
                    self.gridyloc.append(y)
                    y += y_interval


            def plot_gridlines(self):
                if grid_on == False:
                    return 
                for i in self.gridxloc:
                    if i > width:
                        break 
                    elif i < 0:
                        continue 
                    else:
                        plt.vlines(i,ymin = 0, ymax = height, color = grid_colour,linewidth = grid_width,linestyle = grid_line_style)
                for i in self.gridyloc:
                    if i > height:
                        break
                    elif i < 0:
                        continue 
                    else:
                        plt.hlines(i,xmin = 0, xmax = self.verticallines[-1].x, color = grid_colour,linewidth = grid_width,linestyle = grid_line_style)

                
            def plot_graph(self,lst):
                for i in lst:  
                    if i.x > width:
                        break 
                    elif i.x < 0:
                        continue 
                    else:
                        if i.x > self.boxlocationx and i.x < self.boxlocationx + 20:
                            if line_react == True:
                                i.colour = line_highlight # if user selects to highlight the lines
                            else:
                                i.colour = line_colour
                        else:
                            i.colour = line_colour
                        plt.vlines(i.x, ymin=0, ymax=i.y, color = i.colour,linestyle = obstacle_line_style)
                        plt.vlines(i.x, ymin=i.y + character_height, ymax=height, color = i.colour,linestyle = obstacle_line_style)


            def clear_plot(self):
                plt.cla()
                plt.xlim([0,width])
                plt.ylim([0,height])
                plt.grid(False)
                self.fig.set_facecolor(background_colour)
                self.ax.set_facecolor(background_colour)
                self.ax.set_xticklabels([])
                self.ax.set_yticklabels([])
                self.ax.axis('off')
                

            def clear_patches(self):
                self.ax.patches = []


            def create_character(self):
                plt.gca().add_patch(plt.Rectangle((self.boxlocationx,height/2),20,20,linewidth = 1, edgecolor = box_colour,facecolor = box_colour))


            def calculate_xspeed(self,f1,f2,startpos,endpos): #end pos = current position, start pos = destination 
                distance = endpos - startpos
                diff = f2 - f1 
                if diff != 0:
                    speed = distance/diff 
                else:
                    speed = distance 
                return speed 

            def calculate_yspeed(self,f1,f2,endpos):
                distance = endpos - ((height/2) - 30)
                diff = f2 - f1 
                if diff != 0:
                    speed = distance/diff 
                else:
                    speed = distance 
                return speed 


            def construct_plot(self):
                self.create_character()
                self.plot_graph(self.verticallines)
                self.plot_gridlines()
                plt.savefig(f'{output_dir}/frame_{self.image_number}.png')
                self.clear_plot()
                self.clear_patches()
                self.image_number += 1 

            def adjust_xy(self,lst,x,y):
                for i in lst:
                    i.x -= x 
                    i.y -= y 

                for i in range(len(self.gridxloc)):
                    self.gridxloc[i] = self.gridxloc[i] - x 

                for i in range(len(self.gridyloc)):
                    self.gridyloc[i] = self.gridyloc[i] - y


            def entry_animation(self,startposx,endposy):
                frame = 0 
                time = 4 * fps + frame_rate_note(self.verticallines[0].start_time,fps)
                xspeed = self.calculate_xspeed(0,time,self.boxlocationx,self.verticallines[0].x)
                yspeed = self.calculate_yspeed(0,time,endposy)
                while frame < time:
                    self.construct_plot()
                    self.adjust_xy(self.verticallines,xspeed,yspeed)
                    frame += 1


            def animate_theme(self):
                self.entry_animation(self.verticallines[0].x,self.verticallines[0].y)
                previous_time = self.verticallines[0].start_time 
                time_list = []
                for i in self.verticallines:
                    time_list.append(i.start_time)


                for i in time_list:
                    if i == self.verticallines[0].start_time:
                        continue 
                    frames = 0 
                    f1 = frame_rate_note(previous_time,fps)
                    f2 = frame_rate_note(i,fps)
                    note = self.verticallines[time_list.index(i)]
                    xspeed = self.calculate_xspeed(f1,f2,self.boxlocationx,note.x)
                    yspeed = self.calculate_yspeed(f1,f2,note.y)
                    while frames < f2 - f1: 
                        self.construct_plot()
                        self.adjust_xy(self.verticallines,xspeed,yspeed)
                        frames += 1 

                    previous_time = i 
                    if preview == True and previous_time > preview_time:
                        return

        Graph = GraphAnimation()
        Graph.animate_theme()
