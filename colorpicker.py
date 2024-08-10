from tkinter import Tk, Canvas, Frame, Entry, LabelFrame, Button, PhotoImage
from PIL import Image, ImageTk, ImageDraw
import time

class SliderFunctions:
    
    # GET THE HIGHLIGHT POSITION ACCORDING TO INITIAL COLOR
    def get_position(self, initial_color):
        
        rgb_sorted = sorted(initial_color["rgb"])
        
        # GET THE X FACTOR
        if rgb_sorted[2] != 0:
            x_factor = round((rgb_sorted[0]) / rgb_sorted[2], 2)
        else:
            x_factor = 1.0
        
        # TAKE THE MIDDLE COLOR FROM WHITE SCALE TO BLACK SCALE
        if x_factor != 1:
            middle_color_from_white_to_black_scale = (rgb_sorted[1] - rgb_sorted[2]*x_factor) / (1 - x_factor)
        else:
            middle_color_from_white_to_black_scale = 0
        
        # TAKE THE MIDDLE COLOR FROM BLACK SCALE TO INICIAL COLOR
        if rgb_sorted[2] != 0: 
            middle_color_from_black_to_initial = int(middle_color_from_white_to_black_scale * (255 / rgb_sorted[2]))
        else:
            middle_color_from_black_to_initial = 0
        
        # IN CASE THE INITIAL COLOR IS FEWER THAN 0
        if middle_color_from_black_to_initial < 0:
            middle_color_from_black_to_initial = 0
            
        initial_color["rgb"][initial_color["rgb"].index(rgb_sorted[2])] = 255
        initial_color["rgb"][initial_color["rgb"].index(rgb_sorted[0])] = 0
        initial_color["rgb"][initial_color["rgb"].index(rgb_sorted[1])] = middle_color_from_black_to_initial
        
        red = initial_color["rgb"][0]
        green = initial_color["rgb"][1]
        blue = initial_color["rgb"][2]
        
        width_fraction = self.width/6
        

        if blue == 0:
                
            if red > green:
                self.slider_mouse_x = width_fraction * (green / 255)
            else:
                self.slider_mouse_x = width_fraction + width_fraction * ((255 - red) / 255)
                
        elif red == 0:
                       
            if green > blue:
                self.slider_mouse_x = 2 * width_fraction + width_fraction * (blue / 255)
            else:
                self.slider_mouse_x = 3 * width_fraction + width_fraction * ((255 - green) / 255)
                
        elif green == 0:
                
            if blue > red:
                self.slider_mouse_x = 4 * width_fraction + width_fraction * (red / 255)
            else:
                self.slider_mouse_x = 5 * width_fraction + width_fraction * ((255 - blue) / 255)
        
        self.color = self.convert_color_to_dict((red, green, blue))
        
        self.slider_mouse_x = int(self.slider_mouse_x + self.slider_root_x) 
        
        self.selected_cell = self.highlight()
        
    def get_color(self, col):
        fraction = (1529 * (col/(self.width - 1)))
        position = fraction // 255
        segment = fraction % 255

        if position == 0: # RED TO YELLOW
            red = 255
            green = int(segment)
            blue = 0
        elif position == 1: # YELLOW TO GREEN
            red = 255 - int(segment)
            green = 255
            blue = 0
        elif position == 2: # GREEN TO CYAN
            red = 0
            green = 255
            blue = int(segment)
        elif position == 3: # CYAN TO DARK BLUE
            red = 0
            green = 255 - int(segment)
            blue = 255
        elif position == 4: # DARK BLUE TO PINK
            red = int(segment)
            green = 0
            blue = 255
        else: # PINK TO RED
            red = 255
            green = 0
            blue = 255 - int(segment)
        
        return self.convert_color_to_dict((red, green, blue))
        
    def convert_color_to_dict(self, color):
        # WHEN THE INPUT IS HEXADECIMAL "#FFFFFF" OR "#FFF"
        if type(color) == str:
            
            hex_color = color.lstrip("#").upper()
            
            # TO HANDLE WHEN THE LENGTH OF HEXADECIMAL STRING IS 3 OR 6
            if len(hex_color) == 3:
                color = (int(hex_color[0] + hex_color[0], 16), int(hex_color[1] + hex_color[1], 16), int(hex_color[2] + hex_color[2], 16))
            else:
                color = (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))
            
            red = color[0]
            green = color[1]
            blue = color[2]
            
            color = {"hexadecimal": "#{:02X}{:02X}{:02X}".format(red, green, blue),
                      "rgb": [red, green, blue]}
        
        # WHEN THE INPUT IS RGB LIST [R, G, B] OR TUPLE (R, G, B)
        elif type(color) == list or type(color) == tuple:
            red = color[0]
            green = color[1]
            blue = color[2]
            
            color = {"hexadecimal": "#{:02X}{:02X}{:02X}".format(red, green, blue),
                      "rgb": [red, green, blue]}
        
        return color
    
    def highlight(self):
        # TO ERASE THE CELL BORDER SELECTED PREVIUOSLY
        if self.selected_cell:
            self.canvas.delete(self.selected_cell)
            
        # CREATE AN IMAGE WITH TRASPARENT BACGROUND
        img = Image.new("RGBA", (self.thumb_diameter + 1, self.thumb_diameter + 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # DRAW THE SLIDER
        draw.ellipse((0, 0, self.thumb_diameter, self.thumb_diameter), fill=self.color["hexadecimal"], outline=self.thumb_border_color, width=self.thumb_border)
        
        # CONVERT THE IMAGE TO A PHOTOIMAGE
        self.highlight_image = ImageTk.PhotoImage(img)
        
        # CREATE A NEW HIGHLIGHT
        self.highlight_id = self.canvas.create_image(self.slider_mouse_x - self.thumb_radius, self.slider_root_y + self.height // 2 - self.thumb_radius, image=self.highlight_image, anchor="nw")

    # SCROLL THE SLIDER'S THUMB TO RIGHT WHEN THE USER PRESS THE RIGHT ARROW KEY
    def on_right_arrow(self, event):
        if self.focused:
            if self.slider_mouse_x < self.width + self.slider_root_x - 1:
                self.slider_mouse_x += 1
                self.selected_cell = self.highlight()
                self.color = self.get_color(self.slider_mouse_x - self.slider_root_x)
                if self.gradient_picker != None:
                    self.gradient_picker.draw_gradient(self.color)
                    self.gradient_picker.update_hexadecimal_entry()
                    self.gradient_picker.update_rgb_entry()
    
    # SCROLL THE SLIDER'S THUMB TO LEFT WHEN THE USER PRESS THE LEFT ARROW KEY
    def on_left_arrow(self, event):
        if self.focused:
            if self.slider_mouse_x > self.slider_root_x:
                self.slider_mouse_x -= 1
                self.selected_cell = self.highlight()
                self.color = self.get_color(self.slider_mouse_x - self.slider_root_x)
                if self.gradient_picker != None:
                    self.gradient_picker.draw_gradient(self.color)
                    self.gradient_picker.update_hexadecimal_entry()
                    self.gradient_picker.update_rgb_entry()
    
    # WHEN THE USER PRESS DOWN THE LEFT MOUSE BUTTON TO CHOOSE THE COLOR
    def start_picking(self, event):
        row = event.y
        self.canvas.configure(cursor="hand2")
        if 0 < row < self.canvas.winfo_height():
            self.slider_mouse_x = event.x
            self.pick_color(event)
            

    # WHEN THE USER PRESS DOWN THE LEFT MOUSE BUTTON AND MOVE THE MOUSE TO CHOOSE THE COLOR
    def pick_color(self, event):
        self.slider_mouse_x = event.x
        if self.slider_mouse_x < self.slider_root_x:
            self.slider_mouse_x = self.slider_root_x
        if self.slider_mouse_x > self.slider_root_x + self.width:
            self.slider_mouse_x = self.slider_root_x + self.width - 1
            
        self.color = self.get_color(self.slider_mouse_x - self.slider_root_x)
        self.selected_cell = self.highlight()
        

    # WHEN THE USER RELEASE THE MOUSE LEFT BUTTON
    def stop_picking(self, event):
        self.canvas.configure(cursor="arrow")

        if self.gradient_picker != None:
            self.gradient_picker.draw_gradient(self.color)    
            self.gradient_picker.update_hexadecimal_entry()
            self.gradient_picker.update_rgb_entry()
    
    def on_key_press(self, event):
        if event.widget == self.gradient_picker.hexadecimal_entry_label_frame:
            hex_color = event.widget.get().strip().lstrip("#").upper()
            if len(hex_color) == 3 or len(hex_color) == 6:
                self.get_position(self.convert_color_to_dict("#" + hex_color))
                self.gradient_picker.initial_color = self.gradient_picker.convert_color_to_dict("#" + hex_color)
                self.gradient_picker.draw_gradient(self.color)
                
                if self.gradient_picker.rgb_entry_label_frame != None:
                    self.gradient_picker.rgb_entry_label_frame.delete(0, "end")
                    self.gradient_picker.rgb_entry_label_frame.insert(0, str(self.gradient_picker.convert_color_to_dict("#" + hex_color)["rgb"]).replace("[", "").replace("]", ""))
                    self.gradient_picker.display.frame.configure(bg="#" + hex_color)
                    
        elif event.widget == self.gradient_picker.rgb_entry_label_frame:
            rgb_color = event.widget.get().split(",")
            if len(rgb_color) == 3 and " " not in rgb_color and "" not in rgb_color:
                
                if len([True for num in rgb_color if int(num.strip()) > 255]) == 0:
                    rgb_color = [int(num.strip()) for num in rgb_color]
                    self.get_position(self.convert_color_to_dict(rgb_color))
                    self.gradient_picker.initial_color = self.gradient_picker.convert_color_to_dict(rgb_color)
                    self.gradient_picker.draw_gradient(self.color)
                    
                    if self.gradient_picker.hexadecimal_entry_label_frame != None:
                        self.gradient_picker.hexadecimal_entry_label_frame.delete(0, "end")
                        self.gradient_picker.hexadecimal_entry_label_frame.insert(0, self.gradient_picker.convert_color_to_dict(rgb_color)["hexadecimal"])
                        self.gradient_picker.display.frame.configure(bg=self.gradient_picker.convert_color_to_dict(rgb_color)["hexadecimal"])
                        
    def check_focus(self, event):
        if event.widget == self.canvas:
            self.focused = True
        else:
            self.focused = False

class GradientSlider(SliderFunctions):
    def __init__(self, master, bg="#333333", x=None, y=None, width=255, height=5, initial_color="#FF0000", thumb_border_color="#333333", thumb_radius=12, thumb_border=3, gradient_picker=None) -> None:
        # DEFINING GRADIENTSLIDER CLASS VARIABLES
        self.master = master
        self.root = self.master.winfo_toplevel()
        self.bg = bg
        self.width = width
        self.height = height
        self.thumb_border_color = thumb_border_color
        self.thumb_border = thumb_border
        self.thumb_radius = thumb_radius
        self.gradient_picker = gradient_picker
        self.slider_mouse_x = 0
        self.slider_root_x = x
        self.slider_root_y = y
        self.selected_cell = None
        self.slider_image_id = None
        self.thumb_diameter = thumb_radius * 2
        self.focused = False
        
        # CREATE THE GRADIENT SLIDER CANVAS
        self.canvas = Canvas(self.master, bg=self.bg, width=self.width, height=self.height, highlightthickness=0)
        
        # BINDING EVENTS TO MOUSE ACTIONS
        self.canvas.bind("<Button-1>", self.start_picking)
        self.canvas.bind("<B1-Motion>", self.pick_color)
        self.canvas.bind("<ButtonRelease-1>", self.stop_picking)
        self.canvas.winfo_toplevel().bind("<Button-1>", self.check_focus)
        self.canvas.winfo_toplevel().bind("<KeyPress>", self.on_key_press)
        
        # BINDING EVENTS TO ARROW KEYS ACTIONS
        self.canvas.winfo_toplevel().bind("<Right>", self.on_right_arrow)
        self.canvas.winfo_toplevel().bind("<Left>", self.on_left_arrow)

        SliderFunctions.__init__(self)
        
        self.initial_color = self.convert_color_to_dict(initial_color)
        
        
    def grid(self, row=None, column=None, padx=None, pady=None, ipadx=30, ipady=30, sticky="N"):
        if self.slider_root_x == None:
            self.slider_root_x = ipadx
        if self.slider_root_y == None:
            self.slider_root_y = ipady
        
        # DRAW SLIDER
        self.draw_slider()
        
        # PUT THE GRADIENT SLIDER ONTO SCREEN
        self.canvas.grid(row=row, column=column, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=sticky)
        
        # GET THE INITIAL COLOR HIGHLIGHT POSITION ON SCREEN
        self.get_position(self.initial_color)
        
        # DRAW THE GRADIENT PICKER BASED ON THE INITIAL COLOR
        if self.gradient_picker != None:
            self.gradient_picker.draw_gradient(self.color)
        
    def pack(self, side=None, fill=None, expand=None, padx=None, pady=None, ipadx=30, ipady=30, anchor=None):
        if self.slider_root_x == None:
            self.slider_root_x = ipadx
        if self.slider_root_y == None:
            self.slider_root_y = ipady

        # DRAW SLIDER
        self.draw_slider()
        
        self.canvas.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, anchor=anchor)

        # GET THE INITIAL COLOR HIGHLIGHT POSITION ON SCREEN
        self.get_position(self.initial_color)
        
        # DRAW THE GRADIENT PICKER BASED ON THE INITIAL COLOR
        if self.gradient_picker != None:
            self.gradient_picker.draw_gradient(self.color)
        
    def draw_slider(self):
        slider_image = Image.new("RGB", (self.width, self.height))
        pixels = slider_image.load()
        
        # DRAW THE GRADIENT SLIDER
        for col in range(0, self.width):
            for row in range(0, self.height):
                self.color = self.get_color(col)
                pixels[col, row] = tuple(self.color["rgb"])
        
        # CONVERT THE PILLOW IMAGE TO PHOTOIMAGE
        self.slider_image = ImageTk.PhotoImage(slider_image)
        
        # TO REMOVE THE CANVAS' LAST IMAGE, IF IT EXISTS
        if self.slider_image_id is not None:
            self.canvas.delete(self.slider_image_id)
            
        # CREATE THE GRADIENT PICKER'S IMAGE
        self.slider_image_id = self.canvas.create_image(self.slider_root_x, self.slider_root_y, anchor="nw", image=self.slider_image)
    
class PickerFunctions:
    
    def convert_color_to_dict(self, color):

        # WHEN THE INPUT IS HEXADECIMAL "#FFFFFF" OR "#FFF"
        if type(color) == str:
            
            hex_color = color.lstrip("#").upper()
            
            # TO HANDLE WHEN THE LENGTH OF HEXADECIMAL STRING IS 3 OR 6
            if len(hex_color) == 3:
                color = (int(hex_color[0] + hex_color[0], 16), int(hex_color[1] + hex_color[1], 16), int(hex_color[2] + hex_color[2], 16))
            else:
                color = (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))
                
            red = color[0]
            green = color[1]
            blue = color[2]
            
            color = {"hexadecimal": "#{:02X}{:02X}{:02X}".format(red, green, blue),
                      "rgb": [red, green, blue]}  
        
        # WHEN THE INPUT IS RGB LIST [R, G, B] OR TUPLE (R, G, B)
        elif type(color) == list or type(color) == tuple:
            
            red = color[0]
            green = color[1]
            blue = color[2]
            
            color = {"hexadecimal": "#{:02X}{:02X}{:02X}".format(red, green, blue),
                      "rgb": [red, green, blue]}
        
        return color
    
    # CALCULATE THE MARKER POSITION WHEN THE USER GIVE THE PROGRAM A INITIAL COLOR
    def get_position(self, initial_color):
        
        # TO SORT THE COLOR FROM THE LOWEST TO THE GREATEST VALUE
        rgb_sorted = sorted(initial_color["rgb"])
        
        print(rgb_sorted)
        
        # TO GET THE X FACTOR
        if rgb_sorted[2] != 0:
            x_factor = round((rgb_sorted[0]) / rgb_sorted[2], 2)
        else:
            x_factor = 1.0
        
        # TO GET THE Y FACTOR
        y_factor = round((rgb_sorted[2] / 255), 2)
        
        self.picker_mouse_x = round((self.width - 1) * x_factor + self.picker_root_x, 2)
        self.picker_mouse_y = round((1 - y_factor) * (self.height - 1) + self.picker_root_y, 2)
        
        self.update_marker()
    
    # TO GET THE HEXADECIMAL AND RGB COLOR PARAMS WHEN THE USER CHOOSE IT BASED ON CURSOR POSITION
    def get_color(self):
        y_factor = (1 - ((self.picker_mouse_y - self.picker_root_y) / (self.height - 1)))
        x_factor = ((self.picker_mouse_x - self.picker_root_x) / (self.width - 1))
        rgb_color = []
        for rgb in self.base_color["rgb"]:
            color_value = int((rgb + (255 - rgb) * x_factor) * y_factor)

            if 0 <= color_value <= 255:
                rgb_color.append(color_value)
            elif color_value < 0:
                rgb_color.append(0)
            else:
                rgb_color.append(255)
                
        return self.convert_color_to_dict(rgb_color)  
    
    # WHEN THE USER PRESS DOWN THE LEFT MOUSE BUTTON TO CHOOSE THE COLOR
    def start_picking(self, event):
        self.canvas.configure(cursor="hand2")
        self.picker_mouse_x = event.x
        self.picker_mouse_y = event.y
        if self.picker_root_x <= self.picker_mouse_x <= self.picker_root_x + self.width and self.picker_root_y <= self.picker_mouse_y < self.picker_root_y + self.height:
            self.color = self.get_color()
            self.update_marker()
            self.update_hexadecimal_entry()
            self.update_rgb_entry()
    
    # WHEN THE USER PRESS DOWN THE LEFT MOUSE BUTTON AND MOVE THE MOUSE TO CHOOSE THE COLOR
    def pick_color(self, event):
        self.picker_mouse_x = event.x
        self.picker_mouse_y = event.y
        
        # TO CHECK IF THE MOUSE IS INSIDE THE GRADIENT
        if self.picker_mouse_x < self.picker_root_x:
            self.picker_mouse_x = self.picker_root_x
        elif self.picker_mouse_x > self.picker_root_x + self.width:
            self.picker_mouse_x = self.picker_root_x + self.width
        if self.picker_mouse_y  < self.picker_root_y:
            self.picker_mouse_y = self.picker_root_y
        elif self.picker_mouse_y > self.picker_root_y + self.height:
            self.picker_mouse_y = self.picker_root_y + self.height
        
        # TO GET THE HEXADECIMAL AND RGB OF THE CHOOSEN COLOR
        self.color = self.get_color()
        self.update_marker()
        self.update_hexadecimal_entry()
        self.update_rgb_entry()
    
    # WHEN THE USER RELEASE THE MOUSE LEFT BUTTON
    def stop_picking(self, event):
        self.canvas.configure(cursor="arrow")
                
    # UPDATE THE GRADIENT PICKER'S MARKER
    def update_marker(self):
        # TO DESTROY THE DRAWN OLD MARKER
        if self.marker_id is not None:
            self.canvas.delete(self.marker_id)
        
        # CREATE AN IMAGE WITH TRASPARENT BACGROUND
        img = Image.new("RGBA", (self.marker_radius * 2 + 1, self.marker_radius * 2 + 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # DRAW THE GRADIENT PICKER MARKER
        draw.ellipse((0, 0, self.marker_radius * 2, self.marker_radius * 2), fill=self.color["hexadecimal"], outline=self.marker_border_color, width=self.marker_border)
        
        # CONVERT THE IMAGE TO A PHOTOIMAGE
        self.marker_image = ImageTk.PhotoImage(img)
        
        # CREATE A NEW MARKER
        self.marker_id = self.canvas.create_image(self.picker_mouse_x, self.picker_mouse_y, image=self.marker_image, anchor="center")
        
        if self.display != None:
            self.display.update_display(self.color["hexadecimal"])
    
    def update_hexadecimal_entry(self):
        if self.hexadecimal_entry_label_frame != None:
            self.hexadecimal_entry_label_frame.delete(0, "end")
            self.hexadecimal_entry_label_frame.insert(0, self.color["hexadecimal"])
    
    def update_rgb_entry(self):
        if self.rgb_entry_label_frame != None:
            self.rgb_entry_label_frame.delete(0, "end")
            self.rgb_entry_label_frame.insert(0, str(self.color["rgb"]).replace("[", "").replace("]", ""))
        
class GradientPicker(PickerFunctions):
    def __init__(self, master, bg="#333333", x=None, y=None, width=255, height=255, initial_color="#FF0000", marker_radius=12, marker_border=3, marker_border_color="#FFFFFF", display=None, hexadecimal_entry_label_frame=None, rgb_entry_label_frame=None) -> None:
        
        # DEFINING GRADIENTPICKER CLASS VARIABLES
        self.master = master
        self.bg = bg
        self.width = width
        self.height = height
        self.gradient_elements = []
        self.picker_root_x = x
        self.picker_root_y = y
        self.gradient_image_id = None
        self.marker_id = None
        self.marker_radius = marker_radius
        self.marker_border = marker_border
        self.marker_border_color = marker_border_color
        self.picker_mouse_x = None
        self.picker_mouse_y = None
        self.base_color = None
        self.initial_color = self.convert_color_to_dict(initial_color)
        self.color = self.initial_color
        self.display = display
        self.hexadecimal_entry_label_frame = hexadecimal_entry_label_frame
        self.rgb_entry_label_frame = rgb_entry_label_frame
        
        # CREATE THE GRADIENT PICKER CANVAS
        self.canvas = Canvas(self.master, bg=self.bg, width=self.width, height=self.height, highlightthickness=0)
        
        # BINDING EVENTS TO MOUSE ACTIONS
        self.canvas.bind("<Button-1>", self.start_picking)
        self.canvas.bind("<B1-Motion>", self.pick_color)
        self.canvas.bind("<ButtonRelease-1>", self.stop_picking)
        
        PickerFunctions.__init__(self)
        
     # TO PUT THE GRADIENT PRICKER'S CANVAS ONTO SCREEN VIA GRID
    def grid(self, row=None, column=None, padx=None, pady=None, ipadx=0, ipady=0, sticky=None):
        if self.picker_root_x == None:
            self.picker_root_x = ipadx
        if self.picker_root_y == None:
            self.picker_root_y = ipady
        self.canvas.grid(row=row, column=column, padx=padx, pady=pady, ipadx=self.picker_root_x, ipady=self.picker_root_y, sticky=sticky)
        
        if self.initial_color != None:
            self.get_position(self.initial_color)
            if self.hexadecimal_entry_label_frame != None:
                self.hexadecimal_entry_label_frame.insert(0, self.initial_color["hexadecimal"])
            if self.rgb_entry_label_frame != None:
                self.rgb_entry_label_frame.insert(0, str(self.initial_color["rgb"]).replace("[", "").replace("]", ""))
            self.initial_color = None
        
    def pack(self, side=None, fill=None, expand=None, padx=None, pady=None, ipadx=0, ipady=0, anchor=None):
        if self.picker_root_x == None:
            self.picker_root_x = ipadx
        if self.picker_root_y == None:
            self.picker_root_y = ipady
        self.canvas.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, anchor=anchor)
        
        if self.initial_color != None:
            self.get_position(self.initial_color)
            if self.hexadecimal_entry_label_frame != None:
                self.hexadecimal_entry_label_frame.insert(0, self.initial_color["hexadecimal"])
            if self.rgb_entry_label_frame != None:
                self.rgb_entry_label_frame.insert(0, str(self.initial_color["rgb"]).replace("[", "").replace("]", ""))
            self.initial_color = None
            
    # TO DRAW THE GRADIENT PICKER
    def draw_gradient(self, base_color):
        
        self.base_color = self.convert_color_to_dict(base_color)
        
        # CREATE AN IMAGE TO STORE THE GRADIENT PICKER
        gradient_image = Image.new("RGB", (self.width, self.height))
        pixels = gradient_image.load()

        # FILL THE IMAGE WITH GRADIENT
        for row in range(self.height):
            row_factor = round((1 - (row / (self.height - 1))), 2)
            for col in range(self.width):
                col_factor = round((col / (self.width - 1)), 2)
                rgb_color = [int((x + (255 - x) * col_factor) * row_factor) for x in self.base_color["rgb"]]
                pixels[col, row] = tuple(rgb_color)
            
        # CONVERT THE PILLOW IMAGE TO PHOTOIMAGE
        self.gradient_image = ImageTk.PhotoImage(gradient_image)

        # TO REMOVE THE CANVAS' LAST IMAGE, IF IT EXISTS
        if self.gradient_image_id is not None:
            self.canvas.delete(self.gradient_image_id)

        # CREATE THE GRADIENT PICKER'S IMAGE
        self.gradient_image_id = self.canvas.create_image(self.picker_root_x, self.picker_root_y, anchor="nw", image=self.gradient_image)
        
        # WHEN THE INITIAL COLOR IS GIVEN
        if self.initial_color != None:
            self.get_position(self.initial_color)
            self.initial_color = None
        else:
            self.color = self.get_color()
            self.update_marker()
            self.master.update()

# DISPLAY FUNCTIONS
class DisplayFunctions:
    def update_display(self, color):
        self.frame.configure(bg=color)

# DISPLAY CLASS
class Display(DisplayFunctions):
    def __init__(self, master, initial_color="#FF0000", width=120, height=40 , bd=1, bd_color="#FFFFFF"):
        
        DisplayFunctions.__init__(self)
        self.root = master.winfo_toplevel()
        
        self.frame = Frame(master, bg=initial_color, width=width, height=height, highlightbackground=bd_color, highlightcolor=bd_color, highlightthickness=bd)
    
    # WAYS TO PUT DISPLAY ONTO SCREEN
    def grid(self, row=None, column=None, padx=None, pady=None, ipadx=0, ipady=0, sticky=None):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=sticky)
        
    def pack(self, side=None, fill=None, expand=None, padx=None, pady=None, ipadx=0, ipady=0, anchor=None):
        self.frame.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, anchor=anchor)

