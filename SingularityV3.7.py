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
ClickCost = 5
PlayerSize = 20
EnergyRate = 100
MaxEnergyRate = 4000
MaxEnergyCap = 200
JitterRate = 200
ScrubLength = 5000
StartingViruses = 3
ProblemRate = (10000,20000)
ProblemLength = 6
StartingHealth = 100


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
Prompt = 'aaa'
Blacklist = []
Viruses = []
News = 'bbb'
Problem = 'ccc'
Health = 0





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
        c.create_line((int(ShipRoot[0]), int(ShipRoot[1])+PlayerSize, int(ShipRoot[0]), int(ShipRoot[1])-PlayerSize),fill="red",tag='ship')
        c.create_line((int(ShipRoot[0])-PlayerSize, int(ShipRoot[1]), int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])),fill="red",tag='ship')
        c.create_oval(((int(ShipRoot[0])-PlayerSize/1.5), (int(ShipRoot[1])-PlayerSize/1.5), (int(ShipRoot[0])+PlayerSize/1.5), (int(ShipRoot[1])+PlayerSize/1.5)),outline='red')

def CloseAll():
    global GameActive
    winsound.PlaySound(None, 0)
    root.destroy()
    GameActive = 0
    print "Thanks for playing!"

def StartAll():
    global EnergyRate
    global MaxEnergyRate
    global Viruses
    global StartingViruses
    global ProblemRate
    global Health
    global StartingHealth
    global Problem
    global Prompt
    global News
    Problem = ''
    Prompt = ''
    News = ''
    Health = StartingHealth
    Scorekeeper('CLEAR',0)
    BarAdd('Energy',1,str(EnergyRate),1) #Title, Magnitude, Next Tick, Tick Delay
    BarAdd('MaxEnergy',1,str(MaxEnergyRate),1)
    BarAdd('ProblemTrigger',1,str(random.randint(ProblemRate[0],ProblemRate[1])),0)
    for x in range(StartingViruses):
        Viruses.append(AlphaRelate(random.randint(1,26)))
    print Viruses
    


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
    elif Int == 27:
        Return = '_'
    elif Int == 28:
        Return = 'Enter'
    else:
        Return = 'NULL'
    Return = Return.lower()
    return (Return)

def RandomString(length):
    Return = ''
    for x in range(length):
        Return = ''.join([Return,str(AlphaRelate(random.randint(1,26)))])
    return Return
    

def ClickRegistrar(event):
    global Blacklist
    #print (int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)
    Overlaps = c.find_overlapping(int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)
    n1 = 1
    for x in range(28):
        Checker = c.find_withtag(''.join(['Server',AlphaRelate(n1)]))
        n2 = 0
        for x in range(len(Checker)):
            #print Checker
            if Checker[n2] in Overlaps:
                #print AlphaRelate(n1)
                if AlphaRelate(n1) not in Blacklist:
                    ServerSelect(AlphaRelate(n1))
            n2 = n2 + 1
        n1 = n1 + 1
        
def ServerSelect(tagstring):
    global Energy
    global ClickCost
    global Prompt
    if Energy >= ClickCost:
        Energy = Energy - ClickCost
        #print tagstring
        if (str(tagstring).upper()) == 'ENTER':
            PromptEnter(Prompt)
            Prompt = ''
        else:
            Prompt = ''.join([str(Prompt),str(tagstring)])
        #print Prompt

def PromptEnter(Prompt):
    #print Prompt
    global Problem
    n1 = 0
    if Prompt == Problem:
        Problem = ''
    scrublist = ['scrub', 'scan', 'disinfect', 'antivirus', 'check', 'clean']
    for x in range(len(scrublist)):
        if scrublist[n1] in Prompt:
            scrub(Prompt[-1])
        n1 = n1 + 1

    
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
            Scorekeeper(str((ProgressBars[n2])[0]),((ProgressBars[n2])[1]))
            OldTitle = str((ProgressBars[n2])[0])
            Mag = str((ProgressBars[n2])[1])
            OldTick = int((ProgressBars[n2])[2])
            OldDelay = int((ProgressBars[n2])[3])
            Persistance = int((ProgressBars[n2])[4])
            #print ProgressBars[n2]
            del ProgressBars[n2]
            if Persistance != 0:
                ProgressBars.insert(0, ([OldTitle,Mag,int(OldTick)+int(OldDelay),OldDelay,Persistance]))
            if Persistance == 0: 
                n2 = n2 - 1
            #print ProgressBars    
        n2 = n2 + 1
  

