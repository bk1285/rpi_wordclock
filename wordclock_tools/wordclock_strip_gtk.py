# coding: utf8

import threading
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, Pango

from wordclock_interfaces import event_handler as weh
from wordclock_colors import Color

GObject.threads_init()

class GTKstrip(threading.Thread):
    def __init__(self, weh):
        super(GTKstrip, self).__init__()
        self.label = "GTKstrip"

        chars = "ESKISTLFÜNFZEHNZWANZIGDREIVIERTELTGNACHVORJMHALBQZWÖLFPZWEINSIEBENKDREIRHFÜNFELFNEUNVIERWACHTZEHNRSBSECHSFMUHR...."

        self.labels = []
        self.colors = []

        self.weh = weh

        self.win = Gtk.Window(Gtk.WindowType.TOPLEVEL)

        self.win.connect("delete_event", self.delete_event)
        self.win.connect("destroy", self.destroy)
        self.win.connect("key_press_event", self.key_press_event)

        table = Gtk.Table(11, 11, True)

        x = 0
        y = 0
        for i in chars:
            label = Gtk.Label(label=i)
            self.labels.append(label)
            self.colors.append(Color(0, 0, 0))

            fill = Gtk.AttachOptions(4)

            table.attach(label, x, x + 1, y, y + 1, fill, fill)

            x += 1
            if x == 11:
                x = 0
                y += 1

            attrs = Pango.AttrList.new()
            # attrs.insert(Pango.AttrLanguage("de"))
            attrs.insert(Pango.attr_foreground_new(0, 0, 0))
            attrs.insert(Pango.attr_size_new(30 * 1000))
            attrs.insert(Pango.attr_background_new(0, 0, 0))
            label.set_attributes(attrs)

            label.show()

        color = Gdk.color_parse('#000000')
        self.win.modify_bg(Gtk.StateType.NORMAL, color)
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
        Gtk.main_quit()

    def run(self):
        Gtk.main()
        os._exit(1)

    def begin(self):
        self.start()

    def setPixelColor(self, index, color):
        self.colors[index] = color

    def update(self):
        for label, color in zip(self.labels, self.colors):
            attrs = label.get_attributes()
            attrs.change(Pango.attr_foreground_new(int(color.r / 255.0 * 65535), int(color.g / 255.0 * 65535),
                                              int(color.b / 255.0 * 65535)))
            label.set_attributes(attrs)

    def show(self):
        GObject.idle_add(self.update)
