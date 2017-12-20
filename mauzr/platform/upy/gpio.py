"""  Access GPIO. """
__author__ = "Alexander Sowitzki"

import machine # pylint: disable=import-error

class GPIO:
    """ Use GPIO pins. """

    def __init__(self, core):
        self._pins = {}
        self._input_mapping = {}
        self.listeners = []

    def _on_change(self, pin):
        # React to a pin change.

        name = self._input_mapping[str(pin)]
        value = pin()
        [listener(name, value) for listener in self.listeners]

    def setup_input(self, name, edge, pullup):
        """ Set pin as input.

        :param name: ID of the pin.
        :type name: str
        :param edge: Edges to inform listeners about. May be "none", "rising", \
                     "falling" or "both".
        :type edge: str
        :param pullup: Pull mode of the pin. May be "none", "up" or "down".
        :type pullup: str
        """

        if pullup is None:
            pullup = "none"
        if edge is None:
            edge = "none"

        pull_map = {"none": None, "up": machine.Pin.PULL_UP}

        edge_map = {"none": None, "rising": machine.Pin.IRQ_RISING,
                    "falling": machine.Pin.IRQ_FALLING,
                    "both": machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING}

        pin = machine.Pin(name, mode=machine.Pin.IN, pull=pull_map[pullup])
        self._pins[name] = pin
        self._input_mapping[str(pin)] = name

        if edge != "none":
            # Add callback if edge is specified
            pin.irq(trigger=edge_map[edge], handler=self._on_change)

    def setup_output(self, name, initial=False):
        """ Set pin as output.

        :param name: Numer of the pin.
        :type name: int
        :param initial: Initial value to set.
        :type initial: bool
        """

        self._pins[name] = machine.Pin(name, mode=machine.Pin.OUT)
        self._pins[name](initial)

    def __getitem__(self, name):
        # Retrieve value of an input pin.

        return self._pins[name]()

    def __setitem__(self, name, value):
        # Set the value of an output pin.

        return self._pins[name](value)