# COLOR ENTRY LABEL FRAME FUNCTIONS
class ColorEntryLabelFrameFunctions:
    def update_color_entry(self, color):
        self.color_entry.configure(text=color)

# COLOR ENTRY LABEL FRAME CLASS
class ColorEntryLabelFrame(ColorEntryLabelFrameFunctions):
    
    def __init__(self, master, bg="#333333", fg="#FFFFFF", text="HEXADECIMAL", font=("helvetica", 12, "normal"), label_height=5, bd=1, bd_color="#FFFFFF", activebackgrund="#444444", width=11, icon=None, command=None):
        ColorEntryLabelFrameFunctions.__init__(self)
        self.root = master.winfo_toplevel()
        self.label_height = label_height
        
        self.label_frame = LabelFrame(master, text=text, font=(font[0], font[1] - 1, font[2]), bg=bg, fg=fg, bd=0)
        
        self.frame = Frame(self.label_frame, bg=bg, highlightthickness=bd, highlightbackground=bd_color, highlightcolor=bd_color)
        
        self.color_entry = Entry(self.frame, bg=bg, fg=fg, font=font, width=width, bd=0)
        
        self.copy_button = Button(self.frame, bg=bg, bd=0, activebackground=activebackgrund, cursor="hand2", image=icon, command=command)
    
    # WAYS TO PUT COLOR ENTRY LABEL FRAME ONTO SCREEN
    def grid(self, row=None, column=None, padx=None, pady=None, ipadx=0, ipady=0):
        self.label_frame.grid(row=row, column=column, padx=padx, pady=pady)
        self.frame.grid(pady=(self.label_height, 0), ipadx=ipadx, ipady=ipady)
        self.color_entry.grid(row=0, column=0, padx=(5, 0), ipadx=0, ipady=0)
        self.copy_button.grid(row=0, column=1, ipadx=3, ipady=3)
        
    def pack(self, side=None, fill=None, expand=None, padx=None, pady=None, ipadx=0, ipady=0, anchor=None):
        self.label_frame.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady, anchor=anchor)
        self.frame.pack(pady=(self.label_height, 0), ipadx=ipadx, ipady=ipady)
        self.color_entry.pack(padx=(5, 0), ipadx=0, ipady=0)
        self.copy_button.pack(ipadx=3, ipady=3)

