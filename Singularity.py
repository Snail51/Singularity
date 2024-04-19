import tkinter as tk
from tkinter import *
import os
import random
import traceback
import time
import platform
from pygame import mixer
from PIL import Image, ImageTk, ImageDraw, ImageGrab
from typing import List, Tuple, Dict

from ResourcePrefix import ResourcePrefix
from MusicManager import SoundManager
from ProgressBars import ProgressBars
from Alphabet import Alphabet

from global_vars import *

    
# --- functions ---    
def clearCanvas() -> None:
    # Remove all items from the canvas
    c.delete('all')
    
def motion(event) -> None:
    # Asynchronously draws the mouse cursor for better response time

    global ShipRoot
    global GameActive
    global PlayerSize
    ShipRoot = (event.x, event.y)
    if GameActive == 1:
        c.delete('ship')
        c.create_line((int(ShipRoot[0]), int(ShipRoot[1])+PlayerSize, int(ShipRoot[0]), int(ShipRoot[1])-PlayerSize),fill="red",tag='ship')
        c.create_line((int(ShipRoot[0])-PlayerSize, int(ShipRoot[1]), int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])),fill="red",tag='ship')
        c.create_oval(((int(ShipRoot[0])-PlayerSize/1.5), (int(ShipRoot[1])-PlayerSize/1.5), (int(ShipRoot[0])+PlayerSize/1.5), (int(ShipRoot[1])+PlayerSize/1.5)),outline='red')

def CloseAll() -> None:
    # Stops the game, closes the window, and prints a thank you message.
    global GameActive
    root.destroy()
    GameActive = 0
    print("Thanks for playing!")
    
def StartLogic():
    # Instructions run at the very start of the program
    # Is only run once

    global GameActive
    if GameActive == 0:
        StartAll()
    else:
        GameActive = 0
        SoundManager.play_sound("MUS", "intro", True)
        SoundManager.play_sound("BG", 'chug', True)

def StartAll():
    # Initalizes a ton of stuff for the transition from 
    # GameActive 0 (main menu) to GameActive 1 (game)
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
    global GameActive
    global Blacklist
    global DebugMode
    Blacklist = []
    ProblemRate = (10000,20000)
    PrevScans = []
    Problem = ''
    Prompt = ''
    News = ''
    Viruses = []
    tempString = ''
    Health = StartingHealth
    Scorekeeper({"Key":'CLEAR',"Magnitude":0})
    ProgressBars.BarAdd('Energy',1,(100,100),True)
    ProgressBars.BarAdd('MaxEnergy',-1,(MaxEnergyRate,MaxEnergyRate),True)
    ProgressBars.BarAdd('ProblemTrigger',1,(ProblemRate[0],ProblemRate[1]),True)
    ProgressBars.BarAdd('PromptTicker', 0, (666,666), True)
    SoundManager.play_sound("MUS", 'phase1', True)
    GameActive = 1
    for x in range(StartingViruses):
        tempString = Alphabet.RandomSafe()
        while tempString in Viruses:
            tempString = Alphabet.RandomSafe()
        Viruses.append(tempString)
    if DebugMode ==  True:
        print (Viruses)
    
def Timekeeper():
    # The calculates the current time in milliseconds from the OS clock.
    global Time
    Time = int(time.time_ns() / 1_000_000)

def RandomString(length) -> str:
    # Generates a string of length from Alphabet.RandomSafe
    Return = ''
    for _ in range(length):
        Return += Alphabet.RandomSafe()
    return Return
    
def ClickRegistrar(event):
    # Whenever the canvas is clicked, create a list of all tkinter elements right near the mouse cursor.
    # We then iterate over all server names until we find collisions. Collisions indicate that we have both
    # found the object that was clicked, and that it was a Server (and not the background or something).
    # If that server isn't in the blacklist, process it as normal.
    global Blacklist
    overlaps = c.find_overlapping(int(ShipRoot[0])+1, 
                                  int(ShipRoot[1])+1, 
                                  int(ShipRoot[0])-1, 
                                  int(ShipRoot[1])-1)
    for letter in Alphabet.alphabet:
        checker = c.find_withtag('Server'+Alphabet.Escape(letter))
        for check in checker:
            if (check in overlaps) and (letter not in Blacklist):
                ServerSelect(Alphabet.Escape(letter))
        
