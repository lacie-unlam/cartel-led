# -*- coding: UTF-8 -*-

import gtk
import re
from os import path

import modulos
from lib.comm import Serializer

class Window:
    def __init__(self):
        self.build_glade_ui()
        self.set_default_device()

    def on_window_delete_event(self, widget, data=None):
        return False

    def build_glade_ui(self):
        builder = gtk.Builder()
        builder.add_from_file(path.abspath('config.glade'))
        self.other_device = builder.get_object('other_device')
        self.options = self.other_device.get_group()
        self.device = builder.get_object('device')
        self.window = builder.get_object('window')
        builder.connect_signals(self)

    def set_default_device(self):
        device = Serializer.device
        if is_default_tty(device):
            for option in self.options:
                if(option.get_label() == device):
                    opt = option
                    break
        else:
            self.device.set_text(device)
            opt = self.other_device
        opt.set_active(True)
        opt.grab_focus()

    def get_active_option(self):
        for option in self.options:
            if option.get_active():
                return option

    def on_ok_clicked(self, widget):
        opt = self.get_active_option()
        if is_default_tty(opt.get_label()):
            device = opt.get_label()
        else:
            device = self.device.get_text()

        if(path.exists(device)):
            Serializer.device = device
            self.window.destroy()
        else:
            err_dialog = gtk.MessageDialog(parent=self.window, flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                                           type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, 
                                           message_format='Dispositivo no encontrado')
            err_dialog.run()
            err_dialog.destroy()


def is_default_tty(device):
    return device in ['/dev/ttyUSB0', '/dev/ttyS0']