
class prototype(object):
    """
    First draft of python prototypal inheritance.
    """
    def __init__(self, delegate):
        self._delegate = delegate

    def __call__(self, cls):
        bound_delegate = self._delegate
        def replace_getattr(self, name):
            return getattr(bound_delegate, name)

        cls.__getattr__ = replace_getattr
        return cls

def proto2(delegate):
    """
    Better implementation of prototypal inheritance.  Classes that have
    a delegate will defer to them unless they override the property.

    This is basically identical to javascript inheritance.
    """
    def wrap(cls):
        old_getattr = cls.__getattr__ if '__getattr__' in cls.__dict__ else None
        def __getattr__(self, name):
            if old_getattr:
                try:
                    return old_getattr(self, name)
                except AttributeError:
                    pass
            return getattr(delegate, name)
                
        cls.__getattr__ = __getattr__
        return cls
    return wrap
                

class NotDecorated(object):
    def __init__(self, str):
        print "not decorated", self.__dict__, str

    def foo(self):
        print "in foo!"

    def bar(self):
        print "in undecorated bar"


repl = NotDecorated("repl ctr")

@prototype(repl)
class Decorated(object):
    def __init__(self, str):
        print "decorated", self.__dict__, str

    def bar(self):
        print "in decorated bar"

@proto2(repl)
class Decorated2(object):
    def __init__(self, str):
        print "decorated2", self.__dict__, str

    def bar(self):
        print "in decorated2 bar"

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            def repl():
                print name
            return repl



dc = Decorated("dc ctr")
dc.foo()
dc.bar()

dc2 = Decorated2('dc2 ctr')
dc2.foo()
dc2.bar()
dc2.cat()
