import tkinter as tk
from   tkinter.messagebox import showinfo

from   datetime import datetime
import numpy

from Instruments.Instrument import Instruments
from Instruments.Instrument import GeneratorConfig
from Instruments.Instrument import ScopeConfig

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class Colors():
    '''Class with used colors along the app

        *Background of main window,
        *Background for frames,
        *Colors for indicate error or pass in textboxes,
        **Is needed to convert the values usin _rgb_to_tkHEx()
    '''
    def _rgb_to_tkHex(rgb : int) -> str:
        '''Convert rgb value to str hex color for tkinter'''
        return "#%02x%02x%02x" % rgb
    
    MAIN_WINDOW_BG = _rgb_to_tkHex((240, 240, 240))
    FRAME_BG       = _rgb_to_tkHex((227, 227, 227))
    TEXTBOX_ERROR  = _rgb_to_tkHex((219, 118, 118))
    TEXTBOX_OK     = _rgb_to_tkHex((255, 255, 255))


class MainWindow(tk.Tk):
    '''Class for create the main window of the app
    '''
    def __init__(self) -> None:
        super().__init__()
        # configure the root window
        self.title('Bode Plotter')
        self.geometry('1324x700')
        self.config(bg=Colors.MAIN_WINDOW_BG)
        self.resizable(width=False, height=False)


class InstrumentFrame(tk.Frame):
    '''Class for the frame which allows to select the oscilloscope and generator ports

        *Scan for devices and put values into option menus,
        *Get the lists with VISA and serial devices,
        *Get the selected oscilloscope string from menu,
        *Get the selected generator string from menu
    '''

    def __init__(self, container : MainWindow) -> None:
        super().__init__(container)

        # Scan instruments
        self.instruments = Instruments()
        self.instruments.scan_devices()
        self.__options_list_visa = self.instruments.get_visa_list()
        self.__options_list_serial = self.instruments.get_serial_list()

        self.__value_inside_scope = tk.StringVar(self)          #variable to store the oscilloscope port name
        self.__value_inside_scope.set("Select Oscilloscope")

        self.__value_inside_generator = tk.StringVar(self)      #variable to store the generator port name
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

    def get_visa_list(self) -> list:
        return self.__options_list_visa
    
    def get_serial_list(self) -> list:
        return self.__options_list_serial
    
    def get_selected_scope_id(self) -> str:
        return self.__value_inside_scope.get()
    
    def get_selected_gen_port(self) -> str:
        return self.__value_inside_generator.get()