def BarAdd(string, magnitude, delay, persistance): #Create a new progress bar
    global ProgressBars
    global Time 
    n1 = 0
    n2 = 0
    for x in range(len(ProgressBars)):
        #print len(ProgressBars)
        if (ProgressBars[n1])[0] is string:
            del ProgressBars[n1]
            n2 = 1
            ProgressBars.insert(0,[str(string),magnitude, (int(Time)+int(delay)),delay,persistance])
        n1 = n1 + 1
    if n2 == 0:
        ProgressBars.insert(0,[str(string),magnitude, (int(Time)+int(delay)),delay,persistance])
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
    global Blacklist
    global News
    global Problem
    global ProblemLength
    global Health

    if variable == 'ProblemTrigger':
        if len(Problem) > 0:
            Health = Health - 1
        Problem = RandomString(ProblemLength)
        BarAdd('ProblemTrigger',1,str(random.randint(ProblemRate[0],ProblemRate[1])),0)
        
    if variable == 'ClearNews':
        News = ''
    if variable == 'Update':
        News = amount
        BarAdd('ClearNews',0,3000,0)
    if variable[0:5] == 'virus':
        n1 = 0
        #print 'aaa'
        for x in range(len(Blacklist)):
            if variable[-1] == Blacklist[n1]:
                del Blacklist[n1]
                #print 'aaa'
                scrub(''.join(['done',str(variable[-1])]))
            n1 = n1 + 1
    if variable is 'CLEAR':
        ProgressBars = []
        Energy = StartingEnergy
        MaxEnergy = StartingMaxEnergy

    
    #UPDATE
    if variable is 'Energy':
        Energy = Energy + int(amount)
    if variable is 'MaxEnergy' and MaxEnergy < MaxEnergyCap:
        MaxEnergy = MaxEnergy + int(amount)
        if MaxEnergy >= MaxEnergyCap:
            BarAdd('Energy', 1, EnergyRate/2)


        
    # LIMITS
    if Energy > MaxEnergy:
        Energy = MaxEnergy

def ColorManager(string):
    global Blacklist
    global ProgressBars
    global Time
    n1 = 0
    n2 = 0
    Return = 'white'
            
    if len(string) == 1:
        for x in range(len(Blacklist)):
            if string == Blacklist[n1]:
                n2 = n2 + 1
            n1 = n1 + 1      
        if n2 > 0:
            Return = 'red'
        else:
            Return = 'white'
    return Return
    
def DrawServers():
    global JitterRate
    global CanvasHeight
    global CanvasWidth
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
            c.create_rectangle((Width+Jitter(JitterRate), Height+Jitter(JitterRate), Width+50+Jitter(JitterRate), Height+50+Jitter(JitterRate)),fill="black",outline=ColorManager(AlphaRelate(n3)),tag=(''.join(['Server',AlphaRelate(n3)])))
            c.create_text((Width+25+Jitter(JitterRate), Height+5+Jitter(JitterRate)),text=(AlphaRelate(n3)), font=('Inhuman BB', 36), fill=ColorManager(AlphaRelate(n3)), justify='center',anchor='n',tag=(''.join(['ServerText',AlphaRelate(n3)])))
            n3 = n3 + 1
            n1 = n1 + 1
    n2 = n2 + 1
    n1 = 1
    for x in range(2):
        Width = CanvasWidth/7.5
        Width = Width * n1
        Height = (CanvasHeight/10) * 5
        c.create_rectangle((Width+Jitter(JitterRate), Height+Jitter(JitterRate), Width+50+Jitter(JitterRate), Height+50+Jitter(JitterRate)),fill="black",outline=ColorManager(AlphaRelate(n3)),tag=(''.join(['Server',AlphaRelate(n3)])))
        c.create_text((Width+25+Jitter(JitterRate), Height+5+Jitter(JitterRate)),text=(AlphaRelate(n3)), font=('Inhuman BB', 36), fill=ColorManager(AlphaRelate(n3)), justify='center',anchor='n',tag=(''.join(['ServerText',AlphaRelate(n3)])))
        n1 = n1 + 5
        n3 = n3 + 1
    n1 = 2
    for x in range(2):
        Width=CanvasWidth/7.5
        Width = Width * n1
        Height = (CanvasHeight/10)*5
        c.create_rectangle((Width+Jitter(JitterRate), Height+Jitter(JitterRate), ((CanvasWidth/7.5)*(n1+1)+50)+Jitter(JitterRate), Height+50+Jitter(JitterRate)),fill="black",outline=ColorManager(AlphaRelate(n3)),tag=(''.join(['Server',AlphaRelate(n3)])))
        c.create_text((((CanvasWidth/7.5)*(n1+0.5)+25)+Jitter(JitterRate), Height+10+Jitter(JitterRate)),text=(AlphaRelate(n3)), font=('Inhuman BB', 24), fill=ColorManager(AlphaRelate(n3)), justify='center',anchor='n',tag=(''.join(['ServerText',AlphaRelate(n3)])))
        n1 = n1 + 2
        n3 = n3 + 1
        
    
