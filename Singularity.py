import tkinter as tk
import subprocess
import os
import time
import random
import winsound
import math
import datetime
from tkinter import *

from PIL import Image, ImageTk, ImageDraw, ImageGrab

# --- Config ---
StartingEnergy = 0 # >=0
StartingMaxEnergy = 100
ClickCost = 25 # <= StartingMaxEnergy
PlayerSize = 20
EnergyRate = 100
MaxEnergyRate = 5000
MaxEnergyCap = 200
JitterRate = 200
ScrubLength = 5000
StartingViruses = 5 # <= 26
StartingProblemRate = (10000,20000)
ProblemLength = 6
StartingHealth = 10
CanvasWidth = 1000
CanvasHeight = 700
BinaryBG = True
ProblemType = "String" # Prompts or String
DebugMode = False
PrevScansShow = False


# --- variables ---
cwd = os.path.join(os.path.dirname(__file__))
print(cwd)
PromptReference = ''.join([cwd,'/SingularityPrompts.txt'])
ShipRoot = (0,0)
Energy = 0
MaxEnergy = 100
ProblemRate = (0,0)
ProgressBars = [] #Name, inc/dec amount, time when next tick
Time = 0
Jitter = (0,0)
Prompt = 'aaa'
Blacklist = []
Viruses = []
News = 'bbb'
Problem = 'ccc'
Health = 0
ScrubBuffer = []
GameActive = 0
SimpleDict = []
Prompts = []
Dictionary = []
PrevScans = []



# --- Media ---
NowPlaying = ''
Intro = ''.join([cwd,'/machine_intro.wav'])
Music = ''.join([cwd,'/machine_music.wav'])
QED = ''.join([cwd,'/machine_end.wav'])








def DictRead():
    """
    The function DictRead reads data from a file, converts it into a dictionary, and stores prompts in a
    list.
    """
    #Open and convert
    global Dictionary
    global SimpleDict
    global Prompts
    global PromptReference
    Prompts = []
    Dictionary = []
    DictRead = []
    DictDAT = ''
    SimpleDict = []
    n1 = 0
    print('Reading Data...')
    try:
        myFile = open(PromptReference, 'r')
        DictDAT = myFile.read()
        #print HighDAT
        DictRead = (DictDAT.split('\n')) 
        #print DictRead
        myFile.close()
        Dictionary = DictRead
        #print Dictionary
        for x in range(len(Dictionary)):
            Prompts.append((Dictionary[n1]).lower())
            n1 = n1 + 1
        del Prompts[0]
    except:
        pass
    print(Prompts)




# --- functions ---    
def clearCanvas():
    """
    The `clearCanvas` function in Python clears all items from a canvas.
    """
    c.delete('all')
    
def motion(event):
    """
    The `motion` function updates the position of a ship on a canvas based on user input.
    @param event - The `event` parameter in the `motion` function is typically an event object that
    contains information about the event that triggered the function. In this case, it seems like the
    function is handling mouse motion events, as it is using `event.x` and `event.y` to get the
    coordinates of
    """
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
    """
    The CloseAll function stops the game, closes the window, and prints a thank you message.
    """
    global GameActive
    winsound.PlaySound(None, 0)
    root.destroy()
    GameActive = 0
    print("Thanks for playing!")
    
def StartLogic():
    """
    The function `StartLogic` checks if the game is active and either starts all components or sets
    `GameActive` to 0 and plays the intro music.
    """
    global GameActive
    if GameActive == 0:
        StartAll()
    else:
        GameActive = 0
        MusicManager('Intro')

