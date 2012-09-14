# -*- coding: UTF-8 -*-

import gtk

from lib.matriz import Matriz

class MatrizLeds(gtk.VBox):
	def __init__(self, leds_horizontales, leds_verticales):
		super(self.__class__, self).__init__(True)
		self.matriz = Matriz(leds_verticales, leds_horizontales)
		for i in range(leds_verticales):
			hbox = gtk.HBox(True)
			for i in range(leds_horizontales):
				group = gtk.RadioButton()
				hbox.pack_start(gtk.RadioButton(group))
			self.pack_start(hbox)

	def encender(self):
		self.matriz.set()

	def limpiar(self):
		self.matriz.clear()