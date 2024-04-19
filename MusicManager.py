class SoundManager:

    import pygame.mixer as mixer
    from typing import Dict

    import ResourcePrefix
    from global_vars import Time
    

    mixer.init()
    prefix = ResourcePrefix.ResourcePrefix()

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
        for mixer in cls.channel_dict.values():
            mixer.set_volume(volume)