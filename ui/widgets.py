# -*- coding: UTF-8 -*-

import gobject
import gtk
import math
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
    def __init__(self, leds_horizontales, leds_verticales, fase):
        super(self.__class__, self).__init__(True)
        gobject.threads_init()
        self.matriz = Matriz(leds_verticales, leds_horizontales)
        
        for i in range(leds_verticales):
            hbox = gtk.HBox(True)
            for j in range(leds_horizontales):
                hbox.pack_start(self.new_led(), padding=2)
            self.pack_start(hbox)

        self.start(fase)

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

    def start(self, fase):
        self.funcion = Cuadrada(self.matriz, lambda: gobject.idle_add(self.update_ui), fase)
        self.funcion.start()

    def new_led(self):
        led = LED(self)
        led.set_color('off', [1,0,0]) # red
        led.set_color('on', [124,252,0]) # green
        led.set_dia(5)
        return led


# This creates the custom LED widget
class LED(gtk.DrawingArea):
    def __init__(self, parent):
        self.par = parent       
        super(LED, self).__init__() 
        self._dia = 10
        self._state = 0
        self._on_color = [0.3, 0.4, 0.6]
        self._off_color = [0.9, 0.1, 0.1]
        # self.set_size_request(25, 25)
        self.connect("expose-event", self.expose)
        
    # This method draws our widget
    # it draws a black circle for a rim around LED
    # Then depending on self.state
    # fills in that circle with on or off colour.
    # the diameter depends on self.dia
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        cr.set_line_width(3)
        cr.set_source_rgb(0, 0, 0.0)    
        self.set_size_request(self._dia*2+5, self._dia*2+5)           
        w = self.allocation.width
        h = self.allocation.height
        cr.translate(w/2, h/2)
        cr.arc(0, 0, self._dia, 0, 2*math.pi)
        cr.stroke_preserve()
        if self._state:
            cr.set_source_rgb(self._on_color[0],self._on_color[1],self._on_color[2])
        else:
            cr.set_source_rgb(self._off_color[0],self._off_color[1],self._off_color[2])
        cr.fill()
        
        return False
      
    # This sets the LED on or off
    # and then redraws it
    # Usage: ledname.set_active(True) 
    def set_active(self, data):
        self._state = data
        self.queue_draw()
    
    # This allows setting of the on and off colour
    # red,green and blue are float numbers beteen 0 and 1
    # Usage: ledname.set_color("off",[r,g,b])

    def set_color(self, state, color = [0,0,0]):
        if state == "off":
            self._off_color = color
        elif state == "on":
            self._on_color = color
        else:
            return
    # This alows setting the diameter of the LED
    # Usage: ledname.set_dia(10)
    def set_dia(self, dia):
        self._dia = dia
        self.queue_draw()