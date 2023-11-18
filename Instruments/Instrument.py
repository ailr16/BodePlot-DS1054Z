import pyvisa
import serial.tools.list_ports
import feeltech
from time import sleep
import numpy

class GeneratorConfig:
    def __init__(self, max_voltage:float, start_frequency:int, end_frequency:int, step_freq:int, step_delay:float) -> None:
        self.__max_voltage = max_voltage
        self.__start_frequency = start_frequency
        self.__end_frequency = end_frequency
        self.__step_frequency = step_freq
        self.__step_delay = step_delay

    def set_max_voltage(self, max_voltage:float):
        self.__max_voltage = max_voltage

    def set_start_frequency(self, start_frequency:int):
        self.__start_frequency = start_frequency

    def set_end_frequency(self, end_frequency:int):
        self.__end_frequency = end_frequency

    def set_step_frequency(self, step_frequency:int):
        self.__step_frequency = step_frequency

    def set_step_delay(self, step_delay:float):
        self.__step_delay = step_delay

    def get_max_voltage(self) -> float:
        return self.__max_voltage
    
    def get_start_frequency(self) -> int:
        return self.__start_frequency
    
    def get_end_frequency(self):
        return self.__end_frequency
    
    def get_step_frequency(self):
        return self.__step_frequency
    
    def get_step_delay(self):
        return self.__step_delay


class ScopeConfig:
    def __init__(self, frequency:float, maxVoltage:float) -> None:
        self.__frequency = frequency
        self.__maxVoltage = maxVoltage

    def set_frequency(self, frequency:float):
        self.__frequency = frequency

    def set_max_voltage(self, maxVoltage:float):
        self.__maxVoltage = maxVoltage

    def get_frequency(self):
        return self.__frequency
    
    def get_max_voltage(self):
        return self.__maxVoltage
    

class Instruments:
    def __init__(self) -> None:
        self.__visa_list = []
        self.__serial_list = []
        pass

    def scan_devices(self):
        self.__resources = pyvisa.ResourceManager()
        for visa_instrument in self.__resources.list_resources():
            self.__visa_list.append(visa_instrument)
        
        self.ports = serial.tools.list_ports.comports()
        for port, desc, hwid in self.ports:
            self.__serial_list.append(port)
    
    def get_visa_list(self):
        return self.__visa_list
    
    def get_serial_list(self):
        return self.__serial_list

    def _print_terminal_list(self):
        for inst in self.__visa_list:
            print(inst)

        for port in self.__serial_list:
            print(port)

    def open_scope(self, scope_id:str):
        return_status = False

        try:
            self.__scope = self.__resources.open_resource(scope_id)
            return_status = True
        except:
            pass
        
        return return_status
    
    def open_generator(self, gen_port:str):
        return_status = False

        try:
            self.__generator = feeltech.FeelTech(gen_port)
            self.__gen_ch1 = feeltech.Channel(1, self.__generator)
            return_status = True
        except:
            pass

        return return_status
    
    def initial_scope_config(self, config:ScopeConfig):
        self.__scope.write("MEASure:CLEar ALL")				        #Clear all measurement items
        self.__scope.write("MEASure:ITEM VMAX,CHANnel1")			#Create the VMax measurement item for CH1
        self.__scope.write("MEASure:ITEM VMAX,CHANnel2")			#Create the VMax measurement item for CH2
        self.__scope.write("MEASure:ITEM RPHase, CHANnel1, CHANnel2")			#Create the VMax measurement item for CH2
        self.__scope.write("TIMebase:MAIN:SCAle " + str(1/(3*config.get_frequency())))
        self.__scope.write("TRIGger:SWEep AUTO")
        self.__scope.write("TRIGger:EDGe:SOURce CHANnel1")
        self.__scope.write("TRIGger:EDGe:LEVel 0.1")

        if config.get_max_voltage() <= 3.5:						#Set vertical scale of oscilloscope
            self.__scope.write("CHANnel1:SCALe 1")
            self.__scope.write("CHANnel2:SCALe 1")

        elif config.get_max_voltage() > 3.5 and config.get_max_voltage() <= 7:
            self.__scope.write("CHANnel1:SCALe 2")
            self.__scope.write("CHANnel2:SCALe 2")

        elif config.get_max_voltage() > 7:
            self.__scope.write("CHANnel1:SCALe 5")
            self.__scope.write("CHANnel2:SCALe 5")

    def initial_generator_config(self, config:GeneratorConfig):
        self.__gen_ch1.waveform(feeltech.SINE)					    #CH1 will generate a sine wave
        self.__gen_ch1.amplitude(config.get_max_voltage())			#Set CH1 peak to peak voltage
        self.__gen_ch1.frequency(config.get_start_frequency())		#Set CH1 frequency

    def start_analysis(self, config:GeneratorConfig):
        sleep(2*config.get_step_delay())

        self.ch1Vmax = numpy.zeros(config.get_step_frequency() + 1)
        self.ch2Vmax = numpy.zeros(config.get_step_frequency() + 1)
        self.freqValues = numpy.zeros(config.get_step_frequency() + 1)
        self.phaseValues = numpy.zeros(config.get_step_frequency() + 1)

        freqInc = ((config.get_end_frequency()-config.get_start_frequency())/config.get_step_frequency())
        freq = config.get_start_frequency()
        i = 0
        while i <= config.get_step_frequency():
            self.__gen_ch1.frequency(freq)
            self.__scope.write("TIMebase:MAIN:SCAle "+ str(1/(3*freq)))
            sleep(config.get_step_delay())
            
            actual_ch1 = float(self.__scope.query("MEASure:ITEM? VMAX,CHANnel1"))
            actual_ch2 = float(self.__scope.query("MEASure:ITEM? VMAX,CHANnel2"))
            actual_phase = float(self.__scope.query("MEASure:STATistic:ITEM? AVERages,RPHase"))

            self.ch1Vmax[i] = actual_ch1
            self.ch2Vmax[i] = actual_ch2
            if actual_phase > -180.0 and actual_phase < 180.0:
                self.phaseValues[i] = actual_phase
            self.freqValues[i] = freq

            self.__scope.write("CHANnel1:SCALe " + str(actual_ch1/2))
            self.__scope.write("CHANnel2:SCALe " + str(actual_ch2/2))

            freq = freq + freqInc
            i = i + 1

        self.db_array = self._db_compute(self.ch1Vmax, self.ch2Vmax, config.get_step_frequency())


    def _db_compute(self, ch1V:numpy.ndarray, ch2:numpy.ndarray, freqSteps:int):
        db = numpy.zeros(freqSteps + 1)

        db = (ch2/ch1V)
        db = 20*numpy.log10(db)

        return db

    def test_generator(self, freq):
        self.__gen_ch1.frequency(freq)

    def test_scope(self):
        self.__scope.write("MEASure:ITEM VMAX,CHANnel1")
        self.__scope.write("MEASure:ITEM VMAX,CHANnel2")
    
    def __del__(self):
        try:
            self.__scope.close()
            self.__generator.close()
        except:
            pass

