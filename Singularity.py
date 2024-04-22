import tkinter as tk
from tkinter import font
from tkinter import *
import os
import subprocess
import shutil
import ctypes
import random
import traceback
import time
import platform
import threading
from pygame import mixer
from PIL import Image, ImageTk, ImageDraw, ImageGrab
from typing import List, Tuple, Dict

# --- variables ---
cwd = os.path.join(os.path.dirname(__file__))
print(cwd)
ShipRoot: Tuple = (0,0)
Energy = 0 # How much energy the user currently has. Increases over time. Is consumed by certain actions.
ProblemRate = (10000,20000) # how long between problems (ms)
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
PromptTicker = ""
WallSource = ''.join(format(byte, '08b') for byte in os.urandom(1500))
BinaryWall = ""

# --- tkinter instances ---
root = tk.Tk()
c = tk.Canvas(master=root, bg='#000000', highlightthickness=0)

def ResourcePrefix() -> str:
    """
    The function `ResourcePrefix` returns specific resource path prefixes based on if the game
    is in a dev or built state.
    @returns The function `ResourcePrefix()` is returning a string value. The returned value depends on
    whether the directory `_internal` exists. If the directory `_internal` exists, the function will
    return `"_internal/assets/"`, otherwise it will return `"assets/"`.
    """
    if os.path.isdir('_internal'):
        return "_internal/"
    else:
        return ""
    
class Configurator:
    def loadFromFile():
        with open("Singularity.cfg", "r") as file:
            for line in file:
                # Remove any leading/trailing whitespace
                line = line.strip()
                line = line.replace(":", ",")
                line = line.replace(" ", ",")
                line = line.replace("=", ",")
                print(line)
                
                # Split the line into key, type, and value
                components = line.split(",")
                key = components[0]
                type_ = components[1]
                value = components[2]

                # Convert the value to the appropriate type
                if type_ == 'int':
                    value = int(value)
                elif type_ == 'float':
                    value = float(value)
                elif type_ == 'str':
                    value = str(value) # Assuming the value is quoted
                elif type_ == "bool":
                    value = {"True":True,"False":False}[value]

                # Set the global variable
                globals()[key] = value
        
class SoundManager:
    mixer.init()
    prefix = ResourcePrefix()

    channel_dict: Dict[ str, mixer.Channel ] = {
        "MUS"   : mixer.Channel(0),
        "BG"    : mixer.Channel(1),
        "SFX"   : mixer.Channel(2)
    }
    sound_dict: Dict[ str, mixer.Sound ] = {
        "intro"     : mixer.Sound(prefix + "assets/intro.ogg"),
        "phase1"    : mixer.Sound(prefix + "assets/phase1.ogg"),
        "phase2"    : mixer.Sound(prefix + "assets/phase2.ogg"),
        "phase3"    : mixer.Sound(prefix + "assets/phase3.ogg"),
        "end"       : mixer.Sound(prefix + "assets/end.ogg"),
        "chug"      : mixer.Sound(prefix + "assets/chug.ogg"),
        "deus"      : mixer.Sound(prefix + "assets/deus_ex_machina.ogg"),
        "die"       : mixer.Sound(prefix + "assets/die.ogg"),
        "silence"   : mixer.Sound(prefix + "assets/silence.ogg")
    }

    """
    @function play_sound Plays the music file indicated by filename,
    if filename exists in song_dict.


    @return True if the song was able to be played, else False
    """
    @classmethod
    def play_sound(cls, channel: str, filename: str, loop: BooleanVar) -> bool:
        if(filename not in cls.sound_dict.keys()) or (channel not in cls.channel_dict.keys()):
            return False
        target_sound = cls.sound_dict[filename]
        target_channel = cls.channel_dict[channel]
        target_channel.play(target_sound, -1 if loop else 0)
        return True
    
    """
    @function set_volume Adjusts all channel's volumes to,
    the given value between 0.0  and 1.0.
    """
    @classmethod
    def set_volume(cls, val: int) -> None:
        volume = int(val) / 100
        for mixer in cls.channel_dict.values():
            mixer.set_volume(volume)

