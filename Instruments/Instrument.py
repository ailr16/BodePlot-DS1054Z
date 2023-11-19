import pyvisa
import serial.tools.list_ports
import feeltech
import numpy
from   time import sleep

class GeneratorConfig:
    """Class for handling the generator configuration

       *Sets frequency start, end, step and step delay; max voltage
    """

    def __init__(self,
                 max_voltage     : float,
                 start_frequency : int,
                 end_frequency   : int,
                 step_freq       : int,
                 step_delay      : float) -> None:
        self.__max_voltage = max_voltage
        self.__start_frequency = start_frequency
        self.__end_frequency = end_frequency
        self.__step_frequency = step_freq
        self.__step_delay = step_delay

    def set_max_voltage(self, max_voltage : float) -> None:
        self.__max_voltage = max_voltage

    def set_start_frequency(self, start_frequency : int) -> None:
        self.__start_frequency = start_frequency

    def set_end_frequency(self, end_frequency : int) -> None:
        self.__end_frequency = end_frequency

    def set_step_frequency(self, step_frequency : int) -> None:
        self.__step_frequency = step_frequency

    def set_step_delay(self, step_delay : float) -> None:
        self.__step_delay = step_delay

    def get_max_voltage(self) -> float:
        return self.__max_voltage
    
    def get_start_frequency(self) -> int:
        return self.__start_frequency
    
    def get_end_frequency(self) -> int:
        return self.__end_frequency
    
    def get_step_frequency(self) -> int:
        return self.__step_frequency
    
    def get_step_delay(self) -> float:
        return self.__step_delay


class ScopeConfig:
    """Class for handling the oscilloscope configuration

       *Sets max voltage and frequency (used for compute the window)
    """
    def __init__(self,
                 frequency  : float,
                 maxVoltage : float) -> None:
        self.__frequency = frequency
        self.__maxVoltage = maxVoltage

    def set_frequency(self, frequency:float) -> None:
        self.__frequency = frequency

    def set_max_voltage(self, maxVoltage:float) -> None:
        self.__maxVoltage = maxVoltage

    def get_frequency(self) -> float:
        return self.__frequency
    
    def get_max_voltage(self) -> float:
        return self.__maxVoltage
    

class Instruments:
    """Class for handling both instruments

       *Scan VISA and serial devices and return results,
       *Start communication with specified oscilloscope,
       *Start communication with specified generator,
       *Set the oscilloscope to an initial configuration before start,
       *Set the generator to an initial configuration before start,
       *Perform the analysis and store voltage, frequency and phase values
    """

    def __init__(self) -> None:
        """Init lists for store available VISA and serial devices"""
        self.__visa_list = []
        self.__serial_list = []

    def scan_devices(self):
        """Scan for VISA and serial devices"""
        self.__resources = pyvisa.ResourceManager()
        for visa_instrument in self.__resources.list_resources():
            self.__visa_list.append(visa_instrument)
        
        self.ports = serial.tools.list_ports.comports()
        for port, desc, hwid in self.ports:
            # Store only the port name
            self.__serial_list.append(port)
    
    def get_visa_list(self) -> list:
        return self.__visa_list
    
    def get_serial_list(self) -> list:
        return self.__serial_list

    def open_scope(self, scope_id : str) -> bool:
        """Init communication with specified oscilloscope and return status"""
        return_status = False

        try:
            self.__scope = self.__resources.open_resource(scope_id)
            return_status = True
        except:
            pass
        
        return return_status
    
    def open_generator(self, gen_port : str) -> bool:
        """Init communication with specified generator and return status"""
        return_status = False

        try:
            self.__generator = feeltech.FeelTech(gen_port)
            self.__gen_ch1 = feeltech.Channel(1, self.__generator)
            return_status = True
        except:
            pass

        return return_status
    
    def initial_scope_config(self, config : ScopeConfig) -> None:
        """Set the initial configuration for oscilloscope

           *Measurements (vmax on CH1 and CH2, phase),
           *Adjust window (timebase and vertical scale to fit first measurement in screen),
           *Set trigger to Auto, sync with CH1 and move a little above zero
        """
        self.__scope.write("MEASure:CLEar ALL")
        self.__scope.write("MEASure:ITEM VMAX,CHANnel1")
        self.__scope.write("MEASure:ITEM VMAX,CHANnel2")
        self.__scope.write("MEASure:ITEM RPHase, CHANnel1, CHANnel2")
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

    def initial_generator_config(self, config : GeneratorConfig) -> None:
        """Set the initial configuration for generator

           *Sine wave in CH1 with specified max voltage and first frequency step
        """
        self.__gen_ch1.waveform(feeltech.SINE)
        self.__gen_ch1.amplitude(config.get_max_voltage())
        self.__gen_ch1.frequency(config.get_start_frequency())

    def start_analysis(self, config : GeneratorConfig) -> None:
        """Perform the analysis for every frequency step

           *Store the max voltage (CH1 and CH2),
           *Store the phase measurement,
           *Store the frequency step value,
           *Set a new vertical scale according to the last voltage measured,
           *Set a new timebase according to the last frequency step,
           *Before the function ends, compute db based in CH1 and CH2 measurements
        """
        sleep(2*config.get_step_delay())

        self.ch1Vmax = numpy.zeros(config.get_step_frequency() + 1)
        self.ch2Vmax = numpy.zeros(config.get_step_frequency() + 1)
        self.freqValues = numpy.zeros(config.get_step_frequency() + 1)
        self.phaseValues = numpy.zeros(config.get_step_frequency() + 1)

        freqInc = ((config.get_end_frequency() - config.get_start_frequency()) / config.get_step_frequency())
        freq = config.get_start_frequency()

        i = 0
        while i <= config.get_step_frequency():
            self.__gen_ch1.frequency(freq)
            self.__scope.write("TIMebase:MAIN:SCAle "+ str(1 / (3 * freq)))
            sleep(config.get_step_delay())
            
            actual_ch1 = float(self.__scope.query("MEASure:ITEM? VMAX,CHANnel1"))
            actual_ch2 = float(self.__scope.query("MEASure:ITEM? VMAX,CHANnel2"))
            actual_phase = float(self.__scope.query("MEASure:STATistic:ITEM? MINimum,RPHase"))

            self.ch1Vmax[i] = actual_ch1
            self.ch2Vmax[i] = actual_ch2

            if actual_phase >= -180.0 and actual_phase <= 180.0:
                self.phaseValues[i] = actual_phase
            self.freqValues[i] = freq

            self.__scope.write("CHANnel1:SCALe " + str(actual_ch1/2))
            self.__scope.write("CHANnel2:SCALe " + str(actual_ch2/2))

            freq = freq + freqInc
            i = i + 1

        self.db_array = self._db_compute(self.ch1Vmax, self.ch2Vmax, config.get_step_frequency())

    def _db_compute(self,
                    ch1_voltages : numpy.ndarray,
                    ch2_voltages : numpy.ndarray,
                    freqSteps    : int) -> numpy.ndarray:
        """Compute db array using two arrays of measurements
        
           *CH1 (first parameter) is the reference
        """
        db = numpy.zeros(freqSteps + 1)

        db = (ch2_voltages / ch1_voltages)
        db = 20*numpy.log10(db)

        return db
    
    def __del__(self):
        """Destructor

           *Guarantee to close oscilloscope and generator
        """
        try:
            self.__scope.close()
            self.__generator.close()
        except:
            pass

