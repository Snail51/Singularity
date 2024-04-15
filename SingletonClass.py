
class SingletonClass:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).\
                __new__(cls, args, kwargs)
        return cls.instance
    
