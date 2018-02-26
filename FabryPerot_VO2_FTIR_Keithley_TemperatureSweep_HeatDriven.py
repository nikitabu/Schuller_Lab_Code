# -*- coding: utf-8 -*-

"""
Keithley I-V Sweep 
Voltage-Source
Heating Only

Program to sweep voltage & measure current on Keithley SMU
Known bugs: the plot window opens *behind* the current window.
Also, file is saved *usually* in same directory as this script - but at one point it kept saving into the PythonXY directory, which was confusing.  Probably need to set the Python working directory to be sure.  Use `os.getcwd()` to see where it will save.

Edit/Run this file via Python(x,y) (click the 1st "Spyder" button to open the Spyder IDE)
Installed PyVISA for communication.

Based Off Demis John's Script from October 2014
Based off Steve Nichols' Script from ~2010
"""

#####################
### User Settings ###
#####################

Keithley_GPIB_Addr = 14     # GPIB Address of the Keithley (in Menu/Comms)

SaveFiles = True   # Save the plot & data?
DevName   = 'Thin_Film' # in filename of saved plot 

NewFolder  = True    # save data into a subfolder?
FolderName = '18_01_15_VO2_1523_ReflectionResistance_ThermallyDriven'    # Only used if NewFolder=True

fname = 'VO2_1523_15x_1mm_R_295KAuBG';

temp_start = 295;
temp_end   = 385;
temp_step  = 1;

delay = 0.05

VoltageCompliance =  20     # Compliance (max) Voltage
currentValue      =  1e-6   # Ending value of current sweep

######################
### Import Modules ###
######################

# You shouldn't need to edit anything below

import visa                     # PyVISA module fro GPIB communication, installed
import numpy as np              # enable NumPy numerical analysis
import time                     # to allow pause between measurements
import os                       # manipulate file paths and make directories
import matplotlib.pyplot as plt # for python-style plottting, like 'ax1.plot(x,y)'
import pyautogui as pag;               # for interfacing with Linksys
pag.FAILSAFE = False # disables the fail-safe
#from pylab import *            # for matlab-style plotting commands like `plot(x,y)`

# Open Visa connections to instruments
#keithley = visa.GpibInstrument(22)     # GPIB addr 22
rm       = visa.ResourceManager()
keithley = rm.get_instrument(  'GPIB::' + str(Keithley_GPIB_Addr)  )

#######################################
### Setup Keithley for Current Loop ###
#######################################

# Setup electrodes that are voltage

keithley.write("*RST")                                           # Reset the Unit
time.sleep(1)                                                # Pause
keithley.write(":SYST:RSEN 1")                                   # Turn On 4 Point Probe
keithley.write(":SOUR:FUNC:MODE CURR")                           # Set Current Source Function
keithley.write(":SENS:FUNC 'VOLT:DC'")
keithley.write(":SENS:VOLT:PROT:LEV " + str(VoltageCompliance))  # Set Voltage Compliance Level
keithley.write(":SENS:VOLT:RANGE:AUTO 1")                        # Set Voltage Measure Range to Auto
keithley.write(":OUTP ON")                                       # Output On Before Measuring   
              
Voltage = []
Current = []
VoltageError = []
CurrentError = []

for temp in np.arange(temp_start, temp_end+temp_step, temp_step):
    #Voltage.append(V)
    print("Temperature set to: " + str(temp) + " K" )
    tempC = temp - 273.15 #convert to C
    
    pag.click(1470, 130, clicks=2)
    pag.press('delete')
    pag.press('delete')
    pag.press('delete')
    pag.press('delete')
    pag.press('delete')
    pag.typewrite("%.2f" % tempC)
    pag.press('enter')
    time.sleep(15)  

    pag.click(45,  75,  clicks=1)
    time.sleep(0.5)
    pag.click(90,  245, clicks=1)
    time.sleep(0.5)
    pag.click(140, 305, clicks=1)
    time.sleep(0.5)
    
    pag.click(140, 305, clicks=1);
    time.sleep(0.5)
    pag.keyDown('ctrl');
    pag.press('a');
    pag.keyUp('ctrl');
    
    pag.typewrite(fname + '_Heating_' + str(temp) + 'K')
    time.sleep(0.5)
             
    pag.click(55,  245, clicks=1)
    time.sleep(0.5)
    
    pag.click(150, 655, clicks=1)
    time.sleep(30)  
                  
    keithley.write(":SOUR:CURR " + str(currentValue))
    time.sleep(5)
    
    data = keithley.ask(":READ?").split(',');
    V    = eval( data.pop(0) )
    if V > 1:
        currentValue = currentValue/10;
    if V < 0.01:
        currentValue = currentValue*10;
        
    keithley.write(":SOUR:CURR " + str(currentValue))
          
    time.sleep(5)
    
    Vs = []
    Is = []
    
    for i in range(100):
        data = keithley.ask(":READ?").split(',');
        V    = eval( data.pop(0) )
        I    = eval( data.pop(0) )  
        Vs.append(V)
        Is.append(I)
    
    Voltage.append(np.mean(Vs))
    Current.append(np.mean(Is))
    VoltageError.append(np.std(Vs))
    CurrentError.append(np.std(Is))    
    
    keithley.write(":SOUR:CURR " + str(0))              # Set Current Level

    print("--> Voltage = " + str(Voltage[-1]) + ' V')  # Print Last Value 
             
