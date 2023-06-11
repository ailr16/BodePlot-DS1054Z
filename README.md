# BodePlot-DS1054Z
## Python based Bode plotter with Rigol DS1054Z and FY3224S
### Installing/Updating Required Modules
#### PyUSB
`pip install pyusb`
#### PyVisa
`pip install PyVISA`
`pip install PyVISA-py`
#### Feeltech control
`pip install feeltech`
#### Matplotlib
`pip install matplotlib`
#### NumPy
`pip install numpy`


### Version 1 usage:

[![IMAGE ALT TEXT](http://img.youtube.com/vi/WFBuwD8cPuU/0.jpg)](http://www.youtube.com/watch?v=WFBuwD8cPuU "Bode Plotter (DS1054Z-FY3224S)")

[![IMAGE ALT TEXT](http://img.youtube.com/vi/ivJM8q00k0E/0.jpg)](http://www.youtube.com/watch?v=ivJM8q00k0E "Bode Plot - Rigol DS1054Z and FY3224S")
1. Connect probes to the circuit:  
   a. CH1 from Waveform Generator to the "circuit input"  
   b. CH1 from oscilloscope to the "circuit input"  
   c. CH2 from oscilloscope to the "circuit output"  
3. Turn on Waveform generator CH1 and Oscilloscope CH2  
4. Run BodePlot.py  
`    ~/BodePlot-DS1054Z    main    python BodePlot.py `  
3. Enter requested values  
   a. Start frequency. The initial frequency of test (Lower limit)  
   b. End Frequency. The final frequency for the test (Upper limit)  
   c. Frequency steps. The amount of steps which the range will be divided  
   d. Sine Wave Max Voltage. The Peak voltage for the generated sine wave  
   e. Oscilloscope ID. VISA oscilloscope ID. It's showed in the terminal  
   

### Troubleshooting
#### Linux Users /dev/ttyUSB0 permission denied
1. Run viewInstrumentsPorts.py
```
   ~/BodePlot-DS1054Z    main    python viewInstrumentPorts.py 
------Oscilloscope ID & Generator port viewer------

List of connected instruments (search you oscilloscope):
('ASRL/dev/ttyS0::INSTR', 'ASRL/dev/ttyUSB0::INSTR', 'USB0::6833::1230::DS1ZA202711739::0::INSTR')

List of serial ports (search your generator):
/dev/ttyS0: ttyS0
```
2. Look that the instrument list contains both of our instruments, the oscilloscope (which can be identified by the model DS1Z (Rigol DS1xxxZ)) and another instrument that is the waveform generator (/dev/ttyUSB0)
3. Run
```
ls -l <GENERATOR PORT>
```
 Example:
```
     ~/BodePlot-DS1054Z    main    ls -l /dev/ttyUSB0   
crw-rw---- 1 root uucp 188, 0 Jun 10 19:54 /dev/ttyUSB0
```
 Look for the port group, listed after root, in this case, uucp
 4. Add your user to that group and reboot
 ```
 sudo usermod -a -G uucp <USER>
 reboot
 ```
