# -*- coding: UTF-8 -*-

import gtk
import os

from config import Config

class App:
    MODS_HORIZONTALES = 4
    MODS_VERTICALES = 3

    def __init__(self):
        self.build_ui_from_xml()
        self.set_default_values()
        gtk.main()

    def on_window_delete_event(self, widget, data=None):
        gtk.main_quit()
        return False

    def build_ui_from_xml(self):
        builder = gtk.Builder()
        builder.add_from_file(os.path.abspath('cartel-led-inicio.glade'))
        self.mods_horizontales = builder.get_object('mods_horizontales')
        self.mods_verticales = builder.get_object('mods_verticales')
        builder.connect_signals(self)

    def set_default_values(self):
        self.mods_horizontales.set_value(self.MODS_HORIZONTALES)
        self.mods_verticales.set_value(self.MODS_VERTICALES)

    def on_crear_cartel_clicked(self, widget):
        config = Config(self.mods_horizontales.get_value(), self.mods_verticales.get_value())
        config.show()