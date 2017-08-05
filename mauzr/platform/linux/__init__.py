""" Bootstrap the mauzr agent on linux systems. """
__author__ = "Alexander Sowitzki"

import mauzr.platform.posix

class Core(mauzr.platform.posix.Core):
    """ Manage program components on linux platforms.

    :param suit: Suit this agent belongs to.
    :type suit: str
    :param agent: Name of the agent.
    :type agent: str
    :param instance: Instance of this agent. May be None
    :type instance: str
    :param parser: Argparse instance to use. If None, a new one will be used.
    :type parser: argparse.ArgumentParser
    """

    def __init__(self, suit, agent, instance=None, parser=None):
        mauzr.platform.posix.Core.__init__(self, suit, agent, instance, parser)
        self.database = None
        if "systemd" in self.config and self.config["systemd"]:
            from mauzr.platform.linux.systemd import Systemd
            self.add_context(Systemd(self))