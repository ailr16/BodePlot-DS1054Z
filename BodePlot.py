import pyvisa
import feeltech

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

freqInc = (endFreq/freqSteps)
#showParameters()

#Init Scope
rm = pyvisa.ResourceManager()
print(rm.list_resources())
instrument = input('Please enter the oscilloscope ID: ')
scope = rm.open_resource(instrument)


#Init Gen and CH1
ft = feeltech.FeelTech('/dev/ttyUSB0')
c1 = feeltech.Channel(1,ft)

c1.frequency(endFreq)
c1.amplitude(waveVMax*2)
#scope.write("MEASure:ITEM VMAX,CHANnel1")
vmax = scope.query("MEASure:ITEM? VMAX,CHANnel1")
print('VMAX=',vmax)

scope.close()

