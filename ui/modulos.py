# -*- coding: UTF-8 -*-

import gtk
import os

import funcion
import config

class Window:
    MODS_HORIZONTALES = 7
    MODS_VERTICALES = 3

    def __init__(self):
        self.build_ui_from_xml()
        self.set_default_values()
        self.window.show_all()
        gtk.main()

    def on_window_delete_event(self, widget, data=None):
        gtk.main_quit()
        return False

    def build_ui_from_xml(self):
        builder = gtk.Builder()
        builder.add_from_file(os.path.abspath('modulos.glade'))
        self.mods_horizontales = builder.get_object('mods_horizontales')
        self.mods_verticales = builder.get_object('mods_verticales')
        self.window = builder.get_object('window')
        builder.connect_signals(self)

    def set_default_values(self):
        self.mods_horizontales.set_value(self.MODS_HORIZONTALES)
        self.mods_verticales.set_value(self.MODS_VERTICALES)

    def on_crear_cartel_clicked(self, widget):
        funcion.Window(self.mods_horizontales.get_value(), self.mods_verticales.get_value())

    def on_configuracion_clicked(self, widget):
        config.Window()