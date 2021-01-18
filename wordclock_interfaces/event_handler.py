import threading
from monotonic import monotonic as _time


class next_action:
    NEXT_PLUGIN = 1
    GOTO_MENU = 2
    RUN_DEFAULT_PLUGIN = 3


class event_handler:
    EVENT_INVALID = -1

    EVENT_BUTTON_LEFT = 0
    EVENT_BUTTON_RIGHT = 1
    EVENT_BUTTON_RETURN = 2
    EVENT_EXIT_PLUGIN = 3
    EVENT_NEXT_PLUGIN_REQUESTED = 4

    BUTTONS = {'left': EVENT_BUTTON_LEFT, 'right': EVENT_BUTTON_RIGHT, 'return': EVENT_BUTTON_RETURN}

    def __init__(self):
        self.condition = threading.Condition()
        self.event = self.EVENT_INVALID
        self.lock_time = 0.1
        self.nextAction = next_action.RUN_DEFAULT_PLUGIN

    def getNextAction(self, evt):
        if evt == self.EVENT_NEXT_PLUGIN_REQUESTED:
            self.nextAction = next_action.NEXT_PLUGIN
        elif evt == self.EVENT_BUTTON_RETURN:
            self.nextAction = next_action.GOTO_MENU
        else:
            self.nextAction = next_action.RUN_DEFAULT_PLUGIN

    def waitForEvent(self, seconds=None):
        self.condition.acquire()
        self.__wait_for(lambda: self.event != self.EVENT_INVALID, seconds)
        evt = self.event
        self.getNextAction(evt)
        self.event = self.EVENT_INVALID
        self.condition.release()
        return evt

    def setEvent(self, evt):
        self.condition.acquire()
        if self.event != self.EVENT_EXIT_PLUGIN and self.event != self.EVENT_NEXT_PLUGIN_REQUESTED:
            self.event = evt
        self.condition.notifyAll()
        self.condition.release()

    def waitForExit(self, seconds=None):
        self.condition.acquire()
        exitWasTriggered = self.__wait_for(
            lambda: self.event == self.EVENT_EXIT_PLUGIN or self.event == self.EVENT_NEXT_PLUGIN_REQUESTED, seconds)
        self.getNextAction(self.event)
        self.event = self.EVENT_INVALID
        self.condition.release()
        return True if exitWasTriggered else False

    def __wait_for(self, predicate, timeout=None):
        """
        Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        boolean value.  A timeout may be provided giving the maximum time to
        wait.

        """
        endtime = None
        waittime = timeout
        result = predicate()
        while not result:
            if waittime is not None:
                if endtime is None:
                    endtime = _time() + waittime
                else:
                    waittime = endtime - _time()
                    if waittime <= 0:
                        break
            self.condition.wait(waittime)
            result = predicate()
        return result
