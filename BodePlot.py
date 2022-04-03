import pyvisa
import feeltech
import time
import numpy
import matplotlib.pyplot as plt
import math

fichero = open('config.txt')
########################
timeDelay = 0.7 #Adjust the time delay between frequency increments (in seconds)
########################

startFreq = float(fichero.readline().split(',')[1])		#Read the start frequency
endFreq = float(fichero.readline().split(',')[1])		#Read the end frequency
if startFreq < 0 or endFreq < 0:
	print('ERROR. Frequency must be possitive')
	print('Please press Enter to exit :-(')
	input()
	exit()
if startFreq > endFreq:
	print('ERROR. Start Frequency must be less than End Frequency')
	print('Please press Enter to exit:-(')
	input()
	exit()

freqSteps = int(fichero.readline().split(',')[1])			#Read the frequency steps
if freqSteps <= 0:
	print('ERROR. Frequency steps must be greater than zero')
	print('Please press Enter to exit :-(')
	input()
	exit()
waveVMax = float(fichero.readline().split(',')[1])		#Read the max voltage of sine wave
if waveVMax <= 0:
	print('ERROR. Max Voltage must be greater than zero')
	print('Please press Enter to exit :-(')
	input()
	exit()

freqInc = ((endFreq-startFreq)/freqSteps)			#Compute the frequency increments in function of steps, start and end frequencies

rm = pyvisa.ResourceManager()						#PyVISA Resource Manager
instrument = fichero.readline().split(',')[1]
instrument = instrument[:-1]
scope = rm.open_resource(instrument)				#Identify oscilloscope with "scope"
scope.write("MEASure:CLEar ALL")					#Clear all measurement items
scope.write("MEASure:ITEM VMAX,CHANnel1")			#Create the VMax measurement item for CH1
scope.write("MEASure:ITEM VMAX,CHANnel2")			#Create the VMax measurement item for CH2

port_gen = fichero.readline().split(',')[1]
port_gen = port_gen[:-1]


print("Start Frequency: " + str(startFreq))
print("End Frequency" + str(endFreq))
print("Frequency Step: " + str(freqSteps))
print("Max voltage: " + str(waveVMax))
print("Instrument ID: " + instrument)
print("Generator serial port: " + port_gen)

ft = feeltech.FeelTech(port_gen)			#Connect the FY3224s generator
c1 = feeltech.Channel(1,ft)					#Init the CH1 of generator

CH1VMax = numpy.zeros(freqSteps+1)				#Create an array for CH1 measurements
CH2VMax = numpy.zeros(freqSteps+1)				#Create an array for CH2 measurements
db = numpy.zeros(freqSteps+1)					#Create an array for the result in db
freqValues = numpy.zeros(freqSteps+1)				#Create an arrayo for values of frequency

c1.waveform(feeltech.SINE)					#CH1 will generate a sine wave
c1.amplitude(waveVMax*2)					#Set CH1 peak to peak voltage
freq = startFreq
c1.frequency(freq)						#Set CH1 frequency

scope.write("TIMebase:MAIN:SCAle " + str(1/(3*freq)))	#Set horizontal scale of oscilloscope

if waveVMax <= 3.5:						#Set vertical scale of oscilloscope
	scope.write("CHANnel1:SCALe 1")
	scope.write("CHANnel2:SCALe 1")
	
elif waveVMax > 3.5 and waveVMax <= 7:
	scope.write("CHANnel1:SCALe 2")
	scope.write("CHANnel2:SCALe 2")
	
elif waveVMax > 7:
	scope.write("CHANnel1:SCALe 5")
	scope.write("CHANnel2:SCALe 5")
	
time.sleep(2*timeDelay)					#Time delay

i = 0
while i <= freqSteps:
	c1.frequency(freq)						#Set CH1 (gen) frequency 
	scope.write("TIMebase:MAIN:SCAle "+ str(1/(3*freq)))		#Set the horizontal scale of oscilloscope
	time.sleep(timeDelay)						#Time delay
	CH1VMax[i] = scope.query("MEASure:ITEM? VMAX,CHANnel1")	#Read and save CH1 VMax
	CH2VMax[i] = scope.query("MEASure:ITEM? VMAX,CHANnel2")	#Read and save CH2 Vmax
	freqValues[i] = freq;						#Save actual frequency
	freq = freq + freqInc						#Increment frequency
	i = i + 1							#Increment index

scale = fichero.readline().split(',')[1]

if scale == 'db':
	db = (CH2VMax/CH1VMax)				#Cocient between CH2VMax and CH1VMax (for compute db)
	db = 20*numpy.log10(db)				#Compute db
	plt.plot(freqValues,db)			#Graph data
	plt.xlabel('f')
	plt.ylabel('dB')
	plt.title('Bode Plot')
	plt.grid()
	plt.show()

elif scale == 'v':
	plt.plot(freqValues,CH2VMax)			#Graph data
	plt.xlabel('f')
	plt.ylabel('Vout')
	plt.title('Bode Plot')
	plt.grid()
	plt.show()

elif scale == 'both':
	db = (CH2VMax/CH1VMax)				#Cocient between CH2VMax and CH1VMax (for compute db)
	db = 20*numpy.log10(db)				#Compute db
	figdb = plt.figure(1)
	plt.plot(freqValues,db)				#Graph data
	plt.xlabel('f')
	plt.ylabel('dB')
	plt.title('Bode Plot (dB)')
	plt.grid()

	figv = plt.figure(2)
	plt.plot(freqValues,CH2VMax)			#Graph data
	plt.xlabel('f')
	plt.ylabel('Vout')
	plt.title('Bode Plot (V)')
	plt.grid()
	plt.show()

scope.close()					#Stop communication with oscilloscope
ft.close()