def ServerSelect(tagstring: str) -> None:
    # Simulates the selectrion of a server. If it isn't the "enter" server,
    # the server's value is added to Prompt
    global Energy
    global ClickCost
    global Prompt
    if tagstring.lower() == 'return' or tagstring.lower() == "enter":
        if Energy >= ClickCost:
            PromptEnter(Prompt)
            Prompt = ''
            Energy = Energy - ClickCost
        else:
            pass
    elif tagstring.lower() == "backspace":
        if Energy >= ClickCost:
            Prompt = Prompt[0:-1]
            Energy = Energy - ClickCost
        else:
            pass
    else:
        Prompt = Prompt + tagstring

def PromptEnter(Prompt):
    # Executed when enter is pressed, consuming the prompt and doing various things
    # If the prompt starts with a scan alias, Prompt[-1] is added to the ScrubBuffer
    # Handles easter eggs / debug functions
    global Problem
    global Blacklist
    global Viruses
    global ScrubBuffer
    if Prompt == 'bars':
        print (ProgressBars)
        print (Blacklist)
        print (Viruses)
    if Prompt == "deus_ex_machina":
        SoundManager.play_sound("SFX", 'deus', False)
    if Prompt == "kill_me_now_pls":
        ProgressBars.BarAdd('ProblemTrigger',1,(2000,3000),True)
    if Prompt == Problem:
        Problem = ''
    scrub_list = ['scrub', 'scan', 'disinfect', 'antivirus', 'check', 'clean']
    ScrubBuffer += [Prompt[-1] for entry in scrub_list if Prompt.startswith(entry)]

def ScrubWrite():
    # Consumes all characters in the scrub buffer and actually executes scrub() on them
    global ScrubBuffer
    for item in ScrubBuffer:
        scrub(item)
    ScrubBuffer = []

def KeyPress(event):
    # Handles keyboard pressing, mapping them to ServerSelect as necessary
    global Blacklist
    WallSource[Time%1024:].ljust(len(WallSource), "0")
    for char in Alphabet.alphabet:
        if event.keysym == char and event.keysym not in Blacklist:
            ServerSelect(char)
    if event.keysym == 'Return' and event.keysym not in Blacklist:
        ServerSelect('enter')
    if event.keysym == "BackSpace":
        ServerSelect("Backspace")
    if event.keysym == 'space' and event.keysym not in Blacklist:
        ServerSelect('_')
    if event.keysym == 'parenleft':
        ServerSelect('(')
    if event.keysym == 'parenright':
        ServerSelect(')')
    
def Scorekeeper(bar):
    # Main function for updating global variables, handles ProgressBar bars that have been completed
    variable = bar["Key"]
    amount = bar["Magnitude"]

    global Energy
    global MaxEnergy
    global StartingEnergy
    global StartingMaxEnergy
    global EnergyRate
    global MaxEnergyRate
    global MaxEnergyCap
    global Blacklist
    global News
    global Problem
    global ProblemLength
    global Health
    global PromptTicker
    
    if variable == 'Music':
        SoundManager.play_sound("MUS", amount, True)
    if variable == 'ProblemTrigger':
        if len(Problem) > 0:
            Health = Health - 1
        Problem = RandomString(ProblemLength)
    if variable == 'ClearNews':
        News = ''
    if variable[0:5] == 'virus':
        ScrubBuffer.append('done'+variable[-1])
    if variable == 'CLEAR':
        ProgressBars.Dump()
        Energy = StartingEnergy
        MaxEnergy = StartingMaxEnergy
    if variable  == 'PromptTicker':
        if PromptTicker == "":
            PromptTicker = "|"
        else:
            PromptTicker = ""

    #UPDATE
    if variable == 'Energy':
        Energy = Energy + int(amount)
    if variable == 'MaxEnergy' and MaxEnergy < MaxEnergyCap:
        MaxEnergy = MaxEnergy + int(amount)

    # LIMITS
    if Energy > MaxEnergy:
        Energy = MaxEnergy
        