# TO CREATE THE COLOR PICKER
class ColorPicker:
    def __init__(self, initial_color="#FF0000", theme="dark"):
        
        # CREATING THE WINDOW
        self.root = Tk()
        self.root.rowconfigure(0, weight=1)
        self.root.title("Color Picker")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # SET UP THE CHOOSEN THEME
        if theme.upper() == "DARK": # DARK
            bg = "#333333"
            fg = "#FFFFFF"
            activebackground = "#444444"
            bd_color = "#FFFFFF"
            
            self.copy_icon = PhotoImage(file=r"icons\content_copy_dark.png").subsample(3)
            self.check_icon = PhotoImage(file=r"icons\check_dark.png").subsample(3)
            self.cancel_icon = PhotoImage(file=r"icons\cancel_dark.png").subsample(3)
            
        else: # LIGHT
            bg = "#FFFFFF"
            fg = "#333333"
            activebackground = "#CCCCCC"
            bd_color = "#333333"
            
            self.copy_icon = PhotoImage(file=r"icons\content_copy_light.png").subsample(3)
            self.check_icon = PhotoImage(file=r"icons\check_light.png").subsample(3)
            self.cancel_icon = PhotoImage(file=r"icons\cancel_light.png").subsample(3)
        
        # CHANGE THE WINDOW BACKGROUND COLOR ACCORDING TO THE THEME
        self.root.configure(background=bg)
        
        # THE RIGHT FRAME THAT KEEP THE DISPLAY, COLOR ENTRY LABEL FRAMES (HEXADECIMAL AND RGB) AND THE CONFIRM AND CANCEL BUTTONS
        self.second_frame = Frame(self.root, bg=bg)
        self.second_frame.columnconfigure(0, weight=1)
        self.second_frame.grid(row=0, column=1, padx=(0, 30), pady=(25, 0), sticky="NSEW")
        
        # CREATE A DISPLAY TO SHOW THE CHOOSEN COLOR OF THE GRADIENT PICKER
        self.display = Display(self.second_frame, bd_color=bd_color)
        self.display.grid(sticky="EW")
        
        # CREATE AN ENTRY TO DISPLAY THE CHOOSEN COLOR HEXADECIMAL CODE
        self.hexadecimal_entry_label_frame = ColorEntryLabelFrame(self.second_frame, text="HEXADECIMAL", bg=bg, fg=fg, bd_color=bd_color, activebackgrund=activebackground, icon=self.copy_icon, command=self.get_hexadecimal)
        self.hexadecimal_entry_label_frame.grid(pady=(35, 25))
        
        # CREATE AN ENTRY TO DISPLAY THE CHOOSEN COLOR RGB CODE
        self.rgb_entry_label_frame = ColorEntryLabelFrame(self.second_frame, text="RGB", bg=bg, fg=fg, bd_color=bd_color, activebackgrund=activebackground, icon=self.copy_icon, command=self.get_rgb)
        self.rgb_entry_label_frame.grid()
        
        # FRAME TO STORE THE CONFIRM AND CANCEL BUTTONS
        self.buttons_frame = Frame(self.second_frame, bg=bg)
        self.buttons_frame.grid(pady=(55, 0), sticky="SEW")
        
        # CONFIRM BUTTON FRAME
        self.confirm_frame = Frame(self.buttons_frame, bg=bg, highlightbackground=bd_color, highlightcolor=bd_color, highlightthickness=1)
        self.confirm_frame.grid()
        
        # CONFIRM BUTTON
        self.confirm_button = Button(self.confirm_frame, text="CONFIRM", font=("helvetica", 10, "bold"), bg=bg, activebackground=activebackground, fg=fg, bd=0, cursor="hand2", compound="left", image=self.check_icon, command=self.get_color)
        self.confirm_button.grid(ipadx=5, ipady=3)
        
        # CANCEL BUTTON FRAME
        self.cancel_frame = Frame(self.buttons_frame, bg=bg, highlightbackground=bd_color, highlightcolor=bd_color, highlightthickness=1)
        self.cancel_frame.grid(row=0, column=1, padx=(10, 0))
        
        # CANCEL BUTTON
        self.cancel_button = Button(self.cancel_frame, text="CANCEL", font=("helvetica", 10, "bold"), bg=bg, activebackground=activebackground, fg=fg, bd=0, cursor="hand2", compound="left", image=self.cancel_icon, command=self.cancel)
        self.cancel_button.grid(ipadx=5, ipady=3)
        
        # THE LEFT FRAME THAT KEEP THE GRADIENTS SLIDER AND PICKER
        self.first_frame = Frame(self.root, bg=bg)
        self.first_frame.grid(row=0, column=0, pady=(25, 0))
        
        # GRADIENT PICKER
        self.gradient_picker = GradientPicker(self.first_frame, bg=bg, initial_color=initial_color, display=self.display, hexadecimal_entry_label_frame=self.hexadecimal_entry_label_frame.color_entry, rgb_entry_label_frame=self.rgb_entry_label_frame.color_entry)
        self.gradient_picker.grid()

        # GRADIENT SLIDER
        self.gradient_slider = GradientSlider(self.first_frame, bg=bg, thumb_border_color=bg, initial_color=initial_color, gradient_picker=self.gradient_picker)
        self.gradient_slider.grid()

        self.root.mainloop()
    
    # TO GET THE COLOR'S HEXADECIMAL INSIDE THE HEXADECIMAL ENTRY WITH THE COPY BUTTON
    def get_hexadecimal(self):
        self.hexadecimal_entry_label_frame.copy_button.configure(image=self.check_icon)
        self.root.clipboard_clear()
        self.root.clipboard_append(self.hexadecimal_entry_label_frame.color_entry.get().strip())
        time.sleep(1)
        self.hexadecimal_entry_label_frame.copy_button.configure(image=self.copy_icon)
    
    # TO GET THE COLOR'S RGB INSIDE THE RGB ENTRY WITH THE COPY BUTTON
    def get_rgb(self):
        self.rgb_entry_label_frame.copy_button.configure(image=self.check_icon)
        self.root.clipboard_clear()
        self.root.clipboard_append(self.rgb_entry_label_frame.color_entry.get().strip())
        time.sleep(1)
        self.rgb_entry_label_frame.copy_button.configure(image=self.copy_icon)
    
    # WHEN THE USER CLICK CONFIRM BUTTON
    def get_color(self):
        self.root.quit()
        return self.gradient_picker.color
    
    # WHEN THE USER CLICK CANCEL BUTTON
    def cancel(self):
        self.root.quit()
        self.gradient_picker.color = None 
