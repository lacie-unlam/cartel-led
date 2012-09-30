# -*- coding: UTF-8 -*-

import gtk
import os

from widgets import ComboFunciones, MatrizLeds

class Window:
    FRECUENCIA = 2
    FASE = 1.0
    ON_OFF_BTN_ON = 'Parar'
    ON_OFF_BTN_OFF = 'Continuar'

    def __init__(self, mods_horizontales, mods_verticales): 
        self.build_glade_ui()
        self.init_matriz_leds(int(mods_horizontales), int(mods_verticales))
        self.window.show()

    def on_window_delete_event(self, widget, data=None):
        self.matriz_leds.clear()
        return False

    def build_glade_ui(self):
        builder = gtk.Builder()
        builder.add_from_file(os.path.abspath('funcion.glade'))
        builder.connect_signals(self)

        self.fetch_widgets_from_xml(builder)

        # self.combo_func = ComboFunciones()
        # combobox = self.combo_func.get_widget()
        # tabla = builder.get_object('tabla')
        # tabla.attach(combobox, 1, 2, 0, 1, gtk.FILL, gtk.FILL)

        self.init_frecuencia(builder.get_object('frecuencia'))
        self.init_fase(builder.get_object('fase'))
        self.init_func_radios(builder)

    def fetch_widgets_from_xml(self, gtk_builder):
        self.window = gtk_builder.get_object('window')
        self.container = gtk_builder.get_object('container')
        self.on_off_btn = gtk_builder.get_object('on_off_btn')
        self.func_config = gtk_builder.get_object('func_config')

    def init_frecuencia(self, frecuencia):
        frecuencia.set_value(self.FRECUENCIA)
        self.frecuencia = frecuencia

    def init_fase(self, fase):
        fase.set_value(self.FASE)
        self.fase = fase

    def init_func_radios(self, gtk_builder):
        for rbutton in ['bhorizontal', 'bvertical', 'func_mate']:
            radio_button = gtk_builder.get_object(rbutton)
            radio_button.connect("toggled", self.on_func_radio_toggled, rbutton)

    def init_matriz_leds(self, mods_horizontales, mods_verticales):
        self.matriz_leds = MatrizLeds(mods_horizontales, mods_verticales, self.FASE)
        self.container.pack_start(self.matriz_leds)
        self.container.reorder_child(self.matriz_leds, 0)
        self.matriz_leds.show_all()

    def on_encender_clicked(self, widget):
        self.on_off_btn.set_label(self.ON_OFF_BTN_OFF)
        self.matriz_leds.set()

    def on_limpiar_clicked(self, widget):
        self.on_off_btn.set_label(self.ON_OFF_BTN_OFF)
        self.matriz_leds.clear()

    def on_off_btn_clicked_cb(self, widget):
        if widget.get_label() == self.ON_OFF_BTN_ON:
            self.matriz_leds.clear()
            widget.set_label(self.ON_OFF_BTN_OFF)
        else:
            self.matriz_leds.restart()
            widget.set_label(self.ON_OFF_BTN_ON)

    def on_frecuencia_value_changed(self, frecuencia):
        if hasattr(self, 'matriz_leds'):
            self.matriz_leds.restart(frecuencia.get_value())

    def on_func_radio_toggled(self, radio_button, data=None):
        if data == 'func_mate':
            if radio_button.get_active():
                self.func_config.show()
            else:
                self.func_config.hide()
        elif radio_button.get_active():
            self.matriz_leds.set_func(radio_button.get_label())