class TestFrame(tk.Frame):
    '''Class for the frame which contains analysis parameters

        *Labels and textboxes for frequency and voltage parameters,
        *Validate data for avoid exceptions
    '''
    def __init__(self, container : MainWindow) -> None:
        super().__init__(container)

        # Variables to store strings
        self.__string_start_frequency = tk.StringVar()
        self.__string_end_frequency = tk.StringVar()
        self.__string_frequency_steps = tk.StringVar()
        self.__string_max_voltage = tk.StringVar()
        self.__string_step_delay = tk.StringVar()

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

        # label step delay
        self.label_stepDelay = tk.Label(self, text='Step delay (s)')
        self.label_stepDelay.config(bg=Colors.FRAME_BG)
        self.label_stepDelay.grid(row=5, column=0, sticky="w")

        # textbox step delay
        self.__string_step_delay.trace_add("write", self.__text_changed_step_delay_Callback)
        self.textbox_stepDelay = tk.Entry(self, textvariable=self.__string_step_delay)
        self.textbox_stepDelay.config(width=24)
        self.textbox_stepDelay.insert(-1, "0.7")
        self.textbox_stepDelay.grid(row=5, column=1, sticky="w")

    def __text_changed_start_frequency_Callback(self, string, index, mode) -> None:
        '''Validate start frequency is greater than 0

            *Set textbox color to red if value is invalid or green otherwise
        '''
        new_value = self.__string_start_frequency.get()
        try:
            new_value_int = int(new_value)
            if new_value_int > 0:
                self.__start_frequency_int = new_value_int
                self.textbox_startFrequency.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_startFrequency.config(bg=Colors.TEXTBOX_ERROR)

    def __text_changed_end_frequency_Callback(self, string, index, mode) -> None:
        '''Validate end frequency is greater than start frequency
        
            *Set textbox color to red if value is invalid or green otherwise
        '''
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

    def __text_changed_frequency_steps_Callback(self, string, index, mode) -> None:
        '''Validate frequency steps is greater than 0
        
            *Set textbox color to red if value is invalid or green otherwise
        '''
        new_value = self.__string_frequency_steps.get()
        try:
            new_value_int = int(new_value)
            if new_value_int > 0:
                self.__frequency_steps_int = new_value_int
                self.textbox_frequencySteps.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_frequencySteps.config(bg=Colors.TEXTBOX_ERROR)

    def __text_changed_max_voltage_Callback(self, string, index, mode) -> None:
        '''Validate max voltage is greater than 0 and smaller than 6
        
            *Set textbox color to red if value is invalid or green otherwise
        '''
        new_value = self.__string_max_voltage.get()
        try:
            new_value_float = float(new_value)
            if new_value_float > float(0) and new_value_float < float(6):
                self.__max_voltage_float = new_value_float
                self.textbox_maxVoltage.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_maxVoltage.config(bg=Colors.TEXTBOX_ERROR)

    def __text_changed_step_delay_Callback(self, string, index, mode) -> None:
        '''Validate step delay is greater than 0
        
            *Set textbox color to red if value is invalid or green otherwise
        '''
        new_value = self.__string_step_delay.get()
        try:
            new_value_float = float(new_value)
            if new_value_float > float(0):
                self.__step_delay_float = new_value_float
                self.textbox_stepDelay.config(bg=Colors.TEXTBOX_OK)
        except:
            self.textbox_stepDelay.config(bg=Colors.TEXTBOX_ERROR)

    def get_start_frequency_value(self) -> int:
        return self.__start_frequency_int
    
    def get_end_frequency_value(self) -> int:
        return self.__end_frequency_int
    
    def get_frequency_steps_value(self) -> int:
        return self.__frequency_steps_int
    
    def get_max_voltage_value(self) -> float:
        return self.__max_voltage_float
    
    def get_step_delay_value(self) -> float:
        return self.__step_delay_float


class PlotFrame(tk.Frame):
    '''Class for the frame which contains the plots
    '''
    def __init__(self, container : MainWindow) -> None:
        super().__init__(container)

        self.config(relief="groove")
        self.config(padx=8, pady=8)
        self.config(border=1)
        self.config(bg=Colors.FRAME_BG)
        
        self.grid(row=0, column=1, rowspan=8, sticky="nsew", pady=5, padx=10)

        # label instrument
        self.label_name_frame = tk.Label(self, text='PLOTS')
        self.label_name_frame.config(bg=Colors.FRAME_BG)
        self.label_name_frame.pack(side="top", anchor="w")
        

