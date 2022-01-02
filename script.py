import pyvisa
import serial.tools.list_ports

print('------Oscilloscope ID & Generator port viewer------\n')
rm = pyvisa.ResourceManager()					#PyVISA Resource Manager
print("List of connected instruments (search you oscilloscope):")
print(rm.list_resources())					#Show the list of detected instruments

print('\nList of serial ports (search your generator):')
ports = serial.tools.list_ports.comports()			#Print serial ports
for port, desc, hwid in sorted(ports):
        print("{}: {}".format(port, desc))
