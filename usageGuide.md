# Usage Guides

## GUI Version usage

[![IMAGE ALT TEXT](http://img.youtube.com/vi/HRYPE_VEFJE/0.jpg)](https://www.youtube.com/watch?v=HRYPE_VEFJE "Bode Plot GUI with Rigol DS1054Z and Feeltech FY3224S")

Download the last GUI release and unzip (I did in /home/)  
https://github.com/ailr16/BodePlot-DS1054Z/releases/tag/releaseGUIv1.1  

![/home path](/media/homePath.png)

1. Turn on the oscilloscope, connect it through USB to PC and enable CH1 and CH2: 
    ![Oscilloscope initial state](/media/oscilloscopeInitial.jpg)

2. Connect the probes to testpoints:  
    a. CH1 from oscilloscope to the "circuit input"  
    b. CH2 from oscilloscope to the "circuit output"  
    c. CH1 from Waveform Generator to the "circuit input"  
    ![Circuit testpoints schematic](/media/circuitTestPointsSch.png)  
    ![Circuit testpoints](/media/circuitTestPoints.jpg)  
    For this example we're gonna test an active low-pass filter (first order with simple 741)  
   
3. Turn on Waveform generator CH1 (if the CUT (*Circuit Under Test*) is an active circuit remember to energize before apply any signal on its inputs), and connect to PC through USB

    **NOTE: If the CUT inputs are under risk with high voltage signals remember to reduce amplitude BEFORE turning on the Output Channel**

    ![Turn on Generator](/media/generatorOn.jpg)  

    Example of Oscilloscope screen
    ![Oscilloscope example](/media/DS1Z_QuickPrint1.png)  

4. Run BodePlot.py (from the release folder)  
    If your OS supports running Python scripts with double click just go ahead, otherwise open the path in a terminal and run
    ```
    python bodePlot.py
    ```

5. The main window will open  
   a. Select Oscilloscope and Generator ports from the lists  
        ![Oscilloscope and generator selection](/media/selectFromList.png)  
   b. Enter the analysis parameters  
    - **Start Frequency**  
    - **End Frequency**  
    - **Frequency steps** Total steps for the frequency sweep  
    - **Max voltage** Voltage peak of the sine wave (this value equals to Amplitude/2)  
    - **Step delay** Specifies the delay between each step of frequency sweep. The defaulot value is 0.7 but I recommend to increase it for a better result, in this case 1.2s
    ![Enter analysis parameters](/media/analysisParam.png)  
   c. Press Run Analysis. Once the analysis is done, the plots will be showed
    ![Analysis done](/media/analysisDone.png)  
   d. The plots can be hided with the checkboxes
    ![Hiding amplitude](/media/hideAmplitude.png)  
   e. You can save the measured data as CSV and the plot picture as PNG, just specify the path in the text box and press the button  
   ![Saving files](/media/savedFiles.png)  

Here's an example of first-order active low-pass filter analysis with 100 steps. Theoretically. its cutoff frequency is near 7.2kHz, but is configured with gain of 2, so in this frequency we're gonna see more than 3dB. You can find the CSV in [this file](/media/19_11_2023__17_09_26.csv)

![Saving files](/media/19_11_2023__17_09_25.png)  

## CLI Version usage (outdated, working in new version with the GUI features)

[![IMAGE ALT TEXT](http://img.youtube.com/vi/WFBuwD8cPuU/0.jpg)](http://www.youtube.com/watch?v=WFBuwD8cPuU "Bode Plotter (DS1054Z-FY3224S)")

[![IMAGE ALT TEXT](http://img.youtube.com/vi/ivJM8q00k0E/0.jpg)](http://www.youtube.com/watch?v=ivJM8q00k0E "Bode Plot - Rigol DS1054Z and FY3224S")
1. Connect probes to the circuit:  
   a. CH1 from Waveform Generator to the "circuit input"  
   b. CH1 from oscilloscope to the "circuit input"  
   c. CH2 from oscilloscope to the "circuit output"  
3. Turn on Waveform generator CH1 and Oscilloscope CH2  
4. Run BodePlot.py  
    ```
    python BodePlot.py
    ```
3. Enter requested values  
   a. Start frequency. The initial frequency of test (Lower limit)  
   b. End Frequency. The final frequency for the test (Upper limit)  
   c. Frequency steps. The amount of steps which the range will be divided  
   d. Sine Wave Max Voltage. The Peak voltage for the generated sine wave  
   e. Oscilloscope ID. VISA oscilloscope ID. It's showed in the terminal  