import time                     # to allow pause between measurements
import pyautogui as pag;        # for interfacing with Linksys

###################
### Export Loop ###
###################

for i in range(201):
    print(i+1)
    
    dt = 0.6;
    
    # select file
    pag.click(100, 149,  clicks=1)
    time.sleep(dt)
    
    # click save file button
    pag.click(100, 70, clicks=1)
    time.sleep(dt)
    
    # save
    pag.click(290, 680, clicks=1)
    time.sleep(dt)
   
    # right click file
    pag.rightClick(100, 149)
    time.sleep(dt)
    
    # click unload
    pag.rightClick(100, 195)
    time.sleep(dt)
    
    # save
    pag.click(300, 640, clicks=1)
    time.sleep(dt)    