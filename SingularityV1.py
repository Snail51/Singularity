import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import subprocess
import os
import time
import random
import winsound
import math
import datetime



# --- variables ---
cwd = os.path.join(os.path.dirname(__file__))
print os.path.join(os.path.dirname(__file__))
Music = ''.join([cwd,'\Clockbeat.wav'])
CanvasWidth = 700
CanvasHeight = 700
GameActive = 1
ShipRoot = (0,0)
PlayerSize = 10
Objects = [['rectangle',[(50,50),(100,100)],'static'],['rectangle',[(110,110),(160,160)],'dynamic']] #[type, [all (x,y) partings], interactability, dynamic function]
Energy = 0
MaxEnergy = 100
ProgressBars = []
Time = 0


# --- functions ---    
def clearCanvas():
    c.delete('all')
    
def motion(event):
    global ShipRoot
    global GameActive
    global PlayerSize
    ShipRoot = (event.x, event.y)
    if GameActive == 1:
        c.delete('ship')
        c.create_rectangle((int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize),fill="green",outline='green',tag='ship')
        #Check for collisions
        if len(c.find_overlapping(int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)) > 1:
            GameActive = 2
            
def CloseALL():
    global GameActive
    winsound.PlaySound(None, 0)
    root.destroy()
    GameActive = 0
    print "Thanks for playing!"

def StartALL(garbage):
    pass
    #TOTAL_MAIN()

def Timekeeper():
    global Time
    timeget = datetime.datetime.now()
    temptime = str(timeget)[11:]
    #print temptime
    hours = int(temptime[0:2])
    #print hours
    minutes = int(temptime[3:5])
    #print minutes
    seconds = int(temptime[6:8])
    #print seconds
    milla = 0
    try:
        milla = int(temptime[9:12])
    except:
        milla = 0
    #print milla
    minutes = int(minutes) + (int(hours) * 60)
    seconds = int(seconds) + (int(minutes) * 60)
    milla =int(milla) + (int(seconds) * 1000)
    #print milla
    Time = milla

    

def ClickRegistrar(event):
    global Objects
    Cursor = event.x, event.y
    n1 = 0
    pass

def Progressor():
    global ProgressBars
    global Energy
    global Time
    n1 = 0
    n2 = 0
    #print Time
    #print str(ProgressBars)
    for x in range(len(ProgressBars)):
        if str((ProgressBars[n2])[0]) is 'Energy':
            n1 = n1 + 1
            if int((ProgressBars[n2])[2]) < Time:
                #print 'aaa'
                Energy = Energy + int((ProgressBars[n2])[1])
                Mag = (ProgressBars[n2])[1]
                OldTime = int((ProgressBars[n2])[2])
                del ProgressBars[n2]
                ProgressBars.append(['Energy',Mag,OldTime+250])
                #print ProgressBars
                #print ''.join([str(Energy),' is now'])
        n2 = n2 + 1
    if n1 == 0:
        #print 'bbb'
        ProgressBars.append(['Energy',1, str(int(Time)+250)]) #Name, inc/dec amount, time when next tick
    
def Drawer():
    global CanvasHeight
    global CanvasWidth
    global Energy
    c.create_text((CanvasHeight*0.01,CanvasHeight/1.03),text=(''.join(["Energy: ",str(Energy)])), font=('Microsoft Yi Baiti Bold', 24), fill='white', justify='left',anchor='w')
    c.delete('ship')
    c.create_rectangle((int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize),fill="green",outline='green',tag='ship')

        
# --- Game Commands ---
def scrub(letter):
    pass




# --- Executives ---
def TOTAL_MAIN():
    global GameActive
    global time
    clearCanvas()
    Timekeeper()
    Progressor()
    Drawer()
    if GameActive == 1:
        c.after(1, TOTAL_MAIN)



# init    
root = tk.Tk()

#Make Canvas
c = tk.Canvas(master=root, width=CanvasWidth, height=CanvasHeight, bg='#1B2E4C')
c.bind('<Motion>', motion)
c.bind('<ButtonPress>', ClickRegistrar)
c.pack(pady=10)

# button with text closing window
b1 = tk.Button(root, text="Close", command=CloseALL, width=int(CanvasWidth/100) )
b1.pack(padx=5, pady=10, side='right')

#Create start/menu button
b2 = tk.Button(root, text="Start", command=None, width=int(CanvasWidth/100) )
b2.bind('<Button-1>', StartALL, )
b2.pack(padx=5, pady=10, side='left')

#Specific programs to be run once on startup.
TOTAL_MAIN()

winsound.PlaySound(Music,
                  winsound.SND_FILENAME|winsound.SND_ASYNC| winsound.SND_LOOP)



# "start the engine"
root.mainloop()