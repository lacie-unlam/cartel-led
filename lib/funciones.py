# -*- coding: UTF-8 -*-

from threading import Thread
from time import sleep
from pprint import pprint

from lib.estructuras import Matriz

class Funcion(Thread):
	def __init__(self, matriz, callback, frecuencia):
		Thread.__init__(self)
		self.matriz, self.callback, self.frecuencia = matriz, callback, frecuencia
		self.is_running = True

	def run(self):
		while self.is_running:
			self.compute()
			self.callback()
			sleep(self.frecuencia)

	def compute(self):
		pass

	def stop(self):
		self.is_running = False
		self.join()


class BHorizontal(Funcion):
	def __init__(self, matriz, callback, frecuencia):
		super(self.__class__, self).__init__(matriz, callback, frecuencia)
		self.row = 0

	def compute(self):
		prev_row = self.previous_row()
		for c in range(self.matriz.columnas):
			self.matriz[prev_row, c] = False
			self.matriz[self.row, c] = True

		self.inc_row()

	def previous_row(self):
		return self.row-1 if self.row else self.matriz.filas-1

	def inc_row(self):
		self.row = self.row+1 if self.row < self.matriz.filas-1 else 0


class BVertical(Funcion):
	def __init__(self, matriz, callback, frecuencia):
		super(self.__class__, self).__init__(matriz, callback, frecuencia)
		self.col = 0

	def compute(self):
		prev_col = self.previous_col()
		for f in range(self.matriz.filas):
			self.matriz[f, prev_col] = False
			self.matriz[f, self.col] = True

		self.inc_col()

	def previous_col(self):
		return self.col-1 if self.col else self.matriz.columnas-1

	def inc_col(self):
		self.col = self.col+1 if self.col < self.matriz.columnas-1 else 0


# class Cuadrada(Funcion):
# 	def __init__(self, matriz, callback, fase):
# 		super(self.__class__, self).__init__(matriz, callback, fase)
# 		self.fila, self.columna = 0, 0

# 	def execute(self):
# 		self.matriz[self.pos_anterior()] = False
# 		self.matriz[self.fila, self.columna] = True
# 		self.matriz.changed()
# 		# pprint(self.matriz.data)
# 		self.callback()
# 		self.pos_siguiente()
# 		sleep(self.fase)

# 	def columna_anterior(self):
# 		return (self.columna if self.columna else self.matriz.columnas)-1

# 	def fila_anterior(self):
# 		if self.columna:
# 			return self.fila
# 		elif self.fila:
# 			return self.fila-1
# 		else:
# 			return self.matriz.filas-1

# 	def pos_anterior(self):
# 		return self.fila_anterior(), self.columna_anterior()

# 	def columna_sig(self):
# 		self.columna += 1
# 		if self.columna == self.matriz.columnas:
# 			self.columna = 0
# 		return self.columna

# 	def fila_sig(self):
# 		self.fila += 1
# 		if self.fila == self.matriz.filas:
# 			self.fila = 0
# 		return self.fila

# 	def pos_siguiente(self):
# 		if not self.columna_sig():
# 			self.fila_sig()
# 		return self.fila, self.columna