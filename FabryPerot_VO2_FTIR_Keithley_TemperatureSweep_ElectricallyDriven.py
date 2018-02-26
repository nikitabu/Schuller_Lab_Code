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
DevName   = 'Heater_200um' # in filename of saved plot 
NewFolder  = True    # save data into a subfolder?
FolderName = '18_01_15_Ge_VO2_1458_ReflectionResistance_Hysteresis_ElectricallyDriven_50C_200um'    # Only used if NewFolder=True

fname = 'Ge_VO2_1458_FabryPerot_200umSide_36x_3mm_R_50CAuBG';

current_start = 0;
current_end   = 0.03;
current_step  = 0.00025;

delay = 0.05

VoltageCompliance =  50     # Compliance (max) Voltage

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
#keithley.write(":SYST:RSEN 1")                                   # Turn On 4 Point Probe
keithley.write(":SOUR:FUNC:MODE CURR")                           # Set Current Source Function
keithley.write(":SENS:FUNC 'VOLT:DC'")
keithley.write(":SENS:VOLT:PROT:LEV " + str(VoltageCompliance))  # Set Voltage Compliance Level
keithley.write(":SENS:VOLT:RANGE:AUTO 1")                        # Set Voltage Measure Range to Auto
keithley.write(":OUTP ON")                                       # Output On Before Measuring   
              
Voltage = []
Current = []
VoltageError = []
CurrentError = []

#for kurrent in np.logspace(np.log10(current_start), np.log10(current_end), num=current_steps):
for kurrent in np.arange(current_start, current_end+current_step, current_step):
    #Voltage.append(V)
    print("Current set to: " + str(kurrent) + " A" )

    keithley.write(":SOUR:CURR " + str(kurrent))
    time.sleep(15)

    pag.click(45,  75,  clicks=1)
    time.sleep(1)
    pag.click(90,  245, clicks=1)
    time.sleep(1)
    pag.click(140, 305, clicks=1)
    time.sleep(1)
    
    pag.click(140, 305, clicks=1);
    time.sleep(1)
    pag.keyDown('ctrl');
    pag.press('a');
    pag.keyUp('ctrl');
    
    pag.typewrite(fname + '_Heating_' + str(1e3*kurrent) + 'mA')
    time.sleep(1)
             
    pag.click(55,  245, clicks=1)
    time.sleep(1)
    
    pag.click(150, 655, clicks=1)
    time.sleep(25)  
        
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

    print("--> Voltage = " + str(Voltage[-1]) + ' V')  # Print Last Value 

#for kurrent in np.logspace(np.log10(current_end), np.log10(current_start), num=current_steps):
for kurrent in np.arange(current_end, current_start-current_step, -current_step):
    #Voltage.append(V)
    print("Current set to: " + str(kurrent) + " A" )

    keithley.write(":SOUR:CURR " + str(kurrent))
    time.sleep(5)

    pag.click(45,  75,  clicks=1)
    time.sleep(1)
    pag.click(90,  245, clicks=1)
    time.sleep(1)
    pag.click(140, 305, clicks=1)
    time.sleep(1)
    
    pag.click(140, 305, clicks=1);
    time.sleep(1)
    pag.keyDown('ctrl');
    pag.press('a');
    pag.keyUp('ctrl');
    
    pag.typewrite(fname + '_Cooling_' + str(1e3*kurrent) + 'mA')
    time.sleep(1)
             
    pag.click(55,  245, clicks=1)
    time.sleep(1)
    
    pag.click(150, 655, clicks=1)
    time.sleep(25)  
        
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
    
    print("--> Voltage = " + str(Voltage[-1]) + ' V')  # Print Last Value 
             
keithley.write(":SOUR:CURR " + str(0))

############
### Plot ###
############

fig1, ax1 = plt.subplots(nrows=1, ncols=1) 
line1 = ax1.plot(np.arange(current_start, current_end+current_step, current_step), Voltage[:len(Voltage)/2], 'b+-')
line2 = ax1.plot(np.arange(current_end+current_step, current_start, -current_step), Voltage[len(Voltage)/2:], 'r+-')
ax1.set_xlabel('Current (A)')
ax1.set_ylabel('Voltage (V)')
ax1.set_title( 'Temp Sweep - ' + DevName + ' - Heating' )
ax1.grid(True)
fig1.show()

##################
### Save Files ###
##################

if SaveFiles:
    curtime = time.strftime('%Y-%M-%d_%H%M.%S')
    SavePath = 'Temp_Sweep_' + DevName
    # create subfolder if needed:
    if NewFolder and not os.path.isdir(FolderName): os.mkdir(FolderName)
    if NewFolder: SavePath = os.path.join(FolderName, SavePath )
    fig1.savefig(  SavePath + '.png'  )
    
    data = np.array(  zip(np.concatenate((np.arange(current_start, current_end+current_step, current_step), np.arange(current_end, current_start-current_step, -current_step))), Voltage, VoltageError, Current, CurrentError)  )
    np.savetxt( SavePath + '.txt', data, fmt="%e", delimiter="\t", header="Temp (K)\tVoltage (V)" )
    print "Saved data to:\n    %s" %(os.path.abspath(SavePath))

keithley.write(":OUTP OFF")                             # Turn Off Output

keithley.write("SYSTEM:KEY 23")                                   # Switch to Local Control
keithley.close()                                                  # Close the Connection