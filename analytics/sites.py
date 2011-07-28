class AlreadyRegistered(Exception):
    pass

class Gadgets(object):
    """
    A Gadgets object providing managing of various gadgets for display on analytics dashbaord.
    Gadgets are registered with the Gadgets using the register() method.
    """
    def __init__(self):
        self._registry = [] # gadget object.

    def register(self, gadget):
        """
        Registers a gadget object.
        If a gadget is already registered, this will raise AlreadyRegistered.
        """
        if gadget in self._registry:
            raise AlreadyRegistered
        else:
            self._registry.append(gadget)
    
gadgets = Gadgets()
