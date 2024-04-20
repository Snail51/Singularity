from SoundManager import SoundManager
from global_vars import *

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