class ProgressBars:

    Bars = [] # [{"Key":str,"Magnitude":int,"Activation":int,"Delay":{"Actual":int,"Lower":int,"Upper":int},"Persistence":bool}]

    @classmethod
    # Add a new progressbar to cls.Bars based on instantiation data
    # If a bar already exists with the provided key, it is updated (no new one is made)
    def BarAdd(cls, Key: str, Magnitude: int, Delay: Tuple, Persistence: bool) -> None:
        #check what time it is from the global Time variable
        Now = Time_Now()

        #Gather values needed to instantiate a new progress bar item
        Key = Key # the string value of the action this bar represents
        Magnitude = Magnitude # the "amount"/"intensity" of an action to take
        Delay = Delay # a Tuple (Lower:int,Upper:int)
        Delay_LowerBound = Delay[0] # the lower bounds of the delay range
        Delay_UpperBound = Delay[1] # the upper bound of the delay range
        Delay_Actual = random.randint(Delay_LowerBound, Delay_UpperBound)
        Activation = Now + Delay_Actual # a unix timestamp. when Now > this value, the time is considered to have elapsed
        Persistence = Persistence #  should this bar be iteratively re-instantiated, or can it just expire without replacement

        #Create the new bar and add it to this class's list of bars
        newBar = {"Key":Key, "Magnitude":Magnitude, "Activation":Activation, "Delay":{"Actual":Delay_Actual,"Lower":Delay_LowerBound,"Upper":Delay_UpperBound}, "Persistence":Persistence }
        
        # Does the bar with this key already exist?
        # If so, find its index
        bar_index = next((index for index, bar in enumerate(cls.Bars) if bar["Key"] == Key), None)
        
        if bar_index is not None:
            cls.Bars[bar_index] = newBar
        else:
            cls.Bars.insert(0, newBar)

    @classmethod
    # Return the bar in cls.Bars who's "Key" value = key
    def GetBarByKey(cls, key:str) -> dict | None:
        for bar in cls.Bars:
            if bar["Key"] == key:
                return bar
        return None

    @classmethod
    # MaintainConsistency() checks each item of this class's Bars list, and removes duplicate items with the same value for their "Key" property
    # In effect, this means that if there was [{"Key":"Value1","Data":7},{"Key":"Value1","Data:9"}], the second dictionary would be removed because
    # an earlier dictionary in the list already has "Key":"Value1"
    def RemoveDuplicates(cls) -> None:
        seen_keys = set()
        cls.Bars = [d for d in cls.Bars if not (d["Key"] in seen_keys or seen_keys.add(d["Key"]))]

    @classmethod
    # Iterates over all bars in cls.Bars and checks them for updates
    # If the bar's activation timestamp is less than Now's timestamp, the bar's time is up
    # The Bar's Key and Magnitude are given to the scorekeeper to preform game functions
    # If the bar is persistent, we overwrite the current bar with a new bar of equivalent Key, Magnitude, and Persistence,
    # but where a new delay is selected between the Lower and Upper bound, and the bar is set to expire at Now + That Delay
    # If the bar is not persistent, that entry is removed from cls.Bars without replacement
    def Progressor(cls) -> None:
        for index, bar in enumerate(cls.Bars):
            if (bar)["Activation"] < Time_Now():
                Scorekeeper(bar) # do the action here. Scorekeeper will identify what to do based on the NAME @ [0] and will do it by the AMOUNT @ [1]

                Key = bar["Key"] # The name of the event/action
                Magnitude = bar["Magnitude"] # The "amount" of the event, EX: Energy+1
                Activation = bar["Activation"] # A UNIX timestamp. If NOW > Activation, it is considered to have elapsed.
                Delay = bar["Delay"] # A dictionary. {"Lower":int,"Upper":int} Useful for instantiating additional bars at a fixed interval.
                Persistence = bar["Persistence"] # Whether or not we should create a new bar of Activation = Activation + Delay to replace this one, or if we should just let it be deleted. 1 = make additional, 0 = let die.

                if Persistence == 1: # we should create a replacement bar for this one
                    NewDelay = random.randint(Delay["Lower"], Delay["Upper"]) # pick a new delay for the next problem, between the min and max time
                    DelayDict = {"Actual":NewDelay,"Lower":Delay["Lower"],"Upper":Delay["Upper"]}
                    cls.Bars[index] = {"Key":Key,"Magnitude":Magnitude,"Activation":Activation+NewDelay,"Delay":DelayDict,"Persistence":Persistence} # create the same bar but <Delay> in the future
                if Persistence == 0: # we should let this bar expire without replacement
                    cls.Bars[index] = "REAPME" #delete the bar, as it is not persistent

        cls.Bars = [bar for bar in cls.Bars if bar != "REAPME"] # remove items that want to be removed
    
    @classmethod
    # Drop all progressbars from this class
    # Sets cls.Bars = []
    def Dump(cls) -> None:
        cls.Bars = []

    @classmethod
    # Given a string Key, returns a float 0-1 representing how far
    # along a progress bar is into its life. 0.0 = just born, 1.0 = being killed
    def CompletionPercent(cls, BarKey:str) -> float:
        ProblemBar = cls.GetBarByKey(BarKey)
        RemainingTime = ProblemBar["Activation"] - Time_Now()
        Delay = ProblemBar["Delay"]["Actual"]
        
        PercentComplete = float(RemainingTime) / float(Delay)
        PercentComplete = 1.0 - PercentComplete

        return PercentComplete

