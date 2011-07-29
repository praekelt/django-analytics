from random import randint

class AlreadyRegistered(Exception):
    pass

class Gadgets(object):
    """
    A Gadgets object providing managing of various gadgets for display on analytics dashbaord.
    Gadgets are registered with the Gadgets using the register() method.
    """
    def __init__(self):
        self._registry = {} # gadget id -> gadget object.

    def gen_id(self):
        id = randint(1000000, 9000000)
        while id in self._registry.keys():
            id = randint(1000000, 9000000)
        return id

    def get_gadget(self, id):
        return self._registry[id]

    def get_gadgets(self):
        return self._registry.values()

    def register(self, gadget):
        """
        Registers a gadget object.
        If a gadget is already registered, this will raise AlreadyRegistered.
        """
        if gadget in self._registry:
            raise AlreadyRegistered
        else:
            id = self.gen_id()
            gadget.id = id
            self._registry[id] = gadget
    
gadgets = Gadgets()
