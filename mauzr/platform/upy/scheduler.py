""" Scheduler for upy systems. """
__author__ = "Alexander Sowitzki"

import gc # pylint: disable=import-error
import utime # pylint: disable=import-error
import mauzr.platform.scheduler

class Task(mauzr.platform.scheduler.Task):
    """ :class:`mauzr.platform.scheduler.Task` for upy. """

    @staticmethod
    def _now():
        # The current time in ms.
        return utime.ticks_ms()

class Scheduler(mauzr.platform.scheduler.Scheduler):
    """ Scheduler for the upy platform. """

    def __call__(self, *args, **kwargs):
        """ Create a new task.

        See :class:`mauzr.platform.scheduler.Task`
        """

        task = Task(self, *args, **kwargs)
        self.tasks.append(task)
        return task

    @staticmethod
    def _wait(delay):
        # Wait the specified amount of time.

        # Wait with utime
        utime.sleep_ms(delay)

    @staticmethod
    def _idle():
        # No active tasks are present. Wait and check for new tasks.

        raise RuntimeError("Scheduler is going idle with no one to reset it")

    def handle(self, block):
        """ Run the scheduler and process tasks. """

        while True:
            # Handle scheduler
            next_task = self._handle(wait=block)
            # Force garbage collector
            gc.collect()

            if not block:
                return next_task