import pyvisa
import serial.tools.list_ports

class Instruments:
    def __init__(self) -> None:
        self.__visa_list = []
        self.__serial_list = []
        pass

    def scan_devices(self):
        self.resources = pyvisa.ResourceManager()
        for visa_instrument in self.resources.list_resources():
            self.__visa_list.append(visa_instrument)
        
        self.ports = serial.tools.list_ports.comports()
        for port in sorted(self.ports):
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