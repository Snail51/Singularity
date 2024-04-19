from typing import Tuple
import os
# --- Config ---
StartingEnergy = 0 # >=0
StartingMaxEnergy = 100
ClickCost = 25 # how much energy to deduct for certain actions # <= StartingMaxEnergy
PlayerSize = 20 #the width of the player's cursor
EnergyRate = 100
MaxEnergyRate = 5000
MaxEnergyCap = 200
JitterRate = 200
ScrubLength = 5000
StartingHealth = 10
StartingViruses: int = 5 # <= 26
ProblemLength: int = 6
CanvasWidth: int = 1000
CanvasHeight: int = 700
UseBinaryBG: bool = True
ProblemType: str = "String" # Prompts or String
DebugMode: bool = False
PrevScansShow: bool = False

# --- variables ---
cwd = os.path.join(os.path.dirname(__file__))
print(cwd)
ShipRoot: Tuple = (0,0)
Energy = 0 # How much energy the user currently has. Increases over time. Is consumed by certain actions.
MaxEnergy = 100 # Upper-bound to the user's energy. Decreases over time.
ProblemRate = (10000,20000) # how long between problems (ms)
#TITLE = The name of the functionality it accomplishes
#MAGNITUDE = The "amount" to act by; EX: Energy 1 = Increase the Energy by 1
#TIME = The UNIX timestamp when the even should be considered to have elapsed by (If NOW is greater than TIME, complete)
#DELAY = The amount of milliseconds that should be added to NOW if we were to create another instance of the Bar
#PERSISTENCE = If 0, the bar is destroyed when its time is up. If 1, we create a new bar with TIME = NOW + DELAY and the same TITLE, MAGNITUDE, and PERSISTENCE Values. This allows us to have repeated functions
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
PromptTicker = ""


WallSource = ''.join(format(byte, '08b') for byte in os.urandom(1500))