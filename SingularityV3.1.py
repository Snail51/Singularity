import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import subprocess
import os
import time
import random
import winsound
import math
import datetime

# --- Config ---
StartingEnergy = 0
StartingMaxEnergy = 100
ClickCost = 25
PlayerSize = 10
EnergyRate = 500
MaxEnergyRate = 1000
MaxEnergyCap = 200
JitterRate = 2500


# --- variables ---
cwd = os.path.join(os.path.dirname(__file__))
print os.path.join(os.path.dirname(__file__))
Music = ''.join([cwd,'\Background.wav'])
CanvasWidth = 700
CanvasHeight = 700
GameActive = 1
ShipRoot = (0,0)
Energy = 0
MaxEnergy = 100
ProgressBars = [] #Name, inc/dec amount, time when next tick
Time = 0
Gitter = (0,0)





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
        '''
        if len(c.find_overlapping(int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)) > 1:
            GameActive = 2
            '''
def CloseAll():
    global GameActive
    winsound.PlaySound(None, 0)
    root.destroy()
    GameActive = 0
    print "Thanks for playing!"

def StartAll():
    global EnergyRate
    global MaxEnergyRate
    global JitterRate
    Scorekeeper('CLEAR',0)
    BarAdd('Energy',1,str(EnergyRate)) #Title, Magnitude, Next Tick, Tick Delay
    BarAdd('MaxEnergy',1,str(MaxEnergyRate))
    BarAdd('Jitter',0,str(JitterRate))


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

def AlphaRelate(Int):
    Return = ''
    if Int == 1:
        Return = 'a'
    elif Int == 2:
        Return = 'b'
    elif Int == 3:
        Return = 'c'
    elif Int == 4:
        Return = 'd'
    elif Int == 5:
        Return = 'e'
    elif Int == 6:
        Return = 'f'
    elif Int == 7:
        Return = 'g'
    elif Int == 8:
        Return = 'h'
    elif Int == 9:
        Return = 'i'
    elif Int == 10:
        Return = 'j'
    elif Int == 11:
        Return = 'k'
    elif Int == 12:
        Return = 'l'
    elif Int == 13:
        Return = 'm'
    elif Int == 14:
        Return = 'n'
    elif Int == 15:
        Return = 'o'
    elif Int == 16:
        Return = 'p'
    elif Int == 17:
        Return = 'q'
    elif Int == 18:
        Return = 'r'
    elif Int == 19:
        Return = 's'
    elif Int == 20:
        Return = 't'
    elif Int == 21:
        Return = 'u'
    elif Int == 22:
        Return = 'v'
    elif Int == 23:
        Return = 'w'
    elif Int == 24:
        Return = 'x'
    elif Int == 25:
        Return = 'y'
    elif Int == 26:
        Return = 'z'
    else:
        Return = 'NULL'
    return (Return)
    

def ClickRegistrar(event):
    global Objects
    #print (int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)
    Overlaps = c.find_overlapping(int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)
    n1 = 1
    for x in range(26):
        Checker = c.find_withtag(''.join(['Server',AlphaRelate(n1)]))
        n2 = 0
        for x in range(len(Checker)):
            #print Checker
            if Checker[n2] in Overlaps:
                #print AlphaRelate(n1)
                ServerSelect(AlphaRelate(n1))
            n2 = n2 + 1
        n1 = n1 + 1
        
def ServerSelect(tagstring):
    global Energy
    global ClickCost
    if Energy > 25:
        Energy = Energy - ClickCost
        print ''.join([tagstring, ' was pressed!'])
    
def Progressor():
    global ProgressBars
    global Time
    n2 = 0 #Search Pointer
    #print Time
    #print ProgressBars
    for x in range(len(ProgressBars)):
        if int((ProgressBars[n2])[2]) < Time:
            #print len(ProgressBars)
            #print ((ProgressBars[n2])[2])
            #print n2
            #print ProgressBars
            Scorekeeper(str((ProgressBars[n2])[0]),int((ProgressBars[n2])[1]))
            OldTitle = str((ProgressBars[n2])[0])
            Mag = int((ProgressBars[n2])[1])
            OldTick = int((ProgressBars[n2])[2])
            OldDelay = int((ProgressBars[n2])[3])
            #print ProgressBars[n2]
            del ProgressBars[n2]
            ProgressBars.insert(0, ([OldTitle,Mag,int(OldTick)+int(OldDelay),OldDelay]))
            #print ProgressBars    
        n2 = n2 + 1
  

def BarAdd(string, magnitude, delay): #Create a new progress bar
    global ProgressBars
    global Time 
    n1 = 0
    n2 = 0
    for x in range(len(ProgressBars)):
        #print len(ProgressBars)
        if (ProgressBars[n1])[0] is string:
            del ProgressBars[n1]
            n2 = 1
            ProgressBars.insert(0,[str(string),magnitude, (int(Time)+int(delay)),delay])
        n1 = n1 + 1
    if n2 == 0:
        ProgressBars.insert(0,[str(string),magnitude, (int(Time)+int(delay)),delay])
    #print ProgressBars

    