for temp in np.arange(temp_end, temp_start-temp_step, -temp_step):
    #Voltage.append(V)
    print("Temperature set to: " + str(temp) + " K" )
    tempC = temp - 273.15 #convert to C
    
    pag.click(1470, 130, clicks=2)
    pag.press('delete')
    pag.press('delete')
    pag.press('delete')
    pag.press('delete')
    pag.press('delete')
    pag.typewrite("%.2f" % tempC)
    pag.press('enter')
    time.sleep(15)  

    pag.click(45,  75,  clicks=1)
    time.sleep(0.5)
    pag.click(90,  245, clicks=1)
    time.sleep(0.5)
    pag.click(140, 305, clicks=1)
    time.sleep(0.5)
    
    pag.click(140, 305, clicks=1);
    time.sleep(0.5)
    pag.keyDown('ctrl');
    pag.press('a');
    pag.keyUp('ctrl');
    
    pag.typewrite(fname + '_Cooling_' + str(temp) + 'K')
    time.sleep(0.5)
             
    pag.click(55,  245, clicks=1)
    time.sleep(0.5)
    
    pag.click(150, 655, clicks=1)
    time.sleep(30)  
                  
    keithley.write(":SOUR:CURR " + str(currentValue))
    time.sleep(5)
    
    data = keithley.ask(":READ?").split(',');
    V    = eval( data.pop(0) )
    if V > 1:
        currentValue = currentValue/10;
    if V < 0.01:
        currentValue = currentValue*10;
        
    keithley.write(":SOUR:CURR " + str(currentValue))
          
    time.sleep(5)
    
    Vs = []
    Is = []
    
    for i in range(100):
        data = keithley.ask(":READ?").split(',');
        V    = eval( data.pop(0) )
        I    = eval( data.pop(0) )  
        Vs.append(V)
        Is.append(I)
    
    Voltage.append(np.mean(Vs))
    Current.append(np.mean(Is))
    VoltageError.append(np.std(Vs))
    CurrentError.append(np.std(Is))    
    
    keithley.write(":SOUR:CURR " + str(0))              # Set Current Level

    print("--> Voltage = " + str(Voltage[-1]) + ' V')  # Print Last Value 
    
############
### Plot ###
############

fig1, ax1 = plt.subplots(nrows=1, ncols=1) 

line1 = ax1.plot(np.arange(temp_start, temp_end+temp_step, temp_step), Voltage[:len(Voltage)/2], 'b+-')

ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('Voltage (V)')
ax1.set_title( 'Temp Sweep - ' + DevName + ' - ' + str(currentValue) + 'A Heating' )
ax1.set_yscale('log')

ax1.grid(True)

fig1.show()

##################
### Save Files ###
##################

if SaveFiles:
    curtime = time.strftime('%Y-%M-%d_%H%M.%S')
    SavePath = 'Temp_Sweep_' + DevName + '_' + str(currentValue) + 'A_Heating'
    # create subfolder if needed:
    if NewFolder and not os.path.isdir(FolderName): os.mkdir(FolderName)
    if NewFolder: SavePath = os.path.join(FolderName, SavePath )
    fig1.savefig(  SavePath + '.png'  )
    
    data = np.array(  zip(np.arange(temp_start, temp_end+temp_step, temp_step), Voltage, VoltageError, Current, CurrentError)  )
    np.savetxt( SavePath + '.txt', data, fmt="%e", delimiter="\t", header="Temp (K)\tVoltage (V)" )
    print "Saved data to:\n    %s" %(os.path.abspath(SavePath))

keithley.write(":OUTP OFF")                             # Turn Off Output

keithley.write("SYSTEM:KEY 23")                                   # Switch to Local Control
keithley.close()                                                  # Close the Connection