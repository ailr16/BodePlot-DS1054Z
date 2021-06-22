import pyvisa
import feeltech
import time
import numpy
import matplotlib.pyplot as plt
import math

timeDelay = 0.6
startFreq = float(input('Start Frequency (in Hz): '))
endFreq = float(input('End Frequency (in Hz): '))
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

waveVMax = float(input('Sine Wave Max Voltage: '))
if waveVMax <= 0:
	print('ERROR. Max Voltage must be greater than zero')
	print('Please press Enter to exit :-(')
	input()
	exit()
		
freqSteps = int(input('Frequency Steps: '))
if freqSteps <= 0:
	print('ERROR. Max Voltage must be greater than zero')
	print('Please press Enter to exit :-(')
	input()
	exit()

def showParameters():
	print('Start Frequency=', startFreq, "Hz")
	print('End Frequency=', endFreq, "Hz")
	print('Sine Wave Max Voltage=', waveVMax, "V")
	print('Frequency Steps=', freqSteps)
	print('Frequency Increment=', freqInc)

freqInc = ((endFreq-startFreq)/freqSteps)
#showParameters()

#Init Scope
rm = pyvisa.ResourceManager()
print(rm.list_resources())
instrument = input('Please enter the oscilloscope ID: ')
scope = rm.open_resource(instrument)
scope.write("MEASure:CLEar ALL")
scope.write("MEASure:ITEM VMAX,CHANnel1")
scope.write("MEASure:ITEM VMAX,CHANnel2")

#Init Gen and CH1
ft = feeltech.FeelTech('/dev/ttyUSB0')
c1 = feeltech.Channel(1,ft)

CH1VMax = numpy.zeros(freqSteps+1)
CH2VMax = numpy.zeros(freqSteps+1)
db = numpy.zeros(freqSteps+1)
freqValues = numpy.zeros(freqSteps+1)
c1.amplitude(waveVMax*2)
freq = startFreq
c1.frequency(freq)
time.sleep(2*timeDelay)
i = 0
while i <= freqSteps:
	CH1VMax[i] = scope.query("MEASure:ITEM? VMAX,CHANnel1")
	CH2VMax[i] = scope.query("MEASure:ITEM? VMAX,CHANnel2")
	freqValues[i] =freq;
	freq = freq + freqInc
	c1.frequency(freq)
	time.sleep(timeDelay)
	i = i + 1

print(CH2VMax)
print(freqValues)


db = (CH2VMax/CH1VMax)
db = numpy.log10(db)

plt.plot(freqValues,db)
plt.xlabel('f')
plt.ylabel('dB')
plt.title('Bode Plot')
plt.grid()
plt.show()

scope.close()