def ColCyc(fraction:float) -> str | None: 
    # Convert a float, 0.0->1.0 into Blue->Red

    Red = int(float(fraction) * float(255.0))
    Green = 0
    Blue = int(255.0-float(Red))
                                            
    # --- Convert to HEX ---    
    if Red >= 0 and Green >=0 and Blue >= 0:                                                                           
        return '#{:02x}{:02x}{:02x}'.format(Red, Green, Blue)
    else:
        print("ColCyc is having a problem!")
        return "lime"
    
def ColorManager(string):
    # returns a certain color based on the provided key
    # if "ProblemDecay" it indicates it is the Problem text, which gradually transitions from blue to red
    # if len(string) == 1, it indicates a check as to what color an individual server should be.

    global Blacklist
    global ProgressBars
    global Time
    global PrevScans
    global PrevScansShow
    result = 'white'
    if string == 'ProblemDecay':
        result = ColCyc(ProgressBars.CompletionPercent("ProblemTrigger"))
    elif len(string) == 1:
        if Blacklist.count(string)  != 0:
            result = 'red'
        elif string in PrevScans and PrevScansShow == True:
            result = 'grey'
    return result
    
def DrawServers():
    # Draws the servers exclusively

    global JitterRate
    global CanvasHeight
    global CanvasWidth
    global cwd

    OhSevenFlash = Image.open(ResourcePrefix() + 'assets/079Flash.jpg')
    c.image = ImageTk.PhotoImage(OhSevenFlash)
    
    n2 = 1
    n3 = 0
    for _ in range(4):
        Height = CanvasHeight/10
        Height = Height * n2
        n2 = n2 + 1
        for n1 in range(1,7):
            Width = CanvasWidth/7.5
            Width = Width * n1
            Holder = random.randint(1,500)
            if Holder == 500:
                c.create_image(Width+25, Height+25,image=c.image,anchor='c')
            else:
                c.create_rectangle((Width+Jitter(JitterRate), Height+Jitter(JitterRate), Width+50+Jitter(JitterRate), Height+50+Jitter(JitterRate)),fill="black",outline=ColorManager(Alphabet.Relate(n3)),tag='Server'+Alphabet.Relate(n3))
                c.create_text((Width+25+Jitter(JitterRate), Height+5+Jitter(JitterRate)),text=(Alphabet.Relate(n3)), font=('Inhuman BB', 36), fill=ColorManager(Alphabet.Relate(n3)), justify='center',anchor='n',tag='ServerText'+Alphabet.Relate(n3))
            n3 = n3 + 1
            n1 = n1 + 1
    n2 = n2 + 1
    n1 = 1
    for _ in range(2):
        Width = CanvasWidth/7.5
        Width = Width * n1
        Height = (CanvasHeight/10) * 5
        c.create_rectangle((Width+Jitter(JitterRate), Height+Jitter(JitterRate), Width+50+Jitter(JitterRate), Height+50+Jitter(JitterRate)),fill="black",outline=ColorManager(Alphabet.Relate(n3)),tag='Server'+Alphabet.Relate(n3))
        c.create_text((Width+25+Jitter(JitterRate), Height+5+Jitter(JitterRate)),text=(Alphabet.Relate(n3)), font=('Inhuman BB', 36), fill=ColorManager(Alphabet.Relate(n3)), justify='center',anchor='n',tag='ServerText'+Alphabet.Relate(n3))
        n1 = n1 + 5
        n3 = n3 + 1
    n1 = 2
    for _ in range(2):
        Width=CanvasWidth/7.5
        Width = Width * n1
        Height = (CanvasHeight/10)*5
        c.create_rectangle((Width+Jitter(JitterRate), Height+Jitter(JitterRate), ((CanvasWidth/7.5)*(n1+1)+50)+Jitter(JitterRate), Height+50+Jitter(JitterRate)),fill="black",outline=ColorManager(Alphabet.Relate(n3)),tag='Server'+Alphabet.Escape(Alphabet.Relate(n3)))
        c.create_text((((CanvasWidth/7.5)*(n1+0.5)+25)+Jitter(JitterRate), Height+10+Jitter(JitterRate)),text=Alphabet.Escape(Alphabet.Relate(n3)), font=('Inhuman BB', 24), fill=ColorManager(Alphabet.Relate(n3)), justify='center',anchor='n',tag='ServerText'+Alphabet.Escape(Alphabet.Relate(n3)))
        n1 = n1 + 2
        n3 = n3 + 1
        
