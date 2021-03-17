""" THIS FILE HOLDS THE TWO THEME RELATED FUNCTIONS"""

from tkinter import * 
from tkinter import messagebox
from tkmacosx import Button as BT
from View import customization_classes as custom 
from View import scrollable_frame


# called when the customize option is selected from the preferences menu
def customize_theme(root,main):
    #check if any animation is selected 
    if main.selected_animation == '':
        messagebox.showwarning("Import Error","No Theme Selected")
        return 
    else:
        selected_theme = main.selected_animation 

    # create a list called customizable elements from the instance of selected animation type stored in main.theme_data 
    for i in main.theme_data:
        if i.display_name == selected_theme:
            customizable_elements = i.customizable_elements 


    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    x_pos = root_x + 500
    y_pos = root_y + 200
    #create a top level window to display the customizable elements 
    top = Toplevel(bg = 'gray9')
    top.geometry(f'500x300+{x_pos}+{y_pos}')
    top.resizable(0,0)
    top.title("Customize Selected Theme")
    top.grab_set() 
    #create a horizontal scroll bar 
    scrollable_canvas = scrollable_frame.HorizontalScrolledFrame(top,height = 250, width = 500,bg = "gray9")
    scrollable_canvas.place(x = 0, y = 0, anchor = NW)
    # the top frame that holds all the customizable widgets 
    widget_holder = Frame(scrollable_canvas, bg = "gray9", width = 500, height = 250)
    widget_holder.pack(side = TOP)
    #bottom frame that holds the confirm button 
    bottom_frame = Frame(top, bg = "gray9", width = 500, height = 50)
    bottom_frame.pack(side = BOTTOM)

    #function to create a confirm button 
    def create_confirm_button(r,c):
        conf = BT(bottom_frame, bg = "gray6", fg = "white",height = 40, width = 120, borderless = TRUE, text = "Confirm Changes", command = lambda: make_changes(widget_list))
        conf.pack(side = LEFT)

    #makes changes to the elements in customizable elements based on the selected variable values 
    def make_changes(lst):
        for i in main.theme_data:
            if i.display_name == selected_theme:
                for j in i.customizable_elements:
                    if j[1] != "ENTRY":
                        if lst[i.customizable_elements.index(j)].selection != '':
                            j[2] = lst[i.customizable_elements.index(j)].selection 
                        else:
                            j[2] = lst[i.customizable_elements.index(j)].default_val
                    elif j[1] == "ENTRY":
                        j[2] = lst[i.customizable_elements.index(j)].checkvar.get() 

        top.destroy()

    #constructs widget list from customizable elements 
    def construct_widget_list():
        r = 0 #row number 
        c = 0 #column number 
        counter = 1
        output_list = []
        for i in customizable_elements: #i[0] == name, i[1] == type, i[2] == default_val, i[3] == items
            if i[1] == 'COLORBOX':
                wid = custom.ColorButton(i[0],i[2],r,c,widget_holder)
                output_list.append(wid) 
            elif i[1] == 'CHECKBOX':
                wid = custom.CheckBox(i[0],i[2],r,c,widget_holder)
                output_list.append(wid)  
            elif i[1] == 'DROPDOWN':
                wid = custom.Dropdown(i[0],i[2],i[3],r,c,widget_holder)
                output_list.append(wid)
            elif i[1] == 'ENTRY':
                if i[4] == "str":
                    wid = custom.EntryBox(i[0],i[2],r,c,widget_holder,i[3],'',i[4])
                elif i[4] == "int":
                    wid = custom.EntryBox(i[0],i[2],r,c,widget_holder,len(str(i[3][1])),i[3],i[4])

                output_list.append(wid)
            if counter < 7:
                r += 1
                counter += 1 
            if counter == 7:
                r = 0
                c += 2
                counter = 1

        create_confirm_button(r,c) 

        return output_list

    widget_list = construct_widget_list()

    for i in widget_list:
        i.construct()

#this function displays the theme properties of the selected theme 
def display_theme_properties(root,main):
    if main.selected_animation == '':
        messagebox.showwarning("Import Error","No Theme Selected")
        return 
    else:
        selected_theme = main.selected_animation 

    for i in main.theme_data:
        if i.display_name == selected_theme:
            customizable_elements = i.customizable_elements 
            theme_description = i.theme_description 

    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    x_pos = root_x + 500
    y_pos = root_y + 200
    top = Toplevel(bg = 'gray9')
    top.geometry(f'500x300+{x_pos}+{y_pos}')
    top.resizable(0,0)
    top.title("Theme Description")
    top.grab_set()

    title_holder = Frame(top,bg = "gray6",width = 500, height = 50)
    title_holder.propagate(0)
    title_holder.pack(side = TOP)

    title_label = Label(title_holder,bg = "gray6", text = f'{selected_theme} Theme', fg = "white", font = ("Arial", 25))
    title_label.pack(side = TOP, pady = 10)


    description_holder = Frame(top, bg = "gray9", width = 500, height = 200)
    description_holder.propagate(0)
    description_holder.place(x = 0, y = 50)
    description_label = Label(description_holder,bg = "gray9", text = theme_description[0], fg = "white", font = ("Arial", 14), wraplength = 500)
    description_label.pack(side = TOP, pady = 20)


    bottom_frame = Frame(top, bg = "gray6", width = 500, height = 50)
    bottom_frame.propagate(0)
    bottom_frame.pack(side = BOTTOM)
    bottom_label = Label(bottom_frame, bg = "gray6", text = theme_description[1], fg = "white", font = ("Arial", 12), wraplength = 500)
    bottom_label.pack(side = TOP, pady = 10)

    
     


    

    