def StartAll():
    """
    The `StartAll` function initializes various global variables and sets up the game environment,
    including creating a list of viruses and adding progress bars.
    """
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
    global ProgressBars
    global Blacklist
    global StartingProblemRate
    global DebugMode
    Blacklist = []
    ProblemRate = StartingProblemRate
    ProgressBars = []
    PrevScans = []
    Problem = ''
    Prompt = ''
    News = ''
    Viruses = []
    tempString = ''
    Health = StartingHealth
    Scorekeeper('CLEAR',0)
    BarAdd('Energy',1,str(EnergyRate),1) #Title, Magnitude,Tick Delay, Persistance.
    BarAdd('MaxEnergy',-1,str(MaxEnergyRate),1)
    BarAdd('ProblemTrigger',1,str(random.randint(ProblemRate[0],ProblemRate[1])),1)
    MusicManager('Music')
    GameActive = 1
    for x in range(StartingViruses):
        tempString = AlphaRelate(random.randint(1,26))
        while tempString in Viruses:
            #print (tempString in Viruses,tempString,Viruses)
            tempString = AlphaRelate(random.randint(1,26))
        Viruses.append(tempString)
    if DebugMode ==  True:
        print (Viruses)
    


def Timekeeper():
    """
    The `Timekeeper` function calculates the current time in milliseconds.
    """
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
    """
    The function `AlphaRelate` takes an integer input and returns the corresponding lowercase letter or
    special character based on the input value.
    @param Int - It looks like the code you provided is a function called `AlphaRelate` that takes an
    integer input and returns a corresponding letter or symbol based on the input value. The function
    maps integers to lowercase letters from 'a' to 'z', as well as to the underscore character '_', the
    'Enter
    @returns The function `AlphaRelate` takes an integer input and returns a corresponding letter or
    symbol based on the input. If the input is between 1 and 26, it returns the corresponding lowercase
    letter of the alphabet. If the input is 27, it returns an underscore "_". If the input is 28, it
    returns "Enter". For any other input, it returns "NULL". The
    """
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
    """
    The function `RandomString` generates a random string of a specified length using a set of prompts
    or random alphabets if no prompts are provided.
    @param length - The `length` parameter in the `RandomString` function represents the desired length
    of the random string that will be generated.
    @returns The function `RandomString` returns a randomly generated string of a specified length. If
    the global variable `Prompts` has elements, it selects a random element from `Prompts` as the return
    value. If `Prompts` is empty, it generates a random string of the specified length using characters
    related to the alphabet.
    """
    global Prompts
    Return = ''
    if len(Prompts) > 0:
        Return = str(random.choice(Prompts))
    else:
        for x in range(length):
            Return = ''.join([Return,str(AlphaRelate(random.randint(1,26)))])
    return Return
    

def ClickRegistrar(event):
    """
    This function checks for overlaps between a player's ship and certain server objects, and calls a
    function to select a server if there is an overlap.
    @param event - The function `ClickRegistrar` seems to be handling mouse click events in a graphical
    user interface. The `event` parameter in this function typically represents the event object that
    triggered the function, such as a mouse click event.
    """
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
    """
    The function `ServerSelect` checks if a given tag string is 'ENTER' and deducts energy if conditions
    are met, otherwise it appends the tag string to the `Prompt` variable.
    @param tagstring - It looks like the `ServerSelect` function takes a parameter called `tagstring`.
    This parameter is used to determine whether the user wants to enter a value or not. If the
    `tagstring` is 'ENTER', the function will check if there is enough energy to perform the action and
    then call
    """
    global Energy
    global ClickCost
    global Prompt
    
    if (str(tagstring).upper()) == 'ENTER':
        if Energy >= ClickCost:
                PromptEnter(Prompt)
                Prompt = ''
                Energy = Energy - ClickCost
    else:
        Prompt = ''.join([str(Prompt),str(tagstring)])
        #print Prompt

def PromptEnter(Prompt):
    """
    The function `PromptEnter` takes a prompt as input and performs various actions based on the prompt,
    such as displaying progress bars, managing music, and scrubbing data for specific keywords.
    @param Prompt - It looks like the `PromptEnter` function takes a `Prompt` parameter, which is used
    to perform different actions based on its value. The function checks the value of `Prompt` and
    executes specific tasks accordingly.
    """
    #print Prompt
    global ProgressBars
    global Problem
    global Blacklist
    global Viruses
    n1 = 0
    if Prompt == 'bars':
        print (ProgressBars)
        print (Blacklist)
        print (Viruses)
    if Prompt == "deus_ex_machina":
        MusicManager('QED')
    if Prompt == Problem:
        Problem = ''
    scrub_list = ['scrub', 'scan', 'disinfect', 'antivirus', 'check', 'clean']
    for x in range(len(scrub_list)):
        if scrub_list[n1] in Prompt:
            ScrubHolder(Prompt[-1])
        n1 = n1 + 1

