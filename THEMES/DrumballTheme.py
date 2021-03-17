import matplotlib.pyplot as plt
from utility import frame_rate_note
from tracklist_functions import create_drum_hash, find_all_drums
from pretty_midi import note_number_to_drum_name
from PIL import ImageFont
from os.path import join, dirname, abspath, pardir
from os import getcwd
from sys import argv
import matplotlib

matplotlib.use("TkAgg")

class DrumballTheme:
    def __init__(self,tracklist):
        self.category = 'RHYTHM'
        self.display_name = 'Bouncing Balls'
        self.tracklist = tracklist 
        self.background_color = ['Background Colour','COLORBOX','#092047',[]]
        self.ball_color = ['Ball Colour','COLORBOX','#fe00fe',[]]
        self.box_color = ['Box Colour','COLORBOX','#defe47',[]]
        self.line_color = ['Slope Colour','COLORBOX','#ff6e27',[]]
        self.inst_name = ['Instrument Names','CHECKBOX',True,[]]
        
        self.customizable_elements = [self.background_color,self.ball_color,self.box_color,self.line_color,self.inst_name]
        self.theme_description = ["Have you ever wondered what it would be like if numerous balls were dropped from a height on a drum set? Well someone did and their idea was the main inspiration behind this theme. Inspired by the works of 'DoodleChaos', this theme serves as a pseudo-physics simulation of musical rhythms. Note that there is an extra second added in the beginning of the animation.", "Created by Aman Trivedi as part of the Maestoso Project."]
        
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
        box_y_pos = 300

        rhythm_tracklist = create_drum_hash(project_tracklist)

            
        name_list = find_all_drums(project_tracklist,name=False)

        background_color = self.background_color[2]
        ball_color = self.ball_color[2]
        box_color = self.box_color[2]
        slope_color = self.line_color[2]
        instrument_display = self.inst_name[2]


        size_coefficient = 0 #determines the box_length division based on length of name_list 
        horizontal_spacing_coefficient = 0 #determines the division of the horizontal_spacing based on length of name_list
        if len(name_list) < 3:
            size_coefficient = 4
            horizontal_spacing_coefficient = 2
        elif len(name_list) > 2:
            size_coefficient = 2
            horizontal_spacing_coefficient = 1

        box_length = (width/len(name_list))/size_coefficient
        box_height = (9/16) * box_length 
        drumbox_list = []
        slope_offset = 40 # how much the slope is away from the box it rests on - on the x axis 
        slope_ypos = height 
        slope_height = 200

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

        
        class DrumBox:
            def __init__(self,pitch,x,y):
                self.pitch = pitch
                self.x = x
                self.y = y
                self.length = box_length
                self.height = box_height
                self.colour = box_color + '80'
                self.highlight_colour = box_color
                self.active = False 

            def box_draw(self):
                if self.active == False:
                    colour = self.colour 
                elif self.active == True:
                    colour = self.highlight_colour
                return plt.Rectangle((self.x,self.y),self.length,self.height,linewidth = 1, edgecolor = colour,facecolor = colour)

        class Slope:
            def __init__(self,x,y,pitch):
                self.x1 = x - slope_offset
                self.y1 = y 
                self.pitch = pitch
                
                self.x2 = self.x1 + (box_length/2)
                self.y2 = self.y1 - slope_height

                self.slope = (self.y2 - self.y1)/(self.x2 - self.x1)
                self.b = self.y1 - (self.x1 * self.slope)

            def plot_slope(self):
                plt.plot([self.x1,self.x2],[self.y1,self.y2],color = slope_color)


        def create_slope(lst): # function to create slope object 
            slope_list = []
            for i in lst:
                slope_list.append(Slope(i.x,slope_ypos,i.pitch))
            return slope_list

        def draw_slope(lst): # function that runs the draw slope method for each slope object in slopelist 
            for i in lst:
                i.plot_slope()
                    

        def find_horizontal_spacing(): # finds the appropriate spacing between each drum box object 
            difference = width - (box_length * len(name_list))
            horizontal_spacing = difference/(len(name_list) * horizontal_spacing_coefficient)
            return horizontal_spacing


        def create_drumbox(): # creates drum box objects and adds them to the drum_box list array 
            horizontal_spacing = find_horizontal_spacing()
            xpos = horizontal_spacing
            for i in name_list: 
                drumbox_list.append(DrumBox(i,xpos,box_y_pos))
                xpos += (box_length + horizontal_spacing)


        class Ball:
            def __init__(self,pitch,starting_time,ending_time):
                self.pitch = pitch
                self.radius = self.find_radius()
                self.x = 0
                self.y = height + self.radius 
                self.slope = 0
                self.b = 0
                self.initialize_values()
                self.starting_frame = frame_rate_note(starting_time,fps)
                self.ending_frame = frame_rate_note(ending_time,fps)
                self.find_time()
                self.find_distances()
                self.initial_velocity = 0 
                self.final_velocity = self.calculate_final_velocity()
                self.acceleration = self.calculate_acceleration_on_slope()
                self.frame = 0
                self.bounce = False 


            def find_time(self):
                self.total_time = self.ending_frame - self.starting_frame
                self.time_in_fall = round(self.total_time * (0.5))
                self.time_on_slope = self.total_time - self.time_in_fall

            def find_distances(self):
                self.distance_on_slope = ((slope_ypos - slope_height) + self.radius) - (slope_ypos + self.radius)
                self.distance_in_fall = ((box_y_pos + box_height) + self.radius) - ((slope_ypos - slope_height) + self.radius)


            def initialize_values(self):
                slope_list = create_slope(drumbox_list)
                for i in slope_list:
                    if i.pitch == self.pitch:
                        self.slope = i.slope
                        self.b = i.b 
                        self.x = i.x1 + (self.radius/2)

            def find_box_pos(self):
                for i in drumbox_list:
                    if i.pitch == self.pitch:
                        return i.x + (box_length/2)

            def find_radius(self):
                horizontal_spacing = find_horizontal_spacing()
                return horizontal_spacing/12

            def draw_ball(self):
                circle = plt.Circle((self.x, self.y), self.radius, color=ball_color)
                return circle 


            def calculate_final_velocity(self):
                return self.distance_in_fall/self.time_in_fall


            def calculate_acceleration_on_slope(self):
                return (2 * self.distance_on_slope)/(self.time_on_slope **2)

           


            def animate(self):
                plt.gca().add_patch(self.draw_ball())
                time1_start_frame = 0 # exact frame number at which time 0 starts 
                time2_start_frame = time1_start_frame + self.time_on_slope


                if self.frame < time2_start_frame: # if ball is sliding
                    self.y += self.initial_velocity
                    self.x = ((1/self.slope) * (self.y - self.b)) + (self.radius * 2)
                    self.initial_velocity += self.acceleration # causes acceleration 

                elif self.frame > time2_start_frame and self.frame < (time2_start_frame + self.time_in_fall): # if ball has left the slope and not yet touched the rectangle 
                    self.y += self.final_velocity
                    self.final_x_pos = self.x #constant x pos during fall 

                elif self.frame > time2_start_frame + self.time_in_fall:
                    box_border = box_y_pos + box_height + self.radius # the edge of the border 
                    maximum_bounce = box_border + 150
                    max_possible_speed = self.distance_in_fall # the maximum possible speed that can be attained before bounce

                    intercepts_y = box_border # the y dimension of both points 
                    point_a = (self.final_x_pos,intercepts_y) # x on the center of the rectangle and y on the edge of the rectangle 
                    point_b = (((self.final_x_pos + box_length/2) + find_horizontal_spacing()/2), intercepts_y) #intercept b on the center of the horizontal spacing 
                    vertex_y = box_border + ((self.final_velocity * maximum_bounce)/max_possible_speed) # highest point of the parabola on the y axis 
                    vertex_x = (point_a[0] + point_b[0])/2 # the x coordinate of the vertex along the y axis 
                    a = (point_a[1] - vertex_y)/((point_a[0] - vertex_x)**2) # value of a in vertex form 
                    xspeed = (point_b[0] - point_a[0])/self.time_in_fall # horizontal speed estimated from previous speed (max_speed)
                    
                    nframes_before_switch = (time2_start_frame + self.time_in_fall) + 1 #the frame count when the ball begins to bounce 
                    total_frames_before_switch = (point_b[0] - self.final_x_pos)/xspeed # the number of frames it will take for the ball to reach point_b[0], i.e, the center of the gap 

                    if self.frame >= nframes_before_switch and self.frame < (nframes_before_switch + total_frames_before_switch):
                        for i in drumbox_list:
                            if i.pitch == self.pitch:
                                    i.active = True 
                    else:
                        for i in drumbox_list:
                            if i.pitch == self.pitch:
                                i.active = False 
                                

                    self.x += xspeed 
                    self.y = (a * ((self.x - vertex_x)**2)) + vertex_y
                self.frame += 1


        def create_blocks(lst):
            for i in lst:
                plt.gca().add_patch(i.box_draw())


        def find_font_size(): #find ideal font size that fits within the rectangle size 
            drum_names = [(note_number_to_drum_name(i.pitch)) for i in drumbox_list]
            drum_lens = [len(i) for i in drum_names]
            max_length = max(drum_lens)
            max_text = drum_names[drum_lens.index(max_length)]
            max_font_size = 17 # font size when length of drum_box_list = 1
            fnt_width = pix_to_inch(box_length * 2)
            while fnt_width > pix_to_inch(box_length/2):
                max_font_size -= 1
                current_dir = getcwd()
                font_path = join(current_dir,'View/Resources/DejaVuSans-Bold.ttf')
                font = ImageFont.truetype(font_path,max_font_size)
                width_font, height_font = font.font.getsize(max_text)
                fnt_width = pix_to_inch(width_font[0])
            return max_font_size




        def annotate_graph(graph,drumbox_list,font_size): # function add text on the graph 
            for i in drumbox_list:
                txt_x = i.x + (box_length/2)
                txt_y = i.y + (box_height/2)
                drum_name = note_number_to_drum_name(i.pitch)
                if drum_name == '':
                    drum_name = 'Boom'
                graph.ax.annotate(drum_name,(txt_x,txt_y),color = 'white',weight = 'bold',fontsize = font_size ,ha = 'center', va ='center')
 

        def AnimateTheme(lst):
            graph = GraphAnimation()
            create_blocks(drumbox_list)
            draw_slope(create_slope(drumbox_list))
            image_number = 0 
            time_elapsed = 0 
            waiting_time = 1
            font_size = find_font_size()
            
            if instrument_display == True:
                annotate_graph(graph,drumbox_list,font_size)
            
            balls = []
            keys = list(rhythm_tracklist)
            for k, v in rhythm_tracklist.items():
                starting_time = time_elapsed # time at which the ball starts to fall
                ending_time = k + waiting_time # time at which the ball touches the rectangle 
                for j in v:
                    balls.append(Ball(j.pitch,starting_time,ending_time))

                frame = 0
                difference = frame_rate_note(ending_time,fps) - frame_rate_note(starting_time,fps)
                end_frames = (ending_time-starting_time)/2

                if k != keys[-1]:
                    while frame < round(difference/2): # stop the while loop at half the run time 
                        for b in balls:
                            if b.y < 0:
                                continue 
                            else:
                                b.animate()
                        plt.savefig(f'{output_dir}/frame_{image_number}.png')
                        graph.clear_patches()
                        create_blocks(drumbox_list)
                        frame += 1 
                        image_number += 1  
                else:
                    while frame < (5 * fps): # run for five seconds during the last onset 
                        for b in balls:
                            if b.y < 0:
                                continue 
                            else:
                                b.animate()
                        plt.savefig(f'{output_dir}/frame_{image_number}.png')
                        graph.clear_patches()
                        create_blocks(drumbox_list)
                        frame += 1 
                        image_number += 1  

                time_elapsed = ending_time - end_frames

                if preview == True and time_elapsed > preview_time:
                    return

        create_drumbox()
        AnimateTheme(drumbox_list)
        



        



