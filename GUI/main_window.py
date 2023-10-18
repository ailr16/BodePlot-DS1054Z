import  tkinter as tk
from tkinter.messagebox import showinfo
from Instruments.Instrument import Instruments
from Instruments.Instrument import GeneratorConfig
from Instruments.Instrument import ScopeConfig
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Colors():
    def _rgb_to_tkHex(rgb):
        return "#%02x%02x%02x" % rgb
    
    MAIN_WINDOW_BG  = _rgb_to_tkHex((240, 240, 240))
    FRAME_BG        = _rgb_to_tkHex((227, 227, 227))
    TEXTBOX_ERROR   = _rgb_to_tkHex((219, 118, 118))
    TEXTBOX_OK      = _rgb_to_tkHex((255, 255, 255))


class InstrumentFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # scan instruments
        self.instruments = Instruments()
        self.instruments.scan_devices()
        self.__options_list_visa = self.instruments.get_visa_list()
        self.__options_list_serial = self.instruments.get_serial_list()

        self.__value_inside_scope = tk.StringVar(self)
        self.__value_inside_scope.set("Select Oscilloscope")

        self.__value_inside_generator = tk.StringVar(self)
        self.__value_inside_generator.set("Select Generator")

        self.config(relief="groove")
        self.config(padx=8, pady=8)
        self.config(border=1)
        self.config(bg=Colors.FRAME_BG)
        
        self.grid(row=0, column=0, sticky="nsew", pady=5, padx=10)

        # label instrument
        self.label_name_frame = tk.Label(self, text='INSTRUMENT')
        self.label_name_frame.config(bg=Colors.FRAME_BG)
        self.label_name_frame.pack(side="top", anchor="w")

        # optionmenu scope ID
        self.optionmenu_scopeID = tk.OptionMenu(self, self.__value_inside_scope, *self.__options_list_visa)
        self.optionmenu_scopeID.config(width=43, height=1)
        self.optionmenu_scopeID.pack()

        # optionmenu generator port
        self.optionmenu_generatorPort = tk.OptionMenu(self, self.__value_inside_generator, *self.__options_list_serial)
        self.optionmenu_generatorPort.config(width=43, height=1)
        self.optionmenu_generatorPort.pack()

        # show the frame on the container
        #self.pack(**options)

    def get_visa_list(self):
        return self.__options_list_visa
    
    def get_serial_list(self):
        return self.__options_list_serial
    
    def get_selected_scope_id(self):
        return self.__value_inside_scope.get()
    
    def get_selected_gen_port(self):
        return self.__value_inside_generator.get()


class TestFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__string_start_frequency = tk.StringVar()
        self.__string_end_frequency = tk.StringVar()
        self.__string_frequency_steps = tk.StringVar()
        self.__string_max_voltage = tk.StringVar()

        self.config(relief="groove")
        self.config(padx=8, pady=8)
        self.config(border=1)
        self.config(bg=Colors.FRAME_BG)
        
        self.grid(row=1, column=0, sticky="nsew", pady=5, padx=10)

        # label instrument
        self.label_name_frame = tk.Label(self, text='TEST')
        self.label_name_frame.config(bg=Colors.FRAME_BG)
        self.label_name_frame.grid(row=0, column=0, sticky="w")

        # label start frequency
        self.label_startFrequency = tk.Label(self, text='Start Frequency (Hz)')
        self.label_startFrequency.config(bg=Colors.FRAME_BG)
        self.label_startFrequency.grid(row=1, column=0, sticky="w")

        # textbox start frequency
        self.__string_start_frequency.trace_add("write", self.__text_changed_start_frequency_Callback)
        self.textbox_startFrequency = tk.Entry(self, textvariable=self.__string_start_frequency)
        self.textbox_startFrequency.config(width=24)
        self.textbox_startFrequency.insert(-1, "100")
        self.textbox_startFrequency.grid(row=1, column=1, sticky="w")

        # label end frequency
        self.label_endFrequency = tk.Label(self, text='End Frequency (Hz)')
        self.label_endFrequency.config(bg=Colors.FRAME_BG)
        self.label_endFrequency.grid(row=2, column=0, sticky="w")

        # textbox end frequency
        self.__string_end_frequency.trace_add("write", self.__text_changed_end_frequency_Callback)
        self.textbox_endFrequency = tk.Entry(self, textvariable=self.__string_end_frequency)
        self.textbox_endFrequency.config(width=24)
        self.textbox_endFrequency.insert(-1, "10000")
        self.textbox_endFrequency.grid(row=2, column=1, sticky="w")

        # label frequency steps
        self.label_frequencySteps = tk.Label(self, text='Frequency Steps')
        self.label_frequencySteps.config(bg=Colors.FRAME_BG)
        self.label_frequencySteps.grid(row=3, column=0, sticky="w")

        # textbox frequency steps
        self.__string_frequency_steps.trace_add("write", self.__text_changed_frequency_steps_Callback)
        self.textbox_frequencySteps = tk.Entry(self, textvariable=self.__string_frequency_steps)
        self.textbox_frequencySteps.config(width=24)
        self.textbox_frequencySteps.insert(-1, "10")
        self.textbox_frequencySteps.grid(row=3, column=1, sticky="w")

        # label max voltage
        self.label_maxVoltage = tk.Label(self, text='Max Voltage (V)')
        self.label_maxVoltage.config(bg=Colors.FRAME_BG)
        self.label_maxVoltage.grid(row=4, column=0, sticky="w")

        # textbox max voltage
        self.__string_max_voltage.trace_add("write", self.__text_changed_max_voltage_Callback)
        self.textbox_maxVoltage = tk.Entry(self, textvariable=self.__string_max_voltage)
        self.textbox_maxVoltage.config(width=24)
        self.textbox_maxVoltage.insert(-1, "2")
        self.textbox_maxVoltage.grid(row=4, column=1, sticky="w")

    def __text_changed_start_frequency_Callback(self, string, index, mode):
        new_value = self.__string_start_frequency.get()
        try:
            new_value_int = int(new_value)
            if new_value_int > 0:
                self.__start_frequency_int = new_value_int
                self.textbox_startFrequency.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_startFrequency.config(bg=Colors.TEXTBOX_ERROR)

    def __text_changed_end_frequency_Callback(self, string, index, mode):
        new_value = self.__string_end_frequency.get()
        try:
            new_value_int = int(new_value)
            if new_value_int > self.__start_frequency_int:
                self.__end_frequency_int = new_value_int
                self.textbox_endFrequency.config(bg=Colors.TEXTBOX_OK)
            else:
                self.textbox_endFrequency.config(bg=Colors.TEXTBOX_ERROR)
        except:
            self.textbox_endFrequency.config(bg=Colors.TEXTBOX_ERROR)

    def __text_changed_frequency_steps_Callback(self, string, index, mode):
        new_value = self.__string_frequency_steps.get()
        try:
            new_value_int = int(new_value)
            if new_value_int > 0:
                self.__frequency_steps_int = new_value_int
                self.textbox_frequencySteps.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_frequencySteps.config(bg=Colors.TEXTBOX_ERROR)

    def __text_changed_max_voltage_Callback(self, string, index, mode):
        new_value = self.__string_max_voltage.get()
        try:
            new_value_float = float(new_value)
            if new_value_float > float(0) and new_value_float < float(6):
                self.__max_voltage_float = new_value_float
                self.textbox_maxVoltage.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_maxVoltage.config(bg=Colors.TEXTBOX_ERROR)

    def get_start_frequency_value(self):
        return self.__start_frequency_int
    
    def get_end_frequency_value(self):
        return self.__end_frequency_int
    
    def get_frequency_steps_value(self):
        return self.__frequency_steps_int
    
    def get_max_voltage_value(self):
        return self.__max_voltage_float


class PlotFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.config(relief="groove")
        self.config(padx=8, pady=8)
        self.config(border=1)
        self.config(bg=Colors.FRAME_BG)
        
        self.grid(row=0, column=1, rowspan=5, sticky="nsew", pady=5, padx=10)

        # label instrument
        self.label_name_frame = tk.Label(self, text='PLOTS')
        self.label_name_frame.config(bg=Colors.FRAME_BG)
        self.label_name_frame.pack(side="top", anchor="w")


