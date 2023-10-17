import  tkinter as tk
from tkinter.messagebox import showinfo


class Colors():
    def _rgb_to_tkHex(rgb):
        return "#%02x%02x%02x" % rgb
    
    MAIN_WINDOW_BG  = _rgb_to_tkHex((242, 242, 242))
    FRAME_BG        = _rgb_to_tkHex((227, 227, 227))


class InstrumentFrame(tk.Frame):
    options_list = ["OSCILLOSCOPE", "GENERATOR"]

    def __init__(self, container):
        super().__init__(container)

        value_inside_scope = tk.StringVar(self)
        value_inside_scope.set("Select an Option")

        value_inside_generator = tk.StringVar(self)
        value_inside_generator.set("Select an Option")

        self.config(relief="groove")
        self.config(padx=8, pady=8)
        self.config(border=1)
        self.config(bg=Colors.FRAME_BG)
        
        self.grid(row=0, column=0, sticky="nsew")

        # label instrument
        self.label_name_frame = tk.Label(self, text='INSTRUMENT')
        self.label_name_frame.config(bg=Colors.FRAME_BG)
        self.label_name_frame.pack(side="top", anchor="w")

        # optionmenu scope ID
        self.optionmenu_scopeID = tk.OptionMenu(self, value_inside_scope, *self.options_list)
        self.optionmenu_scopeID.config(width=43, height=1)
        self.optionmenu_scopeID.pack()

        # optionmenu generator port
        self.optionmenu_generatorPort = tk.OptionMenu(self, value_inside_generator, *self.options_list)
        self.optionmenu_generatorPort.config(width=43, height=1)
        self.optionmenu_generatorPort.pack()

        # scan devices button
        self.button = tk.Button(self, text='Scan devices')
        self.button['command'] = self.scan_button_clicked
        self.button.pack()

        # show the frame on the container
        #self.pack(**options)

    def scan_button_clicked(self):
        showinfo(title='Information',
                 message='Hello, Tkinter!')
        
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Bode Plotter')
        self.geometry('1400x900')
        self.config(bg=Colors.MAIN_WINDOW_BG)