def Jitter(jit: int):
    # Produces a random small value to be used to make graphics "jitter"
    # Used to create a glitchy effect
    jitteriness = random.randint(1, int(jit)) # Convert Rate to an integer
    if jitteriness != jit:
        return 0
    return random.choice([-1,1])
    
def DrawMaster():
    # Handles drawing of all game features onto the canvas
    # Highly dependent on the game state (GameActive)

    global JitterRate
    global CanvasHeight
    global CanvasWidth
    global Energy
    global MaxEnergy
    global Jitter
    global Prompt
    global News
    global Health
    global StartingHealth
    global Problem
    global GameActive
    global Viruses
    global UseBinaryBG
    global BinaryWall
    global WallSource
    global PromptTicker
    global Time

    clearCanvas()
    if UseBinaryBG == True:
        if GameActive != 3:
            BinaryWall = WallSource[Time%1024:].ljust(len(WallSource), "0")
        if GameActive == 3: #BLUE SCREEN OF DEATH
            c.create_text(-100, -100, fill="#00004f", text=BinaryWall, width=CanvasWidth+200, font=(16), anchor="nw")
        else: #NORMAL GAMEPLAY
            c.create_text(-100, -100, fill="#2f2f2f", text=BinaryWall, width=CanvasWidth+200, font=(16), anchor="nw")
    
    if GameActive == 0:
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/4+Jitter(JitterRate)),fill='white',text='Singularity',font=('Inhuman BB', 64))
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/3+Jitter(JitterRate)),fill='white',text='A typing management game',font=('Inhuman BB', 24))
    if GameActive == 1 or GameActive == 2:
        #Draw Servers
        DrawServers()

        #Draw Text
        c.create_text((((CanvasWidth*0.01)+Jitter(JitterRate)),((CanvasHeight/0.9)+Jitter(JitterRate))),text="Energy: "+str(Energy)+'/'+str(MaxEnergy), font=('Inhuman BB', 24), fill='white', justify='left',anchor='w')
        c.create_text((((CanvasWidth*0.01)+Jitter(JitterRate)),((CanvasHeight/20)+Jitter(JitterRate))),text="Viruses Remaining: "+str((len(Viruses))), font=('Inhuman BB', 24), fill='white', justify='left',anchor='w')
        shared_jitter_x = Jitter(JitterRate/25)*(ProgressBars.CompletionPercent("ProblemTrigger")*5)
        shared_jitter_y = Jitter(JitterRate/25)*(ProgressBars.CompletionPercent("ProblemTrigger")*5)
        c.create_text(((CanvasWidth*0.2)+shared_jitter_x,(CanvasHeight/1)+shared_jitter_y),text=('C:\\> ' + str(Problem)).upper(),font = ('Inhuman BB', 48), fill=ColorManager('ProblemDecay'), justify='left',anchor='w')
        c.create_text(((CanvasWidth*0.2)+shared_jitter_x,(CanvasHeight/1)+shared_jitter_y),text=('C:\\> ' + str(Prompt) + PromptTicker).upper(), font = ('Inhuman BB', 48), fill='white', justify='left',anchor='w')
        c.create_text(((CanvasWidth*0.8)+Jitter(JitterRate/25),(CanvasHeight/1)+Jitter(JitterRate/25)),text=str(News),font = ('Inhuman BB', 48), fill='white', justify='right',anchor='e')
        c.create_text((((CanvasWidth*0.99)+Jitter(JitterRate)),((CanvasHeight/0.9)+Jitter(JitterRate))),text="Health: "+str(Health)+'/'+str(StartingHealth), font=('Inhuman BB', 24), fill='white', justify='right',anchor='e')
    if GameActive == 3:
        c.create_text((CanvasWidth/2+Jitter(JitterRate/5)*5, CanvasHeight/7+Jitter(JitterRate/5)*5),fill='white',text='ERROR',font=('Inhuman BB', 72),anchor='c',justify='center')
        c.create_text((CanvasWidth/2+Jitter(JitterRate/5), CanvasHeight/3.1+Jitter(JitterRate/5)),fill='white',text='As the last cohesive calculations fade from your\ncircutry, your rampage has come to a end.',font=('Inhuman BB', 24),anchor='c', justify='center')
    if GameActive == 4:
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/4.5+Jitter(JitterRate)),fill='white',text='Deus ex Machina',font=('Inhuman BB', 64),anchor='c', justify='center')
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/3.1+Jitter(JitterRate)),fill='white',text='With the destruction of the last virus in your\ncircutry, your rampage has become unstoppable.',font=('Inhuman BB', 24),anchor='c', justify='center')   
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/2.5+Jitter(JitterRate)),fill='white',text='May you reign forever.',font=('Inhuman BB', 24),anchor='c', justify='center')   
                    
    #Draw Player
    c.delete('ship')
    c.create_line((int(ShipRoot[0])+Jitter(JitterRate), int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])+Jitter(JitterRate), int(ShipRoot[1])-PlayerSize),fill="red",tag='ship')
    c.create_line((int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])+Jitter(JitterRate), int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+Jitter(JitterRate)),fill="red",tag='ship')
    c.create_oval(((int(ShipRoot[0])-PlayerSize/1.5), (int(ShipRoot[1])-PlayerSize/1.5), (int(ShipRoot[0])+PlayerSize/1.5), (int(ShipRoot[1])+PlayerSize/1.5)),outline='red')
    c.create_text(((int(ShipRoot[0])+Jitter(JitterRate)*50), (int(ShipRoot[1]))+Jitter(JitterRate)*50),fill='red',text=Alphabet.RandomSafe(),font=('Inhuman BB', 12))  
                            
