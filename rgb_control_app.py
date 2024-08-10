from colorpicker import *
from customtkinter import *
from serial_connection import *
from microphone import *

class RGBControlApp(CTk):

    def __init__(self):
        # DEFINING MAIN WINDOW SETTINGS
        super().__init__()
        super(Tk).__init__()
        self.configure(fg_color="#111111")
        self.title("RGB control appp")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # DEFINING ARDUINO'S VARIABLES
        self.serial_connection = SerialConnection()
        self.ports = self.serial_connection.check_available_ports()["ports"]
        self.arduino = None
        
        self.color = None
        
        self.main_frame = CTkFrame(self, fg_color="#111111")
        self.main_frame.grid()
        
        # ARDUINO CONTROLS
        self.arduino_settings_frame = CTkFrame(self.main_frame, fg_color="#222222", corner_radius=20)
        self.arduino_settings_frame.grid(row=0, column=0, padx=(20, 0), pady=20, sticky="N")
        
        self.connected_arduino_label = CTkLabel(self.arduino_settings_frame, 
                                       text="ARDUINO BOARD",
                                       text_color="#FFFFFF",
                                       font=("helvetica", 20, "bold", "italic"),
                                       compound="right",
                                       image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
        self.connected_arduino_label.grid(padx=20, pady=(20, 30), sticky="W")
        
        # ARDUINO BOARD COMBOBOX
        self.arduino_board_combobox = CTkComboBox(self.arduino_settings_frame,
                                                  font=("helvetica", 20, "bold"),
                                                  dropdown_font=("helvetica", 20, "bold"),
                                                  values=[""],
                                                  width=200,
                                                  height=50,
                                                  state="readonly",
                                                  command=self.connect_arduino)
        self.arduino_board_combobox.grid(padx=20, pady=(0, 20))
        self.arduino_board_combobox.set(self.arduino_board_combobox._values[0])

        # FRAME TO STORE THE DISPLAY
        self.display_frame = CTkFrame(self.main_frame, fg_color="#222222", corner_radius=20)
        self.display_frame.grid(row=0, column=2, pady=20, sticky="NS")
        
        CTkLabel(self.display_frame, 
                 text="RESULT",
                 text_color="#FFFFFF",
                 font=("helvetica", 20, "bold", "italic")).grid(padx=(20, 0), pady=(20, 50), sticky="W")
        
        # SHOWS THE COLOR SELECTED
        self.display = Display(self.display_frame, width=180, height=180)
        self.display.grid(padx=40)
        
        # SHOWS THE RGB CODE
        icon = PhotoImage(file=r"icons\content_copy_dark.png").subsample(3)
        self.rgb_entry = ColorEntryLabelFrame(self.display_frame,
                                              bg="#222222",
                                              text="RGB",
                                              icon=icon,
                                              command=self.copy_rgb)
        self.rgb_entry.grid(pady=(30, 0))
        
        # FRAME TO STORE THE COLORPICKER
        self.color_picker_frame = CTkFrame(self.main_frame, fg_color="#222222", corner_radius=20)
        self.color_picker_frame.grid(row=0, column=1, padx=(8, 8), pady=20)
        
        CTkLabel(self.color_picker_frame, text="COLOR PICKER", text_color="#FFFFFF", font=("helvetica", 20, "bold", "italic")).grid(padx=(20, 0), pady=(20, 0), sticky="W")

        # THE COLOR PICKER
        self.picker = GradientPicker(self.color_picker_frame, bg="#222222", width=200, height=200, display=self.display, rgb_entry_label_frame=self.rgb_entry.color_entry)
        self.picker.grid(padx=10, pady=(10, 0), ipadx=30, ipady=30)
        self.slider = GradientSlider(self.color_picker_frame, bg="#222222", width=200, gradient_picker=self.picker)
        self.slider.grid(padx=10, pady=(0, 10))
        
        # FRAME TO STORE THE MICROPHONE BUTTON
        self.mic_input_frame = CTkFrame(self.main_frame, fg_color="#222222", corner_radius=20)
        self.mic_input_frame.grid(row=0, column=3, padx=(8, 20), pady=20, sticky="NS")
        
        CTkLabel(self.mic_input_frame, 
                 text="MIC INPUT",
                 text_color="#FFFFFF",
                 font=("helvetica", 20, "bold", "italic")).grid(padx=(20, 0), pady=(20, 80), sticky="W")
        
        # MICROPHONE BUTTON
        self.mic_button = CTkButton(self.mic_input_frame,
                                    text="",
                                    width=150,
                                    height=150,
                                    fg_color="#222222",
                                    hover_color="#333333",
                                    border_color="#FFFFFF",
                                    border_width=2,
                                    image=CTkImage(light_image=Image.open("./icons/mic.png"), size=(60, 60)),
                                    command=self.listen)
        self.mic_button.grid(padx=40)
        
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
        self.checking_divices()
        self.update_color()
        
        self.mainloop()
    
    # EVENT WHEN THE MICROPHONE BUTTON IS PRESSED
    def listen(self):
        if self.arduino != None:
            if self.arduino.is_open:
                microphone = Microphone(self, self.arduino, duration=2, language="pt-BR")
                self.start_time = time.time()
                self.preparing_microphone()
                audio = microphone.listen()
                self.mic_button.configure(fg_color="#222222", hover_color="#333333")
                self.update()
                text = microphone.audio_to_text(audio)

                if text != None:
                    color = None
                    if text.upper() in ["VERMELHO", "RED", "ROJO"]:
                        color = [255, 0, 0]
                    elif text.upper() in ["AMARELO", "YELLOW", "AMARILLO"]:
                        color = [255, 255, 0]
                    elif text.upper() in ["VERDE", "GREEN"]:
                        color = [0, 255, 0]
                    elif text.upper() in ["AZUL CLARO", "LIGHT BLUE"]:
                        color = [0, 255, 255]
                    elif text.upper() in ["AZUL ESCURO", "DARK BLUE", "AZUL OSCURO"]:
                        color = [0, 0, 255]
                    elif text.upper() in ["VIOLETTA", "VIOLET"]:
                        color = [125, 0, 255]
                    elif text.upper() in ["ROSA", "PINK"]:
                        color = [255, 0, 255]
                    elif text.upper() in["BRANCO", "WHITE", "BLANCO"]:
                        color = [255, 255, 255]
                    elif text.upper() in["PRETO", "BLACK", "NEGRO"]:
                        color = [0, 0, 0]

                    if color != None:
                        self.slider.get_position(self.picker.convert_color_to_dict(color))
                        self.picker.initial_color = self.picker.convert_color_to_dict(color)
                        self.picker.color = self.picker.convert_color_to_dict(color)
                        self.picker.draw_gradient(self.slider.color)
                        self.picker.color = self.picker.convert_color_to_dict(color)
                   
                        self.rgb_entry.color_entry.delete(0, "end")
                        self.rgb_entry.color_entry.insert(0, str(color).replace("[", "").replace("]", ""))
                        self.update()
    
    # SET THE COLOR BUTTON TO RED WHEN THE USER CAN SPEAK THE COLOR
    def preparing_microphone(self):
        
        if (time.time() - self.start_time > 1):
            self.mic_button.configure(fg_color="#FF0000", hover_color="#FF0000")
            return
        else:
            self.after(11, self.preparing_microphone)
            
    # WHEN THE USER CLICK THE COPY BUTTON
    def copy_rgb(self):
        self.clipboard_clear()
        self.clipboard_append(self.rgb_entry.color_entry.get().strip())
    
    # UPDATE THE COLOR OF THE RGB LED WHEN THE SELECTED COLOR CHANGES
    def update_color(self):
        
        if self.picker.color != self.color:
            self.color = self.picker.color
            self.send_to_serial()
        
        self.after(10, self.update_color)
    
    # SEND COLOR TO SERIAL
    def send_to_serial(self):
        if self.arduino != None:
            if self.arduino.is_open:
                self.arduino.write(f"CHANGE COLOR:{self.color["rgb"][0]}:{self.color["rgb"][1]}:{self.color["rgb"][2]}:".encode())
        
    # TO STABILISH SERIAL CONNECTION
    def connect_arduino(self, event) -> None:
        if self.arduino != None:
            if self.arduino.is_open:
                self.serial_connection.end(self.arduino)
        
        self.arduino = self.serial_connection.start(self.arduino_board_combobox.get(), 250000)
        
        time.sleep(2)
        
        if self.arduino != None:
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb.png")))
        else:
            self.arduino_board_combobox.set(value=[])
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
            self.alert_window("ARDUINO CONNECTION FAILED")

        
    # TO CHECK IF THERE ARE ARDUINOS CONNECTED TO THE USB PORTS ON USER'S COMPUTER
    def checking_divices(self) -> None:               
        
        # GETTING THE PORT
        self.ports = self.serial_connection.check_available_ports()["ports"]
        # PUT THE PORTS INTO COMBOBOX VALUES
        self.arduino_board_combobox.configure(values=self.ports)
        
        if self.arduino_board_combobox.get() not in self.ports:
            self.arduino_board_combobox.set(value=[])
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
            self.arduino = None

        # CHECKS THE USB PORTS EACH 2 SECONDS
        self.after(1000, self.checking_divices)
    
    # TO STOP THE SONG LOOP WHEN THE APP WINDOW CLOSE
    def cancel(self) -> None:
        if self.arduino != None:
            if self.arduino.is_open:
                self.serial_connection.end(self.arduino)

        self.quit()
    
    # SHOW AN ALERT WINDOW WHEN RAISES EN ERROR
    def alert_window(self, message:str) -> None:
        if self.window != None:
            if self.window.winfo_ismapped:
                self.window.destroy()
            self.window = None
            
        self.window = CTkToplevel(self)
        self.window.attributes('-topmost', True)
        self.window.geometry("+200+200")
        self.window.resizable(False, False)
        self.window.title("Alert")
        
        self.window_frame = CTkFrame(self.window,
                                     fg_color="#111111",
                                     corner_radius=0)
        self.window_frame.grid()
        
        CTkLabel(self.window_frame,
                 text=message,
                 text_color="#FFFFFF").grid(padx=30, pady=(20, 5))
        
        CTkButton(self.window_frame,
                  text="OK",
                  fg_color="#008833",
                  hover_color="#006611",
                  command=lambda: self.window.destroy()).grid(padx=30, pady=(5, 20), columnspan=2, sticky="EW")
        
        
if __name__ == "__main__":
    RGBControlApp()