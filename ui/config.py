# -*- coding: UTF-8 -*-

import gtk
import os

from lib.matriz import Matriz

class Configuracion:
    def __init__(self, leds_horizontales, leds_verticales): 
        self.matriz = Matriz(int(leds_verticales), int(leds_horizontales))
        self.build_ui_from_xml()

    def on_configuracion_delete_event(self, widget, data=None):
        return False

    def build_ui_from_xml(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.abspath('cartel-led-config.glade'))
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('configuracion')

    def show(self):
        self.window.show()

    def on_encender_clicked(self, widget):
        self.matriz.set()

    def on_limpiar_clicked(self, widget):
        self.matriz.clear()