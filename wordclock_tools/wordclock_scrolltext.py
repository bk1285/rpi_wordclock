import datetime
import logging

class ScrollText:

    def __init__(self, scrolltext=None, scrollrepeat = 1, scrolldatetime = datetime.datetime.now(), scrollactive = False):
        self.scrolltext = scrolltext
        self.scrollrepeat = scrollrepeat
        self.scrolldatetime = scrolldatetime
        self.scrollcount = 1 if scrollactive else 0
        self.lastRender = scrolldatetime

    def checkIfScrollIsRequiredInternal(self, now):
        if self.scrolltext == None:
            return False

        if self.scrollcount > 0:
            if self.scrollcount == self.scrollrepeat:
                self.scrollcount = 0
            else:
                self.scrollcount += 1
            return True

        if now > self.scrolldatetime and self.lastRender <= self.scrolldatetime:
            return True
                    
        return False

    def checkIfScrollIsRequired(self, now):
        if self.checkIfScrollIsRequiredInternal(now):
            self.lastRender = datetime.datetime.now()
            return True
        return False
