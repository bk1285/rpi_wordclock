# coding: utf8

import threading
import os
import sys
from wordclock_interfaces import event_handler as weh
from wordclock_tools.wordclock_colors import Color

import wx
# in all modules that use pubsub 
from wx.lib.pubsub import pub as Publisher

class WxStripWindow(wx.Frame):

    def __init__(self, parent, title,weh):
        super(WxStripWindow, self).__init__(parent, title=title, 
            size=(500, 500))            
        self.weh = weh
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)        
        self.SetBackgroundColour('#000000')

        # create a pubsub receiver
        self.panel.SetFocus()
        self.Show()
        
    def onKeyPress(self, event=None):
        keycode = event.GetKeyCode()
        if(keycode == wx.WXK_LEFT):
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_LEFT)
        elif(keycode == wx.WXK_RIGHT):
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_RIGHT)
        elif(keycode == wx.WXK_RETURN):
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_RETURN)

    def updateDisplay(self):
        """
        Receives data from thread and updates the display
        """
        self.Update()

class WxStrip():
    def __init__(self, weh):        
        self.label = "QTstrip"
        
        chars = "ESKISTLFÜNFZEHNZWANZIGDREIVIERTELTGNACHVORJMHALBQZWÖLFPZWEINSIEBENKDREIRHFÜNFELFNEUNVIERWACHTZEHNRSBSECHSFMUHR...."
        
        self.labels = []
        self.colors = []
        
        self.weh = weh        
        Publisher.subscribe(self.update, "update")
        self.brightness = 255;
        if(isinstance(threading.current_thread(), threading._MainThread)):                
            self.w =  WxStripWindow(None, title='Wordclock',weh=weh)            
            if(self.w != None):
                
                x = 0
                y = 0
                vbox = wx.BoxSizer(wx.VERTICAL)
                font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
                font.SetPointSize(32)
                gs = wx.GridSizer(11, 11, 5, 5)
                vbox.Add(gs, proportion=1, flag=wx.EXPAND)
                for i in str(chars):                     
                    self.colors.append(Color(0, 0, 0))
                    tmpText = i
                    
                    st2 = wx.StaticText(self.w, label=tmpText)
                    st2.SetFont(font)
                    st2.SetForegroundColour((255,255,255)) # set text color
                    gs.AddMany( [(st2, 0, wx.EXPAND) ])                
                    self.labels.append(st2)                    
                    
                    x = x + 1;
                    if x == 11:                                
                        x = 0
                        y = y + 1

                self.w.SetSizer(vbox)
                self.w.SetSize(1024, 1024)    
        else:
            print("No Main Thread")        
     
    def delete_event(self, widget, event, data=None):
        return False
        
    def setBrightness(self, brightness):
        self.brightness = brightness
    
    def getBrightness(self):
        return self.brightness
    
    def begin(self):
        self.w.Show()        
        #self.app.exec_()
        #os._exit(1)
    
    def setPixelColor(self, index, color):
        self.colors[int(index)] = color

    def update(self):  
        if(self.w != None):
            if(isinstance(threading.current_thread(), threading._MainThread)):
                for label,color in zip(self.labels, self.colors):            
                    label.SetForegroundColour((color.r,color.g,color.b, self.brightness)) # set text color
            else:
                wx.CallAfter(Publisher.sendMessage, "update")
                
    def show(self):        
        self.update()    
