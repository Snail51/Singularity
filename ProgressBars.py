class ProgressBars:

    from typing import Tuple
    import random

    from global_vars import Time

    Bars = [] # [{"Key":str,"Magnitude":int,"Activation":int,"Delay":{"Actual":int,"Lower":int,"Upper":int},"Persistence":bool}]

    @classmethod
    # Add a new progressbar to cls.Bars based on instantiation data
    # If a bar already exists with the provided key, it is updated (no new one is made)
    def BarAdd(cls, Key: str, Magnitude: int, Delay: Tuple, Persistence: bool) -> None:
        #check what time it is from the global Time variable

        Now = Time

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
        global Time
        for index, bar in enumerate(cls.Bars):
            if (bar)["Activation"] < Time:
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
        global Time

        ProblemBar = cls.GetBarByKey(BarKey)
        RemainingTime = ProblemBar["Activation"] - Time
        Delay = ProblemBar["Delay"]["Actual"]
        
        PercentComplete = float(RemainingTime) / float(Delay)
        PercentComplete = 1.0 - PercentComplete

        return PercentComplete