class ActionsFrame(tk.Frame):
    def __init__(self, container, instrument_frame:InstrumentFrame, test_frame:TestFrame, plot_frame:PlotFrame):
        super().__init__(container)

        self.__scope_open_flag = 0
        self.__gen_open_flag = 0

        self.__list_visa = instrument_frame.get_visa_list()
        self.__list_serial = instrument_frame.get_serial_list()
        self.__instrument_frame = instrument_frame
        self.__plot_frame = plot_frame

        self.config(relief="groove")
        self.config(padx=8, pady=8)
        self.config(border=1)
        self.config(bg=Colors.FRAME_BG)

        self.__startFrequency = 100
        self.__endFrequency = 10000
        self.__frequencySteps = 10
        self.__maxVoltage = 2
        
        self.grid(row=2, column=0, sticky="nsew", pady=5, padx=10)

        # button run analysis
        self.button_runAnalysis = tk.Button(self, text="Run Analysis", command=lambda:self.__runAnalysisCallback(test_frame))
        self.button_runAnalysis.config(width=45)
        self.button_runAnalysis.config(bg=Colors.FRAME_BG)
        self.button_runAnalysis.grid(row=0, column=0)

        # button save log
        self.button_saveLog = tk.Button(self, text="Save log", command=self.__saveLog)
        self.button_saveLog.config(width=45)
        self.button_saveLog.config(bg=Colors.FRAME_BG)
        self.button_saveLog.grid(row=1, column=0)

        # button save plots
        self.button_savePlots = tk.Button(self, text="Save plots", command=self.__savePlots)
        self.button_savePlots.config(width=45)
        self.button_savePlots.config(bg=Colors.FRAME_BG)
        self.button_savePlots.grid(row=2, column=0)

    def __runAnalysisCallback(self, test_frame:TestFrame):
        try:
            self.__startFrequency = test_frame.get_start_frequency_value()
        except:
            pass

        try:
            self.__endFrequency = test_frame.get_end_frequency_value()
        except:
            pass

        try:
            self.__frequencySteps = test_frame.get_frequency_steps_value()
        except:
            pass

        try:
            self.__maxVoltage = test_frame.get_max_voltage_value()
        except:
            pass

        self.scope_id = self.__instrument_frame.get_selected_scope_id()
        self.gen_port = self.__instrument_frame.get_selected_gen_port()

        if self.__scope_open_flag == 0:
            self.__instrument_frame.instruments.open_scope(self.scope_id)
            self.__scope_open_flag = 1

        if self.__gen_open_flag == 0:
            self.__instrument_frame.instruments.open_generator(self.gen_port)
            self.__gen_open_flag = 1

        gen_config = GeneratorConfig(self.__maxVoltage,
                                     self.__startFrequency,
                                     self.__endFrequency,
                                     self.__frequencySteps,
                                     0.7,)
        scope_config = ScopeConfig(self.__startFrequency, self.__maxVoltage)

        self.__instrument_frame.instruments.initial_scope_config(scope_config)
        self.__instrument_frame.instruments.initial_generator_config(gen_config)

        self.__instrument_frame.instruments.start_analysis(gen_config)
        
        figure = Figure(figsize=(9,3), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, master=self.__plot_frame)

        NavigationToolbar2Tk(figure_canvas, self.__plot_frame)
        
        axes = figure.add_subplot()
        axes.grid(True)
        axes.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.db_array)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def __saveLog(self):
        print(self.__list_visa[2])
        print(self.__list_serial[1])

    def __savePlots(self):
        print(self.__list_visa[2])
        print(self.__list_serial[1])


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Bode Plotter')
        self.geometry('1400x700')
        self.config(bg=Colors.MAIN_WINDOW_BG)
        

class BodePlotterApp():
    def __init__(self, main_window:MainWindow) -> None:
        self.main_window = main_window
        inst = InstrumentFrame(main_window)
        test = TestFrame(main_window)
        plotf = PlotFrame(main_window)
        actions = ActionsFrame(main_window, inst, test, plotf)