class Alphabet:
    alphabet="abcdefghijklmnopqrstuvwxyz_~"
    #alphabet="abcdefghijklmnopqrstuvwxyz1234567890!@#$%=?*_~"
    special_chars: Dict[ str, str ] = {
        '!': 'excl',
        '@': 'at',
        '#': 'hash',
        '$': 'dollar',
        '%': 'percent',
        '=': 'equals',
        '?': 'question',
        '*': 'asterisk',
        '~': "Return"
    }

    @classmethod
    def Relate(cls, index: int) -> str:
        if(index < 0) or (index > 45):
            return "+"
        result = cls.alphabet[index]
        return result
 
    @classmethod
    def Escape(cls, unescaped: str) -> str:
        return cls.special_chars.get(unescaped, unescaped)
    
    @classmethod
    def RandomSafe(cls) -> str:
        result = random.choice(cls.alphabet)
        if result == "~":
            result = "e"
        if result == "_":
            result = "t"
        return result

class FontInstaller:
    FontSource = ResourcePrefix() + "exe/InhumanBB.ttf"
    FileName =  "Inhuman BB.ttf"

    @classmethod
    def Install(cls) -> None:
        #try:
        #    if platform.system().upper() == "WINDOWS":
        #        cls.Windows()
        #    elif platform.system().upper() == "LINUX":
        #        cls.Linux()
        #    elif platform.system().upper() == "DARWIN":
        #        cls.macOS()
        #    else:
        #        pass
        #except:
        #    traceback.print_exc()
        cls.Warn()

    @classmethod
    def Warn(cls) -> None:
        global GameActive
        global ErrorHeading
        global ErrorSubtitle
        available_fonts = font.families()
        if("Inhuman BB" not in available_fonts):
            GameActive = -1
            ErrorHeading = "Fonts Not Installed"
            ErrorSubtitle = "The font \"Inhuman BB\" is not installed.\nPlease install it manually or proceed\nwith a sub-optimal graphical experience.\n\nIt is located alongside this executible as \"InhumanBB.ttf\"."



    @classmethod
    def Windows(cls) -> None:
        # Destination path for the user's Fonts directory
        fonts_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Fonts')

        if not os.path.isfile(os.path.join(fonts_dir, cls.FileName)):
            # Copy the font file to the user's Fonts directory
            shutil.copy(cls.FontSource, fonts_dir)

            # Load the font into the system font table
            font_path = os.path.join(fonts_dir, os.path.basename(cls.FontSource))
            font_path_w = font_path.encode('utf-16-le') # Convert to wide string

            # Use ctypes to call AddFontResourceEx
            ctypes.windll.gdi32.AddFontResourceExW(font_path_w, 0x10, 0)

    @classmethod
    def Linux(cls) -> None:

        # Destination path for the user's Fonts directory
        fonts_dir = os.path.expanduser('~/.fonts')

        if not os.path.isfile(os.path.join(fonts_dir, cls.FileName)):
            # Copy the font file to the user's Fonts directory
            shutil.copy(cls.FontSource, fonts_dir)

            # Update the font cache
            subprocess.run(['fc-cache', '-fv'], check=True)
    
    @classmethod
    def macOS(cls) -> None:
        # Destination path for the system's Fonts directory
        fonts_dir = '/Library/Fonts'

        if not os.path.isfile(os.path.join(fonts_dir, cls.FileName)):
            # Copy the font file to the system's Fonts directory
            shutil.copy(cls.FontSource, fonts_dir)

            # Load the font into the system font table
            font_path = os.path.join(fonts_dir, cls.FileName)
            font_path_c = font_path.encode('utf-8') # Convert to C string

            # Use ctypes to call ATSFontActivateFontsWithText
            ctypes.CDLL('/System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreText.framework/CoreText').ATSFontActivateFontsWithText(font_path_c, len(font_path_c), None, kATSOptionFlagsDefault, None)

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
    # Functionality of clicling the "Start" button

    global GameActive

    if GameActive == 0: #start the game from title
        StartAll()
    else: #abort the game and return to title
        SoundManager.play_sound("BG", 'chug', True)
        SoundManager.play_sound("MUS", 'intro', True)
        GameActive = 0
        
        

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
    