def ScrubHolder(add):
    """
    The function `ScrubHolder` appends the input parameter `add` to a global list `ScrubBuffer`.
    @param add - The `add` parameter in the `ScrubHolder` function is the value that will be added to
    the `ScrubBuffer` list.
    """
    global ScrubBuffer
    ScrubBuffer.append(add)
    
def ScrubWrite():
    """
    The `ScrubWrite` function iterates over elements in `ScrubBuffer`, applies the `scrub` function to
    each element, and then clears `ScrubBuffer`.
    """
    global ScrubBuffer
    n1 = 0
    for x in range(len(ScrubBuffer)):
        scrub(ScrubBuffer[n1])
        n1 = n1 + 1
    ScrubBuffer = []
 
def BarSieve():
    """
    The function `BarSieve` iterates through `ProgressBars` to filter out duplicate entries and add
    specific bars if they are not already present.
    """
    global ProgressBars
    global GameActive
    n1 = 0
    Sieve = []
    for x in range(len(ProgressBars)):
        if ((ProgressBars[n1])[0]) not in Sieve:    
            Sieve.append((ProgressBars[n1])[0])
        elif ((ProgressBars[n1])[0]) in Sieve:
            del ProgressBars[n1]
            n1 = n1 - 1
        n1 = n1 + 1
        #print Sieve
    if GameActive == 1 or GameActive == 2:          
        if 'Energy' not in Sieve:
            BarAdd('Energy',1,str(EnergyRate),1)
        if 'MaxEnergy' not in Sieve:
            BarAdd('MaxEnergy',1,str(MaxEnergyRate),1)
        if 'ProblemTrigger' not in Sieve:
            BarAdd('ProblemTrigger',1,str(random.randint(ProblemRate[0],ProblemRate[1])),1)  
          
                  
def Progressor():
    """
    The `Progressor` function iterates through `ProgressBars`, updates progress based on time, and
    adjusts progress bars based on certain conditions.
    """
    global ProblemRate
    global ProgressBars
    global Time
    n2 = 0 #Search Pointer
    #print Time
    #print ProgressBars
    n3 = 0
    for x in range(len(ProgressBars)):
        if (ProgressBars[n2])[2] < Time:
            #print len(ProgressBars)
            #print ((ProgressBars[n2])[2])
            #print (str((ProgressBars[n2])[0]),((ProgressBars[n2])[1]))
            '''
            if ((ProgressBars[n2])[0])[0:6] == 'Music':
                print ('progressor',ProgressBars[n2])
            '''
            Scorekeeper(str((ProgressBars[n2])[0]),((ProgressBars[n2])[1]))
            

            OldTitle = str((ProgressBars[n2])[0])
            Mag = str((ProgressBars[n2])[1])
            OldTick = int((ProgressBars[n2])[2])
            OldDelay = int((ProgressBars[n2])[3])
            Persistance = int((ProgressBars[n2])[4])
            if Persistance == 1:
                if OldTitle == 'ProblemTrigger':
                    OldDelay = ProblemRate[0]
                ProgressBars[n2] = (OldTitle,Mag,OldTick+OldDelay, OldDelay, Persistance)
            if Persistance == 0:
                if Mag == 'Deus':
                    OldDelay = 2751
                    ProgressBars[n2] = (OldTitle,'Music',OldTick+OldDelay, OldDelay, Persistance)
                else:
                    del ProgressBars[n2]
                    n2 = n2 -1
                
            #print ProgressBars    
        n2 = n2 + 1
  

