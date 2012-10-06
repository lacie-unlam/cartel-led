# -*- coding: UTF-8 -*-

import gobject
import gtk
import math
import re
from threading import Timer

from lib.estructuras import Matriz
from lib import funciones
from lib.comm import Serializer

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
    PADDING = 2

    def __init__(self, mods_horizontales, mods_verticales, frecuencia):
        super(self.__class__, self).__init__(homogeneous=True)
        gobject.threads_init()
        self.mods_horizontales, self.mods_verticales = mods_horizontales, mods_verticales
        self.frecuencia = frecuencia
        self.matriz = Matriz(mods_verticales*ModuloLeds.CANT_LEDS_X_COL, mods_horizontales*ModuloLeds.CANT_LEDS_X_FILA)
        
        for i in range(mods_verticales):
            hbox = gtk.HBox(True)
            for j in range(mods_horizontales):
                hbox.pack_start(ModuloLeds(), padding=self.PADDING)
            self.pack_start(hbox, padding=self.PADDING)

        self.start()

    def set(self):
        self.destroy()
        self.matriz.set()
        self.serialize()
        self.update_ui()
        Timer(5, self.clear).start()

    def clear(self):
        self.destroy()
        self.matriz.clear()
        self.serialize()
        self.update_ui()

    def update_ui(self):
        for v in range(self.mods_verticales):
            for f in range(ModuloLeds.CANT_LEDS_X_COL):
                for h in range(self.mods_horizontales):
                    for c in range(ModuloLeds.CANT_LEDS_X_FILA):
                        self.get_children()[v].get_children()[h][f, c] = self.matriz[f+v*ModuloLeds.CANT_LEDS_X_COL, c+h*ModuloLeds.CANT_LEDS_X_FILA]

    def destroy(self):
        self.funcion.stop()

    def start(self, func=funciones.BHorizontal, data=None):
        self.func = [func, data]
        params = [self.matriz, lambda: gobject.idle_add(self.update_ui), self.frecuencia, data]
        self.funcion = func(*filter(None, params))
        self.funcion.start()

    def restart(self, **kwargs):
        self.clear()
        if kwargs.has_key('frecuencia'):
            self.frecuencia = kwargs['frecuencia']
        if kwargs.has_key('data'):
            self.func[1] = kwargs['data']
        self.start(*self.func)


    def set_func(self, func, data=None):
        self.clear()
        if re.search(r'horizontal$', func, re.IGNORECASE):
            funcion = funciones.BHorizontal
        elif re.search(r'vertical$', func, re.IGNORECASE):
            funcion = funciones.BVertical
        elif re.search(r'demo$', func, re.IGNORECASE):
            funcion = funciones.Demo
        else:
            funcion = funciones.Texto
        self.start(funcion, data)
        
    def serialize(self):
        Serializer(self.matriz).write()


class ModuloLeds(gtk.Table):
    CANT_LEDS_X_FILA = 8
    CANT_LEDS_X_COL = 4
    PADDING = 1

    def __init__(self):
        super(self.__class__, self).__init__(self.CANT_LEDS_X_COL, self.CANT_LEDS_X_FILA, homogeneous=True)
        self.activos = Matriz(self.CANT_LEDS_X_COL, self.CANT_LEDS_X_FILA)
        self.inactivos = Matriz(self.CANT_LEDS_X_COL, self.CANT_LEDS_X_FILA)
        # self.matriz = Matriz(self.CANT_LEDS_X_COL, self.CANT_LEDS_X_FILA)
        for i in range(self.CANT_LEDS_X_COL):
            for j in range(self.CANT_LEDS_X_FILA):
                activo = gtk.RadioButton()
                self.activos[i, j] = activo
                inactivo = gtk.RadioButton(activo)
                self.inactivos[i, j] = inactivo
                self.attach(inactivo, j, j+1, i, i+1, xpadding=self.PADDING, ypadding=self.PADDING)
                # led = LED(self)
                # self.matriz[i, j] = led
                # self.attach(led, j, j+1, i, i+1, xpadding=self.PADDING, ypadding=self.PADDING)

    def __setitem__(self, position, value):
        i, j = position
        self.activos[i, j].set_active(not value)
        self.inactivos[i, j].set_active(value)
        # self.matriz[i, j].set_active(value)        


# This creates the custom LED widget
class LED(gtk.DrawingArea):
    def __init__(self, parent):
        self.par = parent       
        super(LED, self).__init__() 
        self._dia = 5
        self._state = 0
        self._on_color = [124, 252, 0] # red
        self._off_color = [1, 0, 0] # green
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
