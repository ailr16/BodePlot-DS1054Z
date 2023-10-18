import pyvisa
import serial.tools.list_ports
import feeltech

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
        print("CAlled scope open")

        try:
            self.__scope = self.__resources.open_resource(scope_id)
            return_status = True
        except:
            pass
        
        return return_status
    
    def open_generator(self, gen_port:str):
        return_status = False
        print("CAlled gen open")
        try:
            self.__generator = feeltech.FeelTech(gen_port)
            self.__gen_ch1 = feeltech.Channel(1, self.__generator)
            return_status = True
        except:
            pass

        return return_status
    
    def test_generator(self, freq):
        self.__gen_ch1.frequency(freq)
    
    def __del__(self):
        print("Closing")
        try:
            self.__scope.close()
            self.__generator.close()
        except:
            pass
