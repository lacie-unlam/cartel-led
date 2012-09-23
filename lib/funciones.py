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
		self.row, self.partially_active = 0, True

	def compute(self):
		for c in range(self.matriz.columnas):
			self.matriz[self.row, c] = Matriz.CELL_PARTIALLY_ACTIVE if self.partially_active else Matriz.CELL_FULLY_ACTIVE

		if self.partially_active:
			for c in range(self.matriz.columnas):
				self.matriz[self.row-1 if self.row else self.matriz.filas-1, c] = Matriz.CELL_INACTIVE
		else:
			self.row = self.row+1 if self.row < self.matriz.filas-1 else 0

		self.partially_active = not self.partially_active


class BVertical(Funcion):
	def __init__(self, matriz, callback, frecuencia):
		super(self.__class__, self).__init__(matriz, callback, frecuencia)
		self.col = 0

	def compute(self):
		for f in range(self.matriz.filas):
			self.matriz[f, self.col-1 if self.col else self.matriz.columnas-1] = Matriz.CELL_INACTIVE
			self.matriz[f, self.col] = Matriz.CELL_FULLY_ACTIVE

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