def Scorekeeper(variable,amount):
    global Energy
    global MaxEnergy
    global StartingEnergy
    global StartingMaxEnergy
    global ProgressBars
    global EnergyRate
    global MaxEnergyRate
    global MaxEnergyCap
    if variable is 'CLEAR':
        ProgressBars = []
        Energy = StartingEnergy
        MaxEnergy = StartingMaxEnergy

    
    #UPDATE
    if variable is 'Jitter':
        Jitter()
    if variable is 'Energy':
        Energy = Energy + amount
    if variable is 'MaxEnergy' and MaxEnergy < MaxEnergyCap:
        MaxEnergy = MaxEnergy + amount
        if MaxEnergy >= MaxEnergyCap:
            BarAdd('Energy', 1, EnergyRate/2)


        
    # LIMITS
    if Energy > MaxEnergy:
        Energy = MaxEnergy

def DrawServers():
    global CanvasHeight
    global CanvasWidth
    global Gitter
    n2 = 1
    n3 = 1
    for x in range(4):
        Height = CanvasHeight/10
        Height = Height * n2
        n2 = n2 + 1
        n1 = 1
        for x in range(6):
            Width = CanvasWidth/7.5
            Width = Width * n1
            c.create_rectangle((Width+Gitter[0], Height+Gitter[1], Width+50+Gitter[0], Height+50+Gitter[1]),fill="black",outline='white',tag=(''.join(['Server',AlphaRelate(n3)])))
            c.create_text((Width+15+Gitter[0], Height+20+Gitter[1]),text=(AlphaRelate(n3)), font=('Inhuman BB', 36), fill='white', justify='left',anchor='w',tag=(''.join(['ServerText',AlphaRelate(n3)])))
            n3 = n3 + 1
            n1 = n1 + 1
    n2 = n2 + 1
    n1 = 1
    for x in range(2):
        Width = CanvasWidth/7.5
        Width = Width * n1
        Height = (CanvasHeight/10) * 5
        c.create_rectangle((Width+Gitter[0], Height+Gitter[1], Width+50+Gitter[0], Height+50+Gitter[1]),fill="black",outline='white',tag=(''.join(['Server',AlphaRelate(n3)])))
        c.create_text((Width+15+Gitter[0], Height+20+Gitter[1]),text=(AlphaRelate(n3)), font=('Inhuman BB', 36), fill='white', justify='left',anchor='w',tag=(''.join(['ServerText',AlphaRelate(n3)])))
        n1 = n1 + 5
        n3 = n3 + 1
    
def Jitter():
    global Gitter
    Gitter = [random.randint(-1,1),random.randint(-1,1),random.randint(-1,1),random.randint(-1,1),random.randint(-1,1)]
    
def DrawMaster():
    global CanvasHeight
    global CanvasWidth
    global Energy
    global MaxEnergy
    global Gitter
    clearCanvas()
    #Draw Servers
    DrawServers()
    #Draw Player
    c.delete('ship')
    c.create_rectangle((int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize),fill="green",outline='green',tag='ship')
    #Draw Text
    c.create_text((((CanvasHeight*0.01)+Gitter[0]),((CanvasHeight/1.03)+Gitter[1])),text=(''.join(["Energy: ",str(Energy),'/',str(MaxEnergy)])), font=('Inhuman BB', 24), fill='white', justify='left',anchor='w')

        
# --- Game Commands ---
def scrub(letter):
    pass




# --- Executives ---
def TOTAL_MAIN():
    global GameActive
    global Time
    Timekeeper()
    Progressor()
    DrawMaster()
    c.after(1, TOTAL_MAIN)



# init    
root = tk.Tk()

#Make Canvas
c = tk.Canvas(master=root, width=CanvasWidth, height=CanvasHeight, bg='#000000')
c.bind('<Motion>', motion)
c.bind('<ButtonPress>', ClickRegistrar)
c.pack(pady=10)

# button with text closing window
b1 = tk.Button(root, text="Close", command=CloseAll, width=int(CanvasWidth/100) )
b1.pack(padx=5, pady=10, side='right')

#Create start/menu button
b2 = tk.Button(root, text="Start", command=StartAll, width=int(CanvasWidth/100) )
b2.pack(padx=5, pady=10, side='left')

#Specific programs to be run once on startup.
TOTAL_MAIN()

winsound.PlaySound(Music,
                  winsound.SND_FILENAME|winsound.SND_ASYNC| winsound.SND_LOOP)



# "start the engine"
root.mainloop()