class ActionsFrame(tk.Frame):
    '''Class for the frame which contains analysis controls

        *Run analysis,
        *Save plots,
        *Save log of measurements,
        *Select data to plot (magnitude, phase or both)
    '''
    def __init__(self,
                 container        : MainWindow,
                 instrument_frame : InstrumentFrame,
                 test_frame       : TestFrame,
                 plot_frame       : PlotFrame) -> None:
        super().__init__(container)

        self.__scope_open_flag = 0
        self.__gen_open_flag = 0
        self.__measurement_done_flag = 0

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

        # button save plots
        self.button_savePlots = tk.Button(self, text="Save plots", command=self.__savePlots)
        self.button_savePlots.config(width=45)
        self.button_savePlots.config(bg=Colors.FRAME_BG)
        self.button_savePlots.grid(row=1, column=0)
        self.button_savePlots["state"] = "disabled"

        # button save log
        self.button_saveLog = tk.Button(self, text="Save log", command=self.__saveLog)
        self.button_saveLog.config(width=45)
        self.button_saveLog.config(bg=Colors.FRAME_BG)
        self.button_saveLog.grid(row=2, column=0)
        self.button_saveLog["state"] = "disabled"

        # label log dir
        self.label_logDir = tk.Label(self, text='Save in')
        self.label_logDir.config(bg=Colors.FRAME_BG)
        self.label_logDir.grid(row=3, column=0, sticky="w")

        # textbox log dir
        self.__string_log_dir = tk.StringVar()
        self.textbox_logDir = tk.Entry(self, textvariable=self.__string_log_dir)
        self.textbox_logDir.config(width=48)
        self.textbox_logDir.insert(-1, "/home/$USER/Documents/")
        self.textbox_logDir.grid(row=4, column=0, sticky="w")
        self.textbox_logDir["state"] = "disabled"

        # checkbutton magnitude
        self.check_var_magnitude = tk.IntVar(value=1)
        self.checkbox_magnitude = tk.Checkbutton(self, text="Magnitude plot", variable=self.check_var_magnitude, command=self.__checkboxes_plot)
        self.checkbox_magnitude.config(bg=Colors.FRAME_BG)
        self.checkbox_magnitude.grid(row=6, column=0, sticky="w")

        # checkbutton phase
        self.check_var_phase = tk.IntVar(value=1)
        self.checkbox_phase = tk.Checkbutton(self, text="Phase plot", variable=self.check_var_phase, command=self.__checkboxes_plot)
        self.checkbox_phase.config(bg=Colors.FRAME_BG)
        self.checkbox_phase.grid(row=7, column=0, sticky="w")

        self.__figure = Figure(figsize=(9,6), dpi=100)
        self.__ax = self.__figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.__axP = self.__ax.twinx()
        self.__canvas = FigureCanvasTkAgg(self.__figure, master=self.__plot_frame)
        self.__canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        NavigationToolbar2Tk(self.__canvas, self.__plot_frame)

        self.__ax.plot([0,1,2], [0, 0, 0])
        self.__ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
        self.__ax.grid(which="minor", color="#EEEEEE", linestyle="dotted")
        self.__ax.minorticks_on()

    def __runAnalysisCallback(self, test_frame : TestFrame) -> None:
        '''Function called when button "Run analysis is pressed"

            *Retrieve parameters values from test_frame textboxes
            *Open oscilloscope and config with parameters
            *Open generator and config with parameters
            *Create the matpotlib figure
            *Trigger a flag indicating the analysis has been done
            *Create a string for filemane used when plots or log are saved
        '''
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

        try:
            self.__stepDelay = test_frame.get_step_delay_value()
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

        # Initial instruments config
        gen_config = GeneratorConfig(self.__maxVoltage,
                                     self.__startFrequency,
                                     self.__endFrequency,
                                     self.__frequencySteps,
                                     self.__stepDelay)
        
        scope_config = ScopeConfig(self.__startFrequency,
                                   self.__maxVoltage)

        self.__instrument_frame.instruments.initial_scope_config(scope_config)
        self.__instrument_frame.instruments.initial_generator_config(gen_config)

        self.__instrument_frame.instruments.start_analysis(gen_config)
        self.button_saveLog["state"] = "normal"
        self.button_savePlots["state"] = "normal"
        self.textbox_logDir["state"] = "normal"
        
        # Create figure with axes
        self.__ax.clear()
        self.__axP.clear()
        self.__ax.grid(which="major", color="#DCDCDC", linewidth=0.8)
        self.__ax.grid(which="minor", color="#EDEDED", linestyle="dotted")
        self.__ax.minorticks_on()
        self.__ax.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.db_array, label="Magnitude (db)")
        self.__axP.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.phaseValues, label="Phase (°)", color="orange")
        self.__ax.legend(loc="upper center", bbox_to_anchor=(0.40, 1.08))
        self.__axP.legend(loc="upper center", bbox_to_anchor=(0.60, 1.08))
        self.__ax.set_xlabel("Frequency")
        self.__ax.set_ylabel("db")
        self.__axP.set_ylabel("Degree")
        self.__axP.yaxis.set_label_position("right")
        self.__axP.yaxis.tick_right()
        self.__canvas.draw()

        
        self.__measurement_done_flag = 1

    def __saveLog(self):
        '''Function called when button "Save plots is pressed"

            *Save the log in CSV file in the indicated directory and using date and time in filename
        '''
        self.__filename_date = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")

        filename = self.__string_log_dir.get() + self.__filename_date
        numpy.savetxt(filename + ".csv", numpy.c_[self.__instrument_frame.instruments.freqValues,
                                                  self.__instrument_frame.instruments.db_array,
                                                  self.__instrument_frame.instruments.phaseValues],
                                                  delimiter=",")

    def __savePlots(self):
        '''Function called when button "Save plots is pressed"

            *Save plots as PNG in the indicated directory and using date and time in filename
        '''
        self.__filename_date = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        filename = self.__string_log_dir.get() + self.__filename_date
        self.__figure.savefig(filename + ".png")

    def __checkboxes_plot(self):
        '''Function called when any of checkboxes has changed

            *Plot magnitude, phase or both
        '''
        if self.__measurement_done_flag:
            if (self.check_var_magnitude.get() == 1) and (self.check_var_phase.get() == 1):
                self.__ax.clear()
                self.__axP.clear()
                self.__ax.grid(which="major", color="#DCDCDC", linewidth=0.8)
                self.__ax.grid(which="minor", color="#EDEDED", linestyle="dotted")
                self.__ax.minorticks_on()
                self.__ax.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.db_array, label="Magnitude (db)")
                self.__axP.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.phaseValues, label="Phase (°)", color="orange")
                self.__ax.legend(loc="upper center", bbox_to_anchor=(0.40, 1.08))
                self.__axP.legend(loc="upper center", bbox_to_anchor=(0.60, 1.08))
                self.__ax.set_xlabel("Frequency")
                self.__ax.set_ylabel("db")
                self.__axP.set_ylabel("Degree")
                self.__axP.yaxis.set_label_position("right")
                self.__axP.yaxis.tick_right()
                self.__canvas.draw()
            elif (self.check_var_magnitude.get() == 1) and (self.check_var_phase.get() == 0):
                self.__ax.clear()
                self.__axP.clear()
                self.__ax.grid(which="major", color="#DCDCDC", linewidth=0.8)
                self.__ax.grid(which="minor", color="#EDEDED", linestyle="dotted")
                self.__ax.minorticks_on()
                self.__ax.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.db_array, label="Magnitude (db)") 
                self.__ax.legend(loc="upper center", bbox_to_anchor=(0.40, 1.08))
                self.__ax.set_xlabel("Frequency")
                self.__ax.set_ylabel("db")
                self.__canvas.draw()
            elif (self.check_var_magnitude.get() == 0) and (self.check_var_phase.get() == 1):
                self.__ax.clear()
                self.__axP.clear()
                self.__ax.grid(which="major", color="#DCDCDC", linewidth=0.8)
                self.__ax.grid(which="minor", color="#EDEDED", linestyle="dotted")
                self.__ax.minorticks_on()
                self.__axP.plot(self.__instrument_frame.instruments.freqValues, self.__instrument_frame.instruments.phaseValues, label="Phase (°)", color="orange")
                self.__axP.legend(loc="upper center", bbox_to_anchor=(0.60, 1.08))
                self.__ax.set_xlabel("Frequency")
                self.__axP.set_ylabel("Degree")
                self.__axP.yaxis.set_label_position("right")
                self.__axP.yaxis.tick_right()
                self.__canvas.draw()
            else:
                pass
        else:
            pass


class BodePlotterApp():
    '''Class for all the app

        *Create the main window,
        *Create frames (test, instrument, plot and actions)
    '''
    def __init__(self, main_window:MainWindow) -> None:
        self.main_window = main_window
        inst = InstrumentFrame(main_window)
        test = TestFrame(main_window)
        plotf = PlotFrame(main_window)
        actions = ActionsFrame(main_window, inst, test, plotf)