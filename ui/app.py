# -*- coding: UTF-8 -*-

import gtk
import os

from config import Config

class App:
    LEDS_HORIZONTALES = 48
    LEDS_VERTICALES = 8

    def __init__(self):
        self.build_ui_from_xml()
        self.set_default_values()
        gtk.main()

    def on_window_delete_event(self, widget, data=None):
        gtk.main_quit()
        return False

    def build_ui_from_xml(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.abspath('cartel-led-inicio.glade'))
        self.leds_horizontales = self.builder.get_object('leds_horizontales')
        self.leds_verticales = self.builder.get_object('leds_verticales')
        self.builder.connect_signals(self)

    def set_default_values(self):
        self.leds_horizontales.set_value(self.LEDS_HORIZONTALES)
        self.leds_verticales.set_value(self.LEDS_VERTICALES)

    def on_crear_cartel_clicked(self, widget):
        config = Config(self.leds_horizontales.get_value(), self.leds_verticales.get_value())
        config.show()