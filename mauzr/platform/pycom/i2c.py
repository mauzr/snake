""" Provide I2C functionality for pycm devices. """
__author__ = "Alexander Sowitzki"

import ustruct # pylint: disable=import-error
import machine # pylint: disable=import-error

class Bus:
    """ Manage an I2C bus.

    :param core: Core instance.
    :type core: object
    :param cfgbase: Configuration entry for this unit.
    :type cfgbase: str
    :param kwargs: Keyword arguments that will be merged into the config.
    :type kwargs: dict

    **Configuration:**

        - **baudrate** (:class:`int`) - Baudrate of the bus.
        - **pins** (:class:`tuple`) - Pins to use for the bus (SDA, SCL) \
            as tuple of strings.
    """

    def __init__(self, core, cfgbase="i2c", **kwargs):
        cfg = core.config[cfgbase]
        cfg.update(kwargs)

        self.baudrate = cfg.get("baudrate", 400000)
        self.pins = cfg.get("pins", ("P9", "P10"))
        self.i2c = machine.I2C(0)

    def __enter__(self):
        # Init bus.

        self.i2c.init(machine.I2C.MASTER, baudrate=self.baudrate,
                      pins=self.pins)
        return self

    def __exit__(self, *exec_details):
        # Deinit bus.

        pass

    def write(self, address, data):
        """ Write data to a device.

        :param address: The address of the device.
        :type address: object
        :param data: Data to write.
        :type data: bytes
        :returns: Number of bytes written.
        :rtype: int
        """

        if not isinstance(data, (bytearray, bytes)):
            # Convert data to bytes if this hasn't happened already
            data = bytes(data)

        return self.i2c.writeto(address, data)

    def read(self, address, amount):
        """ Read data from a device.

        :param address: The address of the device.
        :type address: object
        :param amount: How much data to receive at most.
        :type amount: int
        :returns: Bytes read.
        :rtype: bytes
        """

        return self.i2c.readfrom(address, amount)

    def read_register(self, address, register, amount=None, fmt=None):
        """ Read data from an register of a device.

        :param address: The address of the device.
        :type address: object
        :param register: Address of the register.
        :type register: byte
        :param amount: How much data to receive at most.
        :type amount: int
        :param fmt: Optional data format passed to :func:`struct.unpack`
            with the received buffer.
        :type fmt: str
        :returns: The received bytes or the unpacked datatype if fmt was given.
        :rtype: object
        """

        if amount is None and fmt is not None:
            # Calculate amount if fmt is given and amount is not set
            amount = ustruct.calcsize(fmt)

        value = self.i2c.readfrom_mem(address, register, amount)

        if fmt:
            # Unpack value if fmt set
            value = ustruct.unpack(fmt, value)
            if len(value) == 1:
                # If unpacked list contains only one value pass it
                value = value[0]

        return value