def Time_Now():
    # The calculates the current time in milliseconds from the OS clock.
    return int(time.time_ns() / 1_000_000)

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
    print(overlaps)
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
    global ErrorHeading
    global ErrorSubtitle

    clearCanvas()

    if GameActive == -1:
        c.create_text((CanvasWidth/2, CanvasHeight/4),fill='red',text=ErrorHeading,font=('Inhuman BB', 64), justify="center")
        c.create_text((CanvasWidth/2, CanvasHeight/1.5),fill='white',text=ErrorSubtitle,font=('Inhuman BB', 24), justify="center")
    else:
        if UseBinaryBG == True:
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

def ShuffleBackground() -> None:
    global BinaryWall
    global WallSource
    while True: # loop forever until the program ends
        preTime = Time_Now() # the time at the start of this frame
        BinaryWall = WallSource[Time_Now() % 1024:].ljust(len(WallSource), "0")
        postTime = Time_Now() # the time at the end of the frame
        waitTime = max(0, 50 - (postTime - preTime)) # wait N ms until the total amount of time between frames is >= 17
        time.sleep(waitTime / 1000.0)

# --- Executives ---
def TOTAL_MAIN():
    #The main loop, called every frame

    global GameActive
    global ScrubBuffer
    
    try:
        preFrame = Time_Now() #the time at the start of this frame
        GameState()
        ProgressBars.RemoveDuplicates()
        ProgressBars.Progressor()
        ScrubWrite()
        DrawMaster()
        postFrame = Time_Now() # the time at the end of the frame
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
    global root
    global c
    CanvasWidth = root.winfo_width()
    CanvasHeight = root.winfo_height() * 0.8
    c.config(height=CanvasHeight, width=CanvasWidth)

if __name__ == "__main__":

    Configurator.loadFromFile()

    # init    
    root.bind('<Key>', KeyPress)
    root.focus_force()
    root.title('Singularity')
    root.configure(bg='#000000') # set the window background to black
    root.bind('<Configure>', resize_canvas) # every time the window is changed (in this case resized), do something
    root.wm_iconphoto(True, tk.PhotoImage(file=(ResourcePrefix()+"assets/icon.png"))) # set the taskbar icon to a file
    
    if platform.system().upper() == "WINDOWS":
        root.state('zoomed')
    elif platform.system().upper() == "DARWIN":
        root.wm_state('zoomed')
    elif platform.system().upper() == "LINUX":
        root.wm_attributes("-zoomed", True)
    else:
        pass #not supported

    # Make sure the user has "Inhuman BB" installed as a font
    FontInstaller.Install()
    if(GameActive == 0):
        SoundManager.play_sound("BG", 'chug', True)
        SoundManager.play_sound("MUS", 'intro', True)

    #Make Canvas
    c.bind('<Motion>', motion)
    c.bind('<ButtonPress>', ClickRegistrar)
    c.pack(pady=10, fill='both', expand=True, anchor="n")
    c.config(cursor="none")

    OhSevenFlash = ImageTk.PhotoImage(file=ResourcePrefix()+'assets/079Flash.jpg')
    c.create_image(500,500,image=OhSevenFlash)

    # button with text closing window
    b1 = tk.Button(root, text="Close", command=CloseAll, width=int(CanvasWidth/100))#, bg="gray20", fg="white")
    b1.pack(padx=5, pady=10, side='right')

    #Create start/menu button
    b2 = tk.Button(root, text="Start", command=StartLogic, width=int(CanvasWidth/100))#, bg="gray20", fg="white")
    b2.pack(padx=5, pady=10, side='left')

    #Create volume slider
    slider_label = tk.Label(root, text="Volume", background="black", fg="white")
    slider_label.pack()
    slider_value = tk.DoubleVar(value=50)
    slider_length = root.winfo_screenwidth() * 0.25
    volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=SoundManager.set_volume, length=slider_length, variable=slider_value, troughcolor='grey20', sliderlength=20, background="white", showvalue=False)
    volume_slider.pack(anchor="n", side="top")

    if UseBinaryBG:
        shuffle_thread = threading.Thread(target=ShuffleBackground, daemon=True)
        shuffle_thread.start()

    #Specific programs to be run once on startup.
    SoundManager.set_volume(50)
    TOTAL_MAIN()

    # "start the engine"
    root.mainloop()
