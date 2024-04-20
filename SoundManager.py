from global_vars import *
class SoundManager:
    def __new__(cls):
        
        glob_vars = globals()
        print(glob_vars)
        cls.mixer = glob_vars["mixer"]
        cls.mixer.init()

        cls.prefix = glob_vars["ResourcePrefix"].ResourcePrefix()
        cls.Dict = glob_vars["Dict"]
        cls.channel_dict = {
            "MUS"   : cls.mixer.Channel(0),
            "BG"    : cls.mixer.Channel(1),
            "SFX"   : cls.mixer.Channel(2)
        } 
        cls.sound_dict = {
            "intro"     : cls.cls.mixer.Sound(cls.prefix + "assets/intro.ogg"),
            "phase1"    : cls.mixer.Sound(cls.prefix + "assets/phase1.ogg"),
            "phase2"    : cls.mixer.Sound(cls.prefix + "assets/phase2.ogg"),
            "phase3"    : cls.mixer.Sound(cls.prefix + "assets/phase3.ogg"),
            "end"       : cls.mixer.Sound(cls.prefix + "assets/end.ogg"),
            "chug"      : cls.mixer.Sound(cls.prefix + "assets/chug.ogg"),
            "deus"      : cls.mixer.Sound(cls.prefix + "assets/deus_ex_machina.ogg"),
            "die"       : cls.mixer.Sound(cls.prefix + "assets/die.ogg"),
            "silence"   : cls.mixer.Sound(cls.prefix + "assets/silence.ogg")
        }
    """
    @function play_sound Plays the music file indicated by filename,
    if filename exists in song_dict.


    @return True if the song was able to be played, else False
    """
    @classmethod
    def play_sound(cls, channel: str, filename: str, loop: bool) -> bool:
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
        for channel in cls.channel_dict.values():
            channel.set_volume(volume)