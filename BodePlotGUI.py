import pyvisa
import feeltech
import time
import numpy
import matplotlib.pyplot as plt
import math
import tkinter
import serial

bg_color = '#66E1FF'
error_fg = '#F35432'

window = tkinter.Tk()
window.resizable(False, False)
window.title('Bode Plot - DS1054z')
window.geometry('800x480')
window.configure(bg = bg_color)

#Start frequency section ----------------------------------
start_freq_label= tkinter.Label(window,
			    	 text = 'Start Frequency',
			    	 bg = bg_color,
			    	 font = ('Arial', 16))

start_freq_label.place(relx = 0.05,
			rely = 0.05)
			
start_freq_error_label = tkinter.Label(window,
			    	 	text = '',
			    	 	bg = bg_color,
				    	font = ('Arial', 12),
				    	fg = error_fg)

start_freq_error_label.place(relx = 0.38,
			      rely = 0.057)

def start_freq_fn(var):
	content = var.get()
	if int(content) < 0 :
		start_freq_error_label["text"] = 'Error. Frequency must be a possitive value'
	else:
		start_freq_error_label["text"] = ''
		
var = tkinter.StringVar()
var.trace("w", lambda name, index, mode, var = var:start_freq_fn(var))

start_freq_entry = tkinter.Entry(window,
				  width = 8,
				  font = ('Arial', 16), textvariable = var)
start_freq_entry.place(relx = 0.25,
	    		rely = 0.05)
start_freq_entry.delete(0, 'end')
start_freq_entry.insert(0, '100')
#End frequency section ------------------------------------
end_freq_label = tkinter.Label(window,
			 	text = 'End Frequency',
				bg = bg_color,
				font=('Arial', 16))
			  
end_freq_label.place(relx = 0.055,
		      rely = 0.12)

end_freq_error_label = tkinter.Label(window,
			    	      text = '',
			    	      bg = bg_color,
				      font = ('Arial', 12),
				      fg = error_fg)

end_freq_error_label.place(relx = 0.38,
			    rely = 0.127)

def end_freq_fn(var, var1):
	content = var.get()
	content1 = var1.get()
	if int(content) < 0 :
		end_freq_error_label["text"] = 'Error. Frequency must be a possitive value'
	else:
		if int(content) <= int(content1):
			end_freq_error_label["text"] = 'Error. Frequency must be greater than Start frequency'
		else:
			end_freq_error_label["text"] = ''
		
var1 = tkinter.StringVar()
var1.trace("w", lambda name, index, mode, var1 = var1:end_freq_fn(var1,var))

end_freq_entry = tkinter.Entry(window,
				width = 8,
				font = ('Arial', 16), textvariable = var1)
				
end_freq_entry.place(relx = 0.25,
		     rely = 0.12)
end_freq_entry.delete(0, 'end')
end_freq_entry.insert(0, '10000')
#Frequency steps section ----------------------------------
freq_step_label = tkinter.Label(window,
			 	 text = 'Steps',
				 bg = bg_color,
				 font=('Arial', 16))
			  
freq_step_label.place(relx = 0.17,
		      rely = 0.19)

step_freq_error_label = tkinter.Label(window,
			    	       text = '',
			    	       bg = bg_color,
				       font = ('Arial', 12),
				       fg = error_fg)

step_freq_error_label.place(relx = 0.38,
			     rely = 0.197)
			     
def step_freq_fn(var):
	content = var.get()
	if int(content) <= 0 :
		step_freq_error_label["text"] = 'Error. Step must be greater than zero'
	else:
		step_freq_error_label["text"] = ''
		
var2 = tkinter.StringVar()
var2.trace("w", lambda name, index, mode, var2 = var2:step_freq_fn(var2))

step_freq_entry = tkinter.Entry(window,
				 width = 8,
				 font = ('Arial', 16), textvariable = var2)
step_freq_entry.place(relx = 0.25,
		      rely = 0.19)
step_freq_entry.delete(0, 'end')
step_freq_entry.insert(0, '10')
#Max voltage section ----------------------------------
max_vol_label = tkinter.Label(window,
			 	 text = 'Max Voltage',
				 bg = bg_color,
				 font=('Arial', 16))
			  
max_vol_label.place(relx = 0.092,
		      rely = 0.26)

max_vol_error_label = tkinter.Label(window,
			    	       text = '',
			    	       bg = bg_color,
				       font = ('Arial', 12),
				       fg = error_fg)

max_vol_error_label.place(relx = 0.38,
			     rely = 0.267)
			     
def max_vol_fn(var):
	content = var.get()
	if int(content) <= 0 :
		max_vol_error_label["text"] = 'Error. Step must be greater than zero'
	elif int(content) > 10 :
		max_vol_error_label["text"] = 'Error. Step must be less than 10'
	else:
		max_vol_error_label["text"] = ''
		
var3 = tkinter.StringVar()
var3.trace("w", lambda name, index, mode, var3 = var3:max_vol_fn(var3))

max_vol_entry = tkinter.Entry(window,
				 width = 8,
				 font = ('Arial', 16), textvariable = var3)
max_vol_entry.place(relx = 0.25,
		      rely = 0.26)
max_vol_entry.delete(0, 'end')
max_vol_entry.insert(0, '10')


#Update variables -------------------------------------

start_frequency = int(start_freq_entry.get())
end_frequency = int(end_freq_entry.get())
step_frequency = int(step_freq_entry.get())
max_voltage = int(max_vol_entry.get())
print('sf' + str(start_frequency))
print('ef' + str(end_frequency))
print('s' + str(step_frequency))
print('mv' + str(max_voltage))


#Exit button
boton = tkinter.Button(window,
			text = 'Exit',
			command = exit)
boton.place(relx = 0.9,
	    rely = 0.72)
  
#ventana.after(10100, leeImprime)

#leeImprime()
window.mainloop()
