class Gadgets(object):
    """
    A Gadgets object providing managing of various gadgets for display on analytics dashboard.
    Gadgets are registered with the Gadgets using the register() method.
    """
    def __init__(self):
        self._registry = {} # gadget hash -> gadget object.

    def get_gadget(self, id):
        return self._registry[id]

    def get_gadgets(self):
        return self._registry.values()

    def register(self, gadget):
        """
        Registers a gadget object.
        If a gadget is already registered, this will raise AlreadyRegistered.
        """
        self._registry[gadget.id] = gadget

gadgets = Gadgets()
