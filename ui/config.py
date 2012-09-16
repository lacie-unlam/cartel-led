# -*- coding: UTF-8 -*-

import gtk
import os

from widgets import ComboFunciones, MatrizLeds

class Config:
    FRECUENCIA = 1.0
    FASE = 1.0
    ON_OFF_BTN_OFF = 'Continuar'

    def __init__(self, leds_horizontales, leds_verticales): 
        self.leds_horizontales, self.leds_verticales = int(leds_horizontales), int(leds_verticales)
        self.build_ui_from_xml()
        self.matriz_leds = MatrizLeds(self.leds_horizontales, self.leds_verticales)
        self.container.pack_start(self.matriz_leds)
        self.container.reorder_child(self.matriz_leds, 0)

    def on_window_delete_event(self, widget, data=None):
        self.matriz_leds.clear()
        return False

    def build_ui_from_xml(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.abspath('cartel-led-config.glade'))
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window')
        self.container = self.builder.get_object('container')
        self.combo_func = ComboFunciones()
        combobox = self.combo_func.get_widget()
        tabla = self.builder.get_object('tabla')
        tabla.attach(combobox, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
        self.frecuencia = self.builder.get_object('frecuencia')
        self.frecuencia.set_value(self.FRECUENCIA)
        self.fase = self.builder.get_object('fase')
        self.fase.set_value(self.FASE)
        self.on_off_btn = self.builder.get_object('on_off_btn')

    def show(self):
        self.window.show_all()

    def on_encender_clicked(self, widget):
        self.on_off_btn_off()
        self.matriz_leds.set()

    def on_limpiar_clicked(self, widget):
        self.on_off_btn_off()
        self.matriz_leds.clear()

    def on_off_btn_toggled_cb(self, widget):
        if widget.get_active():
            widget.set_label('Parar')
            self.matriz_leds.start()
        else:
            widget.set_label(self.ON_OFF_BTN_OFF)
            self.matriz_leds.clear()

    def on_off_btn_off(self):
        if self.on_off_btn.get_active():
            self.on_off_btn.set_active(False)
            self.on_off_btn.set_label(self.ON_OFF_BTN_OFF)