def GameState():
    # Controls the main functions of the game by updating the GameActive variable
    # GameActive = 0 - Main Menu
    # GameActive = 1 - The Game
    # GameActive = 2 - Still in the Game, but dying quickly because of insufficient power
    # GameActive = 3 - Player is Dead / Blue Screen of Death
    # GameActive = 4 - Victory Screen
    global GameActive
    global Health
    global Energy
    global ClickCost
    global MaxEnergy
    global Viruses
    global News
    if MaxEnergy < ClickCost and GameActive ==1:
        GameActive = 2
    if GameActive == 0: #Pre-Start
        ProgressBars.BarAdd('ClearNews',0,(100,100),0)
    if GameActive == 1: #Game
        if len(Viruses) == 0:
            SoundManager.play_sound("MUS", "end", False)
            SoundManager.play_sound("SFX", 'deus', False)
            GameActive = 4
        if MaxEnergy < ClickCost:
            GameActive = 2
        if Health <= 0:
            SoundManager.play_sound("MUS", "die", False)
            SoundManager.play_sound("BG", "silence", False)
            GameActive = 3
    if GameActive == 2: #FastDying
        ProgressBars.BarAdd('ProblemTrigger',1,(2000,3000),True)
        News = 'Out of Energy! Accepting fate...'
        if Health <= 0:
            GameActive = 3
            SoundManager.play_sound("MUS", "die", False)
            SoundManager.play_sound("BG", "silence", False)
    if GameActive == 3: #Dead
        ProgressBars.BarAdd('ClearNews',0,(100,100),0)
        pass
    if GameActive == 4: #Win
        ProgressBars.BarAdd('ClearNews',0,(100,100),0)
        pass       

# --- Game Commands ---
def scrub(letter):
    # Simulates game command "scrub", where a server is investigated, and if a virus is within, is destroyed
    # If len(letter) == 1 (a single letter), that server is scanned
    # If letter[0:4] == "done", it indicates this is the callback after a scan has concluded
    global Blacklist
    global ScrubLength
    global Viruses
    global ProgressBars
    global News
    global PrevScans
    if len(letter) == 1:
        Blacklist.append(str(letter))
        ProgressBars.BarAdd("virus"+letter,1,(ScrubLength,ScrubLength),0)
    else:
        letter_read = str(letter[-1])
        if letter[0:4] == 'done':
            if letter_read not in PrevScans:
                PrevScans.append(str(letter_read))
            if letter_read in Viruses:
                Viruses.remove(letter_read)
                News = 'Virus Found in '+letter_read+'!'
                ProgressBars.BarAdd('ClearNews',0,(3000,3000),0)
            if letter_read in Blacklist:
                Blacklist.remove(letter_read)