def BarAdd(string, magnitude, delay, persistance): #Create a new progress bar
    """
    The function `BarAdd` creates a new progress bar and manages its properties in a list called
    `ProgressBars`.
    @param string - The `string` parameter in the `BarAdd` function is used to specify the name or
    identifier of the progress bar being created or updated.
    @param magnitude - The `magnitude` parameter in the `BarAdd` function represents the size or scale
    of the progress bar that you want to create. It could be the total number of steps or units that the
    progress bar will represent. This value helps determine the overall length or completion of the
    progress bar as it advances
    @param delay - The `delay` parameter in the `BarAdd` function represents the amount of time (in
    seconds) to wait before displaying the progress bar. It is used to introduce a delay before showing
    the progress of a particular task.
    @param persistance - The `persistance` parameter in the `BarAdd` function seems to be used to
    determine how long the progress bar should persist or remain visible. It likely specifies the
    duration for which the progress bar should be displayed before it disappears or completes.
    """
    global ProgressBars
    global Time 
    n1 = 0
    n2 = 0
    #print [str(string),magnitude, (int(Time)+int(delay)),delay,persistance]
    for x in range(len(ProgressBars)):
        #print len(ProgressBars)
        if (ProgressBars[n1])[0] == string:
            del ProgressBars[n1]
            n2 = 1
            ProgressBars.insert(0,(str(string),magnitude, (int(Time)+int(delay)),delay,persistance))
        n1 = n1 + 1
    if n2 == 0:
        ProgressBars.insert(0,(str(string),magnitude, (int(Time)+int(delay)),delay,persistance))
    #print ProgressBars

def MusicManager(File):
    """
    The function `MusicManager` plays different sound files based on the input `File` and manages the
    currently playing sound.
    @param File - It looks like the `MusicManager` function is designed to manage playing different
    types of music files based on the input `File`. The function uses the `winsound` module to play the
    music files asynchronously.
    """
    global Music
    global QED
    global NowPlaying
    global ProgressBars
    global Time

    if File == "Intro" and NowPlaying != 'Intro':
        winsound.PlaySound(Intro,
                    winsound.SND_FILENAME|winsound.SND_ASYNC| winsound.SND_LOOP)
        NowPlaying = "Intro"
    if File == 'Music' and NowPlaying != 'Music':
        winsound.PlaySound(Music,
                    winsound.SND_FILENAME|winsound.SND_ASYNC| winsound.SND_LOOP)
        NowPlaying = 'Music'
    if File == 'QED' and NowPlaying != "QED":
        winsound.PlaySound(QED,
                    winsound.SND_FILENAME|winsound.SND_ASYNC)
        NowPlaying = 'QED'


def KeyPress(event):
    """
    The function `KeyPress` handles key press events in Python, checking for specific key presses and
    calling the `ServerSelect` function accordingly.
    @param event - The `event` parameter in the `KeyPress` function is used to capture the key press
    event that occurs when a key is pressed on the keyboard. The function then checks the `keysym`
    attribute of the event to determine which key was pressed. The function then performs certain
    actions based on the key
    """
    #print event.keysym
    global Blacklist
    #print (int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])-PlayerSize)
    n1 = 1
    for x in range(26):
        if event.keysym == AlphaRelate(n1) and event.keysym not in Blacklist:
            ServerSelect(AlphaRelate(n1))
        n1 = n1 + 1
    if event.keysym == 'Return' and event.keysym not in Blacklist:
        ServerSelect('Enter')
    if event.keysym == 'space' and event.keysym not in Blacklist:
        ServerSelect('_')
    if event.keysym == 'parenleft':
        ServerSelect('(')
    if event.keysym == 'parenright':
        ServerSelect(')')
    