def Jitter(Rate):
    pointer = random.randint(1,Rate)
    if pointer == Rate:
        Gitter = random.choice([-1,1])
    else:
        Gitter = 0
    return Gitter
    
def DrawMaster():
    global JitterRate
    global CanvasHeight
    global CanvasWidth
    global Energy
    global MaxEnergy
    global Gitter
    global Prompt
    global News
    global Health
    global StartingHealth
    global Problem
    
    # --- temp ---
    global ProgressBars
    global Time
    n1 = 0
    for x in range(len(ProgressBars)):
        if (ProgressBars[n1])[0] == 'ProblemTrigger':
            print (float(Time)/float((ProgressBars[n1])[2]))
        n1 = n1 + 1
    # --- prototype for problem saturation decay ^ ---
    
    clearCanvas()
    #Draw Servers
    DrawServers()
    #Draw Player
    c.delete('ship')
    c.create_line((int(ShipRoot[0])+Jitter(JitterRate), int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])+Jitter(JitterRate), int(ShipRoot[1])-PlayerSize),fill="red",tag='ship')
    c.create_line((int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])+Jitter(JitterRate), int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+Jitter(JitterRate)),fill="red",tag='ship')
    c.create_oval(((int(ShipRoot[0])-PlayerSize/1.5), (int(ShipRoot[1])-PlayerSize/1.5), (int(ShipRoot[0])+PlayerSize/1.5), (int(ShipRoot[1])+PlayerSize/1.5)),outline='red')
    c.create_text(((int(ShipRoot[0])+Jitter(JitterRate)*50), (int(ShipRoot[1]))+Jitter(JitterRate)*50),fill='red',text=str(AlphaRelate(random.randint(1,26))),font=('Inhuman BB', 12))
    #Draw Text
    c.create_text((((CanvasWidth*0.01)+Jitter(JitterRate)),((CanvasHeight/1.03)+Jitter(JitterRate))),text=(''.join(["Energy: ",str(Energy),'/',str(MaxEnergy)])), font=('Inhuman BB', 24), fill='white', justify='left',anchor='w')
    c.create_text(((CanvasWidth/2)+Jitter(JitterRate/25),(CanvasHeight/1.5)+Jitter(JitterRate/25)),text=str(Prompt),font = ('Inhuman BB', 24), fill='red', justify='center',anchor='n')
    c.create_text(((CanvasWidth/2)+Jitter(JitterRate/25),(CanvasHeight/1.3)+Jitter(JitterRate/25)),text=str(News),font = ('Inhuman BB', 24), fill='white', justify='center',anchor='n')
    c.create_text(((CanvasWidth/2)+Jitter(JitterRate/25),(CanvasHeight/1.15)+Jitter(JitterRate/25)),text=str(Problem),font = ('Inhuman BB', 24), fill='blue', justify='center',anchor='n')
    c.create_text((((CanvasWidth*0.99)+Jitter(JitterRate)),((CanvasHeight/1.03)+Jitter(JitterRate))),text=(''.join(["Health: ",str(Health),'/',str(StartingHealth)])), font=('Inhuman BB', 24), fill='white', justify='right',anchor='e')
            
                   
                                 
# --- Game Commands ---
def scrub(letter):
    global Blacklist
    global ScrubLength
    global Viruses
    if len(letter) == 1:
        Blacklist.append(str(letter))
        BarAdd(''.join(['virus',str(letter)]),1,str(ScrubLength),0)
    else:
        if letter[0:4] == 'done':
            if letter[-1] in Viruses:
                Viruses.remove(letter[-1])
                BarAdd('Update', ''.join(['Virus Found in ', letter[-1], '!']), 10, 0)

                
            
    




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
c.config(cursor="none")

# button with text closing window
b1 = tk.Button(root, text="Close", command=CloseAll, width=int(CanvasWidth/100) )
b1.pack(padx=5, pady=10, side='right')

#Create start/menu button
b2 = tk.Button(root, text="Start", command=StartAll, width=int(CanvasWidth/100) )
b2.pack(padx=5, pady=10, side='left')

#Specific programs to be run once on startup.
TOTAL_MAIN()
'''
winsound.PlaySound(Music,
                  winsound.SND_FILENAME|winsound.SND_ASYNC| winsound.SND_LOOP)
'''

# "start the engine"
root.mainloop()