# -*- coding: UTF-8 -*-

from threading import Thread
from time import sleep
from pprint import pprint

class Funcion(Thread):
	def __init__(self, matriz, callback, fase):
		Thread.__init__(self)
		self.matriz, self.callback, self.fase = matriz, callback, fase
		self.is_running = True

	def run(self):
		while self.is_running:
			self.execute()

	def execute(self):
		pass

	def stop(self):
		self.is_running = False
		self.join()


class Cuadrada(Funcion):
	def __init__(self, matriz, callback, fase):
		super(self.__class__, self).__init__(matriz, callback, fase)
		self.fila, self.columna = 0, 0

	def execute(self):
		self.matriz[self.pos_anterior()] = False
		self.matriz[self.fila, self.columna] = True
		self.matriz.changed()
		# pprint(self.matriz.data)
		self.callback()
		self.pos_siguiente()
		sleep(self.fase)

	def columna_anterior(self):
		return (self.columna if self.columna else self.matriz.columnas)-1

	def fila_anterior(self):
		if self.columna:
			return self.fila
		elif self.fila:
			return self.fila-1
		else:
			return self.matriz.filas-1

	def pos_anterior(self):
		return self.fila_anterior(), self.columna_anterior()

	def columna_sig(self):
		self.columna += 1
		if self.columna == self.matriz.columnas:
			self.columna = 0
		return self.columna

	def fila_sig(self):
		self.fila += 1
		if self.fila == self.matriz.filas:
			self.fila = 0
		return self.fila

	def pos_siguiente(self):
		if not self.columna_sig():
			self.fila_sig()
		return self.fila, self.columna