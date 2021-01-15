# coding: utf8

import gtk
import gobject
import threading
from gtk._gtk import FILL
import pango
import os
from wordclock_interfaces import event_handler as weh
from wordclock_colors import Color

gobject.threads_init()

class GTKstrip(threading.Thread):
    def __init__(self, weh):
        super(GTKstrip, self).__init__()
        self.label = "GTKstrip"

        chars = "ESKISTLFÜNFZEHNZWANZIGDREIVIERTELTGNACHVORJMHALBQZWÖLFPZWEINSIEBENKDREIRHFÜNFELFNEUNVIERWACHTZEHNRSBSECHSFMUHR...."

        self.labels = []
        self.colors = []

        self.weh = weh

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.win.connect("delete_event", self.delete_event)
        self.win.connect("destroy", self.destroy)
        self.win.connect("key_press_event", self.key_press_event)

        table = gtk.Table(11, 11, True)

        x = 0
        y = 0
        for i in unicode(chars):
            label = gtk.Label(i)
            self.labels.append(label)
            self.colors.append(Color(0, 0, 0))

            table.attach(label, x, x + 1, y, y + 1, FILL, FILL)

            x += 1
            if x == 11:
                x = 0
                y += 1

            attrs = pango.AttrList()
            # attrs.insert(pango.AttrLanguage("de"))
            attrs.insert(pango.AttrForeground(0, 0, 0))
            attrs.insert(pango.AttrSize(30 * 1000))
            attrs.insert(pango.AttrBackground(0, 0, 0))
            label.set_attributes(attrs)

            label.show()

        color = gtk.gdk.color_parse('#000000')
        self.win.modify_bg(gtk.STATE_NORMAL, color)
        self.win.add(table)
        self.win.show_all()

    def key_press_event(self, widget, event):
        if event.keyval == 65361:
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_LEFT)
        elif event.keyval == 65363:
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_RIGHT)
        elif event.keyval == 65362:
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_RETURN)

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def run(self):
        gtk.main()
        os._exit(1)

    def begin(self):
        self.start()

    def setPixelColor(self, index, color):
        self.colors[index] = color

    def update(self):
        for label, color in zip(self.labels, self.colors):
            attrs = label.get_attributes()
            attrs.change(pango.AttrForeground(int(color.r / 255.0 * 65535), int(color.g / 255.0 * 65535),
                                              int(color.b / 255.0 * 65535)))
            label.set_attributes(attrs)

    def show(self):
        gobject.idle_add(self.update)
