# -*- coding: UTF-8 -*-

import gobject
import gtk
from threading import Timer

from lib.estructuras import Matriz
from lib.funciones import Cuadrada

class ComboFunciones:
    SENO = 'Seno'
    TRIANGULAR = 'Triangular'
    CUADRADA = 'Cuadrada'

    def __init__(self):
        self.combobox = gtk.combo_box_new_text()
        self.model = self.combobox.get_model()
        self.append(self.CUADRADA)
        self.append(self.SENO)
        self.append(self.TRIANGULAR)
        self.combobox.set_active(0)
        
    def append(self, txt):
        self.combobox.append_text(txt)

    def get_active_text(self):
        active = self.combobox.get_active()
        if active < 0:
            return None
        return self.model[active][0]

    def get_widget(self):
        return self.combobox


class MatrizLeds(gtk.VBox):
    def __init__(self, leds_horizontales, leds_verticales):
        super(self.__class__, self).__init__(True)
        gobject.threads_init()
        self.matriz = Matriz(leds_verticales, leds_horizontales)
        
        for i in range(leds_verticales):
            hbox = gtk.HBox(True)
            for i in range(leds_horizontales):
                hbox.pack_start(gtk.CheckButton())
            self.pack_start(hbox)

        self.start()

    def set(self):
        self.destroy()
        self.matriz.set()
        self.update_ui()
        Timer(5, self.clear).start()

    def clear(self):
        self.destroy()
        self.matriz.clear()
        self.update_ui()

    def update_ui(self):
        for i, j in self.matriz.each_index():
            self.get_children()[i].get_children()[j].set_active(self.matriz[i, j])

    def destroy(self):
        if self.funcion.is_alive():
            self.funcion.stop()

    def start(self):
        self.funcion = Cuadrada(self.matriz, lambda: gobject.idle_add(self.update_ui))
        self.funcion.start()