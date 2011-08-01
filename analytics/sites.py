class Gadgets(object):
    """
    A Gadgets object providing managing of various gadgets for display on analytics dashbaord.
    Gadgets are registered with the Gadgets using the register() method.
    """
    def __init__(self):
        self._registry = {} # gadget hash -> gadget object.

    def get_gadget(self, hash):
        return self._registry[hash]

    def get_gadgets(self):
        return self._registry.values()

    def register(self, gadget):
        """
        Registers a gadget object.
        If a gadget is already registered, this will raise AlreadyRegistered.
        """
        self._registry[gadget.__hash__()] = gadget

gadgets = Gadgets()
