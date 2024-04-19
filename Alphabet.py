class Alphabet:
    from typing import Dict
    import random

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