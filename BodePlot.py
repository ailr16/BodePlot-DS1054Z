from cmath import phase
import pyvisa
import feeltech
import time
import numpy
import matplotlib.pyplot as plt
import math

fichero = open('config.txt')
########################
time_delay = 0.8 #Adjust the time delay between frequency increments (in seconds)
########################

freq_start = float(fichero.readline().split(',')[1])		#Read the start frequency
freq_end = float(fichero.readline().split(',')[1])		#Read the end frequency
if freq_start < 0 or freq_end < 0:
	print('ERROR. Frequency must be possitive')
	print('Please press Enter to exit :-(')
	input()
	exit()
if freq_start > freq_end:
	print('ERROR. Start Frequency must be less than End Frequency')
	print('Please press Enter to exit:-(')
	input()
	exit()

freq_steps = int(fichero.readline().split(',')[1])			#Read the frequency steps
if freq_steps <= 0:
	print('ERROR. Frequency steps must be greater than zero')
	print('Please press Enter to exit :-(')
	input()
	exit()
wave_v_max = float(fichero.readline().split(',')[1])		#Read the max voltage of sine wave
if wave_v_max <= 0:
	print('ERROR. Max Voltage must be greater than zero')
	print('Please press Enter to exit :-(')
	input()
	exit()

freq_inc = ((freq_end-freq_start)/freq_steps)			#Compute the frequency increments in function of steps, start and end frequencies

rm = pyvisa.ResourceManager()						#PyVISA Resource Manager
instrument = fichero.readline().split(',')[1]
instrument = instrument[:-1]
scope = rm.open_resource(instrument)				#Identify oscilloscope with "scope"
scope.write("MEASure:CLEar ALL")					#Clear all measurement items
scope.write("MEASure:ITEM VMAX,CHANnel1")			#Create the VMax measurement item for CH1
scope.write("MEASure:ITEM VMAX,CHANnel2")			#Create the VMax measurement item for CH2

port_gen = fichero.readline().split(',')[1]
port_gen = port_gen[:-1]

scale = fichero.readline().split(',')[1]

print("-"*32)
print("Starting...")
print("Start Frequency: " + str(freq_start))
print("End Frequency: " + str(freq_end))
print("Frequency Step: " + str(freq_steps))
print("Max voltage: " + str(wave_v_max))
print("Instrument ID: " + instrument)
print("Generator serial port: " + port_gen)
print("Scale " + scale)


ft = feeltech.FeelTech(port_gen)			#Connect the FY3224s generator
c1 = feeltech.Channel(1, ft)					#Init the CH1 of generator

ch1_v_max = numpy.zeros(freq_steps + 1)				#Create an array for CH1 measurements
ch2_v_max = numpy.zeros(freq_steps + 1)				#Create an array for CH2 measurements
db = numpy.zeros(freq_steps + 1)					#Create an array for the result in db
freq_values = numpy.zeros(freq_steps + 1)				#Create an array for values of frequency
db3 = numpy.zeros(freq_steps + 1)				#Create an array for plot a line in -3db
phase_values = numpy.zeros(freq_steps + 1)

c1.waveform(feeltech.SINE)					#CH1 will generate a sine wave
c1.amplitude(wave_v_max*2)					#Set CH1 peak to peak voltage
freq = freq_start
c1.frequency(freq)						#Set CH1 frequency

scope.write("TIMebase:MAIN:SCAle " + str(1/(3*freq)))	#Set horizontal scale of oscilloscope

if wave_v_max <= 3.5:						#Set vertical scale of oscilloscope
	scope.write("CHANnel1:SCALe 1")
	scope.write("CHANnel2:SCALe 1")
	
elif wave_v_max > 3.5 and wave_v_max <= 7:
	scope.write("CHANnel1:SCALe 2")
	scope.write("CHANnel2:SCALe 2")
	
elif wave_v_max > 7:
	scope.write("CHANnel1:SCALe 5")
	scope.write("CHANnel2:SCALe 5")

scope.write("MEASure:SETup:PSA CHANnel1")	#Setup CH1 as reference to measure phase
scope.write("MEASure:STATistic:ITEM RPHase")	#Setup CH1 as reference to measure phase

time.sleep(2*time_delay)					#Time delay

i = 0
while i <= freq_steps:
	c1.frequency(freq)						#Set CH1 (gen) frequency 
	scope.write("TIMebase:MAIN:SCAle "+ str(1/(3*freq)))		#Set the horizontal scale of oscilloscope
	time.sleep(time_delay)						#Time delay
	ch1_v_max[i] = scope.query("MEASure:ITEM? VMAX,CHANnel1")	#Read and save CH1 VMax
	ch2_v_max[i] = scope.query("MEASure:ITEM? VMAX,CHANnel2")	#Read and save CH2 Vmax
	phase_values[i] = scope.query("MEASure:STATistic:ITEM? AVERages,RPHase")
	freq_values[i] = freq						#Save actual frequency
	freq = freq + freq_inc						#Increment frequency
	db3[i] = -3.01
	i = i + 1							#Increment index

print("Ended")
print("-"*32)

if scale == 'db':
	db = (ch2_v_max/ch1_v_max)				#Cocient between ch2_v_max and ch1_v_max (for compute db)
	db = 20*numpy.log10(db)				#Compute db
	i = 0
	freq_cutoff = 0
	while i <= freq_steps:
		if db[i] <= -2.9 and db[i] >=-3.2:
			freq_cutoff = freq_values[i]
			break
		else:
			pass
		i = i + 1

	fig_db = plt.figure(1)
	plt.plot(freq_values,db)				#Graph data
	plt.axhline(-3.01, color = 'orchid', linestyle = ':', label = '-3dB')
	plt.axvline(freq_cutoff, color = 'orange', linestyle = ':', label = 'Cutoff Frequency (Aprox= ' + str(freq_cutoff) + ")")
	plt.xlabel('f')
	plt.ylabel('dB')
	plt.title('Magnitude Bode Plot')
	plt.grid()
	plt.legend()

	fig_phase = plt.figure(2)
	plt.plot(freq_values, phase_values)				#Graph data
	plt.axvline(freq_cutoff, color = 'orange', linestyle = ':', label = 'Cutoff Frequency (Aprox= ' + str(freq_cutoff) + ")")
	plt.xlabel('f')
	plt.ylabel('°')
	plt.title('Phase Bode Plot')
	plt.grid()
	plt.legend()
	plt.show()

elif scale == 'v':
	plt.plot(freq_values,ch2_v_max)			#Graph data
	plt.xlabel('f')
	plt.ylabel('Vout')
	plt.title('Bode Plot')
	plt.grid()
	plt.show()

elif scale == 'both':
	db = (ch2_v_max/ch1_v_max)				#Cocient between ch2_v_max and ch1_v_max (for compute db)
	db = 20*numpy.log10(db)				#Compute db
	fig_db = plt.figure(1)
	plt.plot(freq_values,db)				#Graph data
	plt.xlabel('f')
	plt.ylabel('dB')
	plt.title('Bode Plot (dB)')
	plt.grid()

	fig_v = plt.figure(2)
	plt.plot(freq_values,ch2_v_max)			#Graph data
	plt.xlabel('f')
	plt.ylabel('Vout')
	plt.title('Bode Plot (V)')
	plt.grid()
	plt.show()

scope.close()					#Stop communication with oscilloscope
ft.close()