# -*- coding: UTF-8 -*-

from threading import Thread
from time import sleep
from pprint import pprint

from comm import Serializer
from estructuras import Matriz
from fonts import font

class Funcion(Thread):
	def __init__(self, matriz, callback, frecuencia):
		Thread.__init__(self)
		self.matriz, self.callback, self.frecuencia = matriz, callback, frecuencia
		self.serializer = Serializer(matriz)
		self.is_running = True

	def run(self):
		while self.is_running:
			self.compute()
			self.serializer.write()
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


class Texto(Funcion):
	def __init__(self, matriz, callback, frecuencia, texto):
		super(self.__class__, self).__init__(matriz, callback, frecuencia)
		self.texto = texto
		self.reset_indexes()

	def compute(self):
		for i, l in enumerate(list(self.texto[self.i:self.j])):
			m = self.letter2matrix(l)
			for f in range(m.filas):
				for c in range(m.columnas):
					self.matriz[2+f, (m.columnas)*i+c] = m[f, c]
		self.i += 1
		self.j += 1
		if self.j > len(self.texto):
			self.reset_indexes()

	def letter2matrix(self, letter):
		arr = font(letter) # ['7e', '11', '11', '11', '7e']
		m = Matriz(len(arr[0]*4), len(arr))
		for i, n in enumerate(arr):
			s = ''.join(map(lambda x: bin(int(x, 16))[2:].rjust(4, '0'), list(n)))
			bits = map(lambda x: int(x), list(s))
			for j in range(m.filas):
				m[j, i] = True if bits[j] else False
		# flip it 180º
		for i in range(m.filas/2):
			for j in range(len(m[i])):
				aux = m[i, j]
				m[i, j] = m[m.filas-i-1, j]
				m[m.filas-i-1, j] = aux
		return m

	def reset_indexes(self):
		self.i, self.j = 0, 11


class Demo(Funcion):
	def __init__(self, matriz, callback, frecuencia):
		super(self.__class__, self).__init__(matriz, callback, frecuencia)
		self.row, self.col, self.mode = 0, 0, 'h'

	def compute(self):
		if self.mode == 'h':
			if not self.col:
				prev_col = self.previous_col()
				for f in range(self.matriz.filas):
					self.matriz[f, prev_col] = False
			prev_row = self.previous_row()
			for c in range(self.matriz.columnas):
				self.matriz[prev_row, c] = False
				self.matriz[self.row, c] = True
			self.inc_row()
			if not self.row:
				self.mode = 'v'
		else:
			if not self.row:
				prev_row = self.previous_row()
				for c in range(self.matriz.columnas):
					self.matriz[prev_row, c] = False
			prev_col = self.previous_col()
			for f in range(self.matriz.filas):
				self.matriz[f, prev_col] = False
				self.matriz[f, self.col] = True
			self.inc_col()
			if not self.col:
				self.mode = 'h'

	def previous_row(self):
		return self.row-1 if self.row else self.matriz.filas-1

	def inc_row(self):
		self.row = self.row+1 if self.row < self.matriz.filas-1 else 0

	def previous_col(self):
		return self.col-1 if self.col else self.matriz.columnas-1

	def inc_col(self):
		self.col = self.col+1 if self.col < self.matriz.columnas-1 else 0
		if not self.col:
			self.mode = 'h'