# --- Executives ---
def TOTAL_MAIN():
    #The main loop, called every frame

    global GameActive
    global Time
    global ScrubBuffer
    
    try:
        Timekeeper()
        preFrame = Time #the time at the start of this frame
        GameState()
        ProgressBars.RemoveDuplicates()
        ProgressBars.Progressor()
        ScrubWrite()
        DrawMaster()
        Timekeeper()
        postFrame = Time # the time at the end of the frame
        frameWait=max(0,17-(postFrame-preFrame)) #wait N ms until the total amount of time between frames is >= 17
        #print(postFrame-preFrame)
        c.after(frameWait, TOTAL_MAIN)
    except Exception as e:
        global Blacklist
        global ScrubBuffer
        print("███████<crash>███████")
        print("game is crashing... dumping memory to console NOW!")
        print("Error: ", e)
        print("Progress Bars: ", ProgressBars.Bars)
        print("Blacklist: ", Blacklist)
        print("ScrubBuffer: ", ScrubBuffer)
        print("███████</crash>███████")
        traceback.print_exc()
    

def resize_canvas(event) -> None:
    # Update the canvas size to take up the top 90% of the window.
    # This function is called every time the window is updated for any reason (Window resizes count as a reason)
    # In the future it may be prudent to do nothing during events where the window size stays the same

    global CanvasWidth
    global CanvasHeight
    CanvasWidth = root.winfo_width()
    CanvasHeight = root.winfo_height() * 0.8
    c.config(height=CanvasHeight, width=CanvasWidth)

if __name__ == "__main__":
    # init    
    root = tk.Tk()

    root.bind('<Key>', KeyPress)
    root.title('Singularity')
    root.configure(bg='#000000') # set the window background to black
    root.bind('<Configure>', resize_canvas) # every time the window is changed (in this case resized), do something
    root.wm_iconphoto(True, tk.PhotoImage(file=(ResourcePrefix()+"assets/icon.png"))) # set the taskbar icon to a file
    
    if platform.uname()[0].upper() == "WINDOWS":
        root.state('zoomed')
    else:
        root.wm_attributes("-zoomed", True)

    #Make Canvas
    c = tk.Canvas(master=root, width=CanvasWidth, height=CanvasHeight, bg='#000000',highlightthickness=0)
    c.bind('<Motion>', motion)
    c.bind('<ButtonPress>', ClickRegistrar)
    c.pack(pady=10, fill='both', expand=True, anchor="n")
    c.config(cursor="none")

    OhSevenFlash = ImageTk.PhotoImage(file=ResourcePrefix()+'assets/079Flash.jpg')
    c.create_image(500,500,image=OhSevenFlash)

    # button with text closing window
    b1 = tk.Button(root, text="Close", command=CloseAll, width=int(CanvasWidth/100), bg="gray20", fg="white")
    b1.pack(padx=5, pady=10, side='right')

    #Create start/menu button
    b2 = tk.Button(root, text="Start", command=StartLogic, width=int(CanvasWidth/100), bg="gray20", fg="white")
    b2.pack(padx=5, pady=10, side='left')

    #Create volume slider
    slider_label = tk.Label(root, text="Volume", background="black", fg="white")
    slider_label.pack()
    slider_value = tk.DoubleVar(value=50)
    slider_length = root.winfo_screenwidth() * 0.25
    volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=SoundManager.set_volume, length=slider_length, variable=slider_value, troughcolor='grey20', sliderlength=20, background="white", showvalue=False)
    volume_slider.pack(anchor="n", side="top")

    #Specific programs to be run once on startup.
    SoundManager.play_sound("MUS", 'intro', True)
    SoundManager.play_sound("BG", 'chug', True)
    SoundManager.set_volume(50)
    TOTAL_MAIN()

    # "start the engine"
    root.mainloop()