def Scorekeeper(variable,amount):
    """
    The function `Scorekeeper` in Python manages various game variables and conditions based on the
    input variable and amount provided.
    @param variable - The `variable` parameter in the `Scorekeeper` function is used to determine the
    action to be taken based on its value. It is a string that specifies the type of operation or action
    to be performed within the function. The function contains conditional statements that check the
    value of the `variable` parameter
    @param amount - The `amount` parameter in the `Scorekeeper` function represents the value by which a
    certain variable will be updated. Depending on the `variable` parameter passed to the function, the
    `amount` will be used to update different aspects of the game state such as Energy, MaxEnergy,
    ProgressBars
    """
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
    
    if variable == 'Music':
        print  (ProgressBars, variable, amount)
        MusicManager(amount)


    if variable == 'ProblemTrigger':
        if len(Problem) > 0:
            Health = Health - 1
        Problem = RandomString(ProblemLength)
        #print "aaa"
        
    if variable == 'ClearNews':
        News = ''

        
    if variable[0:5] == 'virus':
        #print(''.join(['done',str(variable[-1])]))
        ScrubHolder(''.join(['done',str(variable[-1])]))

    if variable == 'CLEAR':
        ProgressBars = []
        Energy = StartingEnergy
        MaxEnergy = StartingMaxEnergy

    
    #UPDATE
    if variable == 'Energy':
        Energy = Energy + int(amount)
    if variable == 'MaxEnergy' and MaxEnergy < MaxEnergyCap:
        MaxEnergy = MaxEnergy + int(amount)
        if MaxEnergy >= MaxEnergyCap:
            BarAdd('Energy', 1, EnergyRate/2)


        
    # LIMITS
    if Energy > MaxEnergy:
        Energy = MaxEnergy
        
    
def MiscDecay():
    """
    The function `MiscDecay` calculates and returns an output value based on the progress bars, time,
    and game activity status.
    @returns The function `MiscDecay` returns the calculated `Output` value.
    """
    global ProgressBars
    global Time
    global GameActive
    n1 = 0
    EventTime = 0
    Delay = 0
    Output = 1.0
    if GameActive == 1:
        for x in range(len(ProgressBars)):
            if str((ProgressBars[n1])[0]) == 'ProblemTrigger':
                EventTime = int((ProgressBars[n1])[2])
                Delay = int((ProgressBars[n1])[3])
            n1 = n1 + 1
        Output = float((float(EventTime)-float(Time))/float(Delay))
        #print Output
        Output = (Output*-1.0) + 1.0
        Output = Output * 5
    return Output
        


def ColCyc(EventTime,Delay): 
    """
    This Python function calculates a color value based on the input event time and delay, and returns
    the color in hexadecimal format.
    @param EventTime - EventTime is the time of the event that you want to calculate the color for. It
    is a numerical value representing the time of the event.
    @param Delay - The `Delay` parameter in the `ColCyc` function represents the time delay between
    events. It is used to calculate the color output based on the difference between the current event
    time and the previous event time.
    @returns The function `ColCyc(EventTime, Delay)` is returning a hexadecimal color code based on the
    input parameters `EventTime` and `Delay`. The color code is calculated based on the difference
    between `EventTime` and a global variable `Time`, and then converted to a hexadecimal format
    representing a color. The function returns the final hexadecimal color code as a string.
    """
    global Time
    #print (Time, EventTime,Delay)

    Output = float((float(EventTime)-float(Time))/float(Delay))
    #print Output
    Output = (Output*-1.0) + 1.0
    #print Output
    
    Red = int(float(Output) * float(255.0))
    Green = 0
    Blue = int(255.0-float(Red))
    #print (Red,Green,Blue)
                                            
    # --- Convert to HEX ---    
    if Red >= 0 and Green >=0 and Blue >= 0:                                                                           
        MR = ""
        MG = ""
        MB = ""
        MR = "{0:x}".format(Red)
        if len(MR) == 1:
            MR = ''.join(['0',MR])
        MG = "{0:x}".format(Green)
        if len(MG) == 1:
            MG = ''.join(['0',MG])
        MB = "{0:x}".format(Blue)
        if len(MB) == 1:
            MB = ''.join(['0',MB])
        Master = ''.join(['#',MR, MG, MB])
        return Master
    
