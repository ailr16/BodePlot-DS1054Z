# BodePlot-DS1054Z

## Python based Bode plotter with Rigol DS1054Z and FY3224S

### Releases
- BodePlotGUI-v1.1 

   https://github.com/ailr16/BodePlot-DS1054Z/releases/tag/releaseGUIv1.1

   [![IMAGE ALT TEXT](http://img.youtube.com/vi/PC2ccm4rZgQ/0.jpg)](https://www.youtube.com/watch?v=PC2ccm4rZgQ "Bode Plotter (DS1054z and FY3224s)")

- BodePlot-v1.0 

   https://github.com/ailr16/BodePlot-DS1054Z/releases/tag/releaseV1


### Installing/Updating Required Modules
#### PyUSB
```
pip install pyusb
```
#### PyVisa
```
pip install PyVISA
pip install PyVISA-py
```

#### Feeltech control
```
pip install feeltech
```
#### Matplotlib
```
pip install matplotlib
```
#### NumPy
```
pip install numpy
```
#### psutil (your OS could recommend to install this)
```
pip install psutil
```
#### zeroconf (your OS could recommend to install this)
```
pip install zeroconf
```


### Usage Guide:
[View usageGuide.md](/usageGuide.md)
   

### Troubleshooting
#### Linux Users. */dev/ttyUSB0 permission denied*
1. Run (usually the generator port is ttyUSB0)
   ```
   ls -l <GENERATOR PORT>
   ```
   Example:
   ```
   ls -l /dev/ttyUSB0
   ```
   Output:

   `crw-rw---- 1 root uucp 188, 0 Jun 10 19:54 /dev/ttyUSB0`

   Look for the port group, listed after root, in this case `uucp`

2. Add your user to that group and reboot
 ```
 sudo usermod -a -G uucp <USER>
 reboot
 ```


#### Linux Users. *The oscilloscope don't shows in instrument list*

There's a guide to setup the instruments with VISA. Check this:https://lucask07.github.io/instrbuilder/build/html/linux_visa.html

1. Basically create the file *99-com.rules* inside */etc/udev/rules.d/* (if it don't exist)
   ```
   cd /etc/udev/rules.d/
   sudo nano 99-com.rules
   ```
2. Add the line:
   ```
   SUBSYSTEM=="usb", MODE="0666", GROUP="usbusers"
   ```
   And save with Ctrl+O
3. Add your user to *usbuser* group with:
    ```
    sudo groupadd usbusers
    sudo usermod -a -G usbusers <USERNAME>
    ```
4. Reboot

#### Arch Linux Users. *Error import Tkinter*
Install Tkinter with:

```
sudo pacman -S tk
```
