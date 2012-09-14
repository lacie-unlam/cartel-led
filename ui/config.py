# -*- coding: UTF-8 -*-

import gtk
import os

from lib.matriz import Matriz
from func_mate import FuncMate

class Configuracion:
    FRECUENCIA = 1.0
    FASE = 1.0

    def __init__(self, leds_horizontales, leds_verticales): 
        self.leds_horizontales, self.leds_verticales = int(leds_horizontales), int(leds_verticales)
        self.matriz = Matriz(self.leds_verticales, self.leds_horizontales)
        self.build_ui_from_xml()
        self.build_preview()

    def on_configuracion_delete_event(self, widget, data=None):
        return False

    def build_ui_from_xml(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.abspath('cartel-led-config.glade'))
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('configuracion')
        self.container = self.builder.get_object('container')
        self.func_mate = FuncMate()
        combobox = self.func_mate.get_widget()
        tabla = self.builder.get_object('tabla')
        tabla.attach(combobox, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
        combobox.show()
        self.frecuencia = self.builder.get_object('frecuencia')
        self.frecuencia.set_value(self.FRECUENCIA)
        self.fase = self.builder.get_object('fase')
        self.fase.set_value(self.FASE)

    def build_preview(self):
        for i in range(self.leds_verticales):
            hbox = gtk.HBox(True)
            for i in range(self.leds_horizontales):
                group = gtk.RadioButton()
                hbox.pack_start(gtk.RadioButton(group))
            self.container.pack_start(hbox)

    def show(self):
        self.window.show_all()

    def on_encender_clicked(self, widget):
        self.matriz.set()

    def on_limpiar_clicked(self, widget):
        self.matriz.clear()

    def on_transmitiendo_toggled(self, widget):
        if widget.get_active():
            widget.set_label('Pausar')
        else:
            widget.set_label('Reanudar')