def ColorManager(string):
    """
    The ColorManager function in Python determines the color to be displayed based on input strings and
    global variables.
    @param string - The `ColorManager` function takes a string as input and returns a color based on
    certain conditions. The function checks the input string against the `Blacklist` and `PrevScans`
    lists, as well as the `ProgressBars` list to determine the color to return.
    @returns The ColorManager function returns the color value based on the input string. The color
    value is determined by the conditions specified in the function, such as checking if the input
    string matches any items in the Blacklist, or if it is a specific string like 'ProblemDecay'. The
    final color value is stored in the variable 'Return' and is returned at the end of the function.
    """
    global Blacklist
    global ProgressBars
    global Time
    global PrevScans
    global PrevScansShow
    n1 = 0
    n2 = 0
    Return = 'white'
    if string == 'ProblemDecay':
        n1 = 0
        for x in range(len(ProgressBars)):
            if (ProgressBars[n1])[0] == 'ProblemTrigger':
                Return = ColCyc(((ProgressBars[n1])[2]),((ProgressBars[n1])[3]))
            n1 = n1 + 1       
    n1 = 0       
    if len(string) == 1:
        for x in range(len(Blacklist)):
            if string == Blacklist[n1]:
                n2 = n2 + 1
            n1 = n1 + 1      
        if n2 > 0:
            Return = 'red'
        else:
            if string in PrevScans and PrevScansShow == True:
                Return = 'grey'
            else:
                Return = 'white'
    return Return
    
def DrawServers():
    """
    The `DrawServers` function in Python creates a visual representation of servers on a canvas with
    specified dimensions, using images and rectangles with text labels.
    """
    global JitterRate
    global CanvasHeight
    global CanvasWidth
    global cwd
    OhSevenFlash = Image.open((''.join([cwd,'\\','079Flash.jpg'])))
    c.image = ImageTk.PhotoImage(OhSevenFlash)
    
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
            Holder = random.randint(1,500)
            if Holder == 500:
                c.create_image(Width+25, Height+25,image=c.image,anchor='c')
            else:
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
    """
    The function `Jitter` generates a random jitter value based on a given rate.
    @param Rate - The `Rate` parameter in the `Jitter` function represents the frequency at which the
    jitter occurs. The function generates a random number between 1 and the integer value of `Rate`. If
    the generated number is equal to `Rate`, it assigns a random choice of either -1 or 1
    @returns The function `Jitter` returns either -1, 1, or 0 based on the conditions inside the
    function.
    """
    pointer = random.randint(1, int(Rate)) # Convert Rate to an integer
    if pointer == Rate:
        Jitter = random.choice([-1,1])
    else:
        Jitter = 0
    return Jitter
    
def DrawMaster():
    """
    The `DrawMaster` function in Python is responsible for drawing various elements on the canvas based
    on the current state of the game, including text, player ship, servers, and background.
    """
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
    global BinaryBG
    global WallTemp


    clearCanvas()
    if BinaryBG == True:
        if GameActive != 3:
            WallTemp = ""
            for x in range(6000):
                WallTemp = ''.join([WallTemp,(random.choice(["0","1"]))])
        if GameActive == 3:
            c.create_text(CanvasWidth/2+Jitter(JitterRate/50)*5,CanvasHeight/2+Jitter(JitterRate/50)*5,fill="#00004f",text=WallTemp, width=CanvasWidth,font=(16))
        else:
            c.create_text(CanvasWidth/2,CanvasHeight/2,fill="#2f2f2f",text=WallTemp, width=CanvasWidth,font=(16))
    
    
        
    if GameActive == 0:
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/4+Jitter(JitterRate)),fill='white',text='Singularity',font=('Inhuman BB', 64))
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/3.25+Jitter(JitterRate)),fill='white',text='A typing management game',font=('Inhuman BB', 24))
    if GameActive == 1 or GameActive == 2:
        #Draw Servers
        DrawServers()
        
        #Draw Text
        c.create_text((((CanvasWidth*0.01)+Jitter(JitterRate)),((CanvasHeight/1.03)+Jitter(JitterRate))),text=(''.join(["Energy: ",str(Energy),'/',str(MaxEnergy)])), font=('Inhuman BB', 24), fill='white', justify='left',anchor='w')
        c.create_text((((CanvasWidth*0.01)+Jitter(JitterRate)),((CanvasHeight/20)+Jitter(JitterRate))),text=(''.join(["Viruses Remaining: ",str((len(Viruses)))])), font=('Inhuman BB', 24), fill='white', justify='left',anchor='w')
        c.create_text(((CanvasWidth/2)+Jitter(JitterRate/25),(CanvasHeight/1.65)+Jitter(JitterRate/25)),text=str(Prompt),font = ('Inhuman BB', 48), fill='red', justify='center',anchor='n')
        c.create_text(((CanvasWidth/2)+Jitter(JitterRate/25),(CanvasHeight/1.35)+Jitter(JitterRate/25)),text=str(News),font = ('Inhuman BB', 48), fill='white', justify='center',anchor='n')
        c.create_text(((CanvasWidth/2)+Jitter(JitterRate/25)*MiscDecay(),(CanvasHeight/1.15)+Jitter(JitterRate/25)*MiscDecay()),text=str(Problem),font = ('Inhuman BB', 48), fill=ColorManager('ProblemDecay'), justify='center',anchor='n')
        c.create_text((((CanvasWidth*0.99)+Jitter(JitterRate)),((CanvasHeight/1.03)+Jitter(JitterRate))),text=(''.join(["Health: ",str(Health),'/',str(StartingHealth)])), font=('Inhuman BB', 24), fill='white', justify='right',anchor='e')
    if GameActive == 3:
        c.create_text((CanvasWidth/2+Jitter(JitterRate/5)*5, CanvasHeight/7+Jitter(JitterRate/5)*5),fill='white',text='ERROR',font=('Inhuman BB', 72),anchor='n',justify='center')
        c.create_text((CanvasWidth/2+Jitter(JitterRate/5), CanvasHeight/3.1+Jitter(JitterRate/5)),fill='white',text='As the last cohesive calculations fade from your\ncircutry, your rampage has come to a end.',font=('Inhuman BB', 24),anchor='n', justify='center')
    if GameActive == 4:
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/4+Jitter(JitterRate)),fill='white',text='Deus ex Machina',font=('Inhuman BB', 64))
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/3.1+Jitter(JitterRate)),fill='white',text='With the destruction of the last virus in your\ncircutry, your rampage has become unstoppable.',font=('Inhuman BB', 24),anchor='n', justify='center')   
        c.create_text((CanvasWidth/2+Jitter(JitterRate), CanvasHeight/2.5+Jitter(JitterRate)),fill='white',text='May you reign forever.',font=('Inhuman BB', 24),anchor='n', justify='center')   
                    
    #Draw Player
    c.delete('ship')
    c.create_line((int(ShipRoot[0])+Jitter(JitterRate), int(ShipRoot[1])+PlayerSize, int(ShipRoot[0])+Jitter(JitterRate), int(ShipRoot[1])-PlayerSize),fill="red",tag='ship')
    c.create_line((int(ShipRoot[0])-PlayerSize, int(ShipRoot[1])+Jitter(JitterRate), int(ShipRoot[0])+PlayerSize, int(ShipRoot[1])+Jitter(JitterRate)),fill="red",tag='ship')
    c.create_oval(((int(ShipRoot[0])-PlayerSize/1.5), (int(ShipRoot[1])-PlayerSize/1.5), (int(ShipRoot[0])+PlayerSize/1.5), (int(ShipRoot[1])+PlayerSize/1.5)),outline='red')
    c.create_text(((int(ShipRoot[0])+Jitter(JitterRate)*50), (int(ShipRoot[1]))+Jitter(JitterRate)*50),fill='red',text=str(AlphaRelate(random.randint(1,26))),font=('Inhuman BB', 12))  
                  
                      
def GameState():
    """
    The `GameState` function manages the game state based on various conditions such as energy levels,
    health status, and the presence of viruses.
    """
    #print GameActive
    global GameActive
    global Health
    global Energy
    global ClickCost
    global ProblemRate
    global MaxEnergy
    global Viruses
    if MaxEnergy < ClickCost and GameActive ==1:
        GameActive = 2
    if GameActive == 0: #Pre-Start
        pass
    if GameActive == 1: #Game

        if len(Viruses) == 0:
            MusicManager("QED")
            GameActive = 4
        if MaxEnergy < ClickCost:
            GameActive = 2
            ProblemRate = (1000,2000)
        if Health <= 0:
            MusicManager("QED")
            GameActive = 3
    if GameActive == 2: #FastDying
        ProblemRate = (1000,2000)
        if Health <= 0:
            GameActive = 3
    if GameActive == 3: #Dead
        pass
    if GameActive == 4: #Win
        pass                    
# --- Game Commands ---
def scrub(letter):
    """
    The `scrub` function in Python manages a list of blacklisted items, viruses, progress bars, news
    updates, and previous scans, with the ability to add or remove items based on input letters.
    @param letter - The `scrub` function seems to be a part of a larger program that deals with scanning
    and removing viruses. The function takes a parameter `letter`, which is used to update various
    global variables like `Blacklist`, `ScrubLength`, `Viruses`, `ProgressBars`, `News`,
    """
    global Blacklist
    global ScrubLength
    global Viruses
    global ProgressBars
    global News
    global PrevScans
    #print ('aaa',letter,Blacklist,Viruses)
    if len(letter) == 1:
        Blacklist.append(str(letter))
        BarAdd(''.join(['virus',str(letter)]),1,int(ScrubLength),0)
    else:
        #print (letter,'letter')
        letter_read = str(letter[-1])
        if letter[0:4] == 'done':
            #print (Blacklist,'blacklist')
            #print (letter_read, 'letterred')
            if letter_read not in PrevScans:
                PrevScans.append(str(letter_read))
                #print PrevScans
            if letter_read in Viruses:
                Viruses.remove(letter_read)
                News = ''.join(['Virus Found in ', letter_read, '!'])
                BarAdd('ClearNews',0,3000,0)
            if letter_read in Blacklist:
                Blacklist.remove(letter_read)

    #print ('bbb',letter,Blacklist,Viruses)

                
            
    




# --- Executives ---
def TOTAL_MAIN():
    """
    The TOTAL_MAIN function in Python contains global variables and calls multiple other functions in a
    loop using the c.after method.
    """
    global GameActive
    global Time
    GameState()
    Timekeeper()
    BarSieve()
    Progressor()
    ScrubWrite()
    DrawMaster()
    c.after(1, TOTAL_MAIN)



# init    
root = tk.Tk()

root.bind('<Key>', KeyPress)
root.title('Singularity')
root.configure(bg='#000000')

#Make Canvas
c = tk.Canvas(master=root, width=CanvasWidth, height=CanvasHeight, bg='#000000',highlightthickness=0)
c.bind('<Motion>', motion)
c.bind('<ButtonPress>', ClickRegistrar)
c.pack(pady=10)
c.config(cursor="none")

OhSevenFlash = ImageTk.PhotoImage(file=(''.join([cwd,'\\','079Flash.jpg'])))
c.create_image(500,500,image=OhSevenFlash)

# button with text closing window
b1 = tk.Button(root, text="Close", command=CloseAll, width=int(CanvasWidth/100) )
b1.pack(padx=5, pady=10, side='right')

#Create start/menu button
b2 = tk.Button(root, text="Start", command=StartLogic, width=int(CanvasWidth/100) )
b2.pack(padx=5, pady=10, side='left')



#Specific programs to be run once on startup.
MusicManager('Intro')
TOTAL_MAIN()




# "start the engine"
root.mainloop()
