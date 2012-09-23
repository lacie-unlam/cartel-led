from pprint import pprint

class Matriz:
    CELL_INACTIVE = 0
    CELL_PARTIALLY_ACTIVE = 1
    CELL_FULLY_ACTIVE = 2

    def __init__(self, filas, columnas):
        self._filas, self._columnas = filas, columnas
        self.data = [[False for j in range(columnas)] for i in range(filas*2)]

    @property
    def filas(self):
        return self._filas

    @property
    def columnas(self):
        return self._columnas

    def set(self):
        self.__reset__(self.CELL_FULLY_ACTIVE)

    def clear(self):
        self.__reset__(self.CELL_INACTIVE)

    def each_index(self):
        for i in range(len(self.data)/2):
            for j in range(len(self.data[i])):
                yield i, j

    def __setitem__(self, position, value):
        i, j = position
        i*=2
        if value == self.CELL_PARTIALLY_ACTIVE:
            self.data[i][j] = False
            self.data[i+1][j] = True
        else:
            self.data[i][j] = self.data[i+1][j] = value == self.CELL_FULLY_ACTIVE

    def __getitem__(self, position):
        i, j = position
        i*=2
        if self.data[i][j] == self.data[i+1][j]:
            return self.CELL_FULLY_ACTIVE if self.data[i][j] else self.CELL_INACTIVE
        else:
            return self.CELL_PARTIALLY_ACTIVE

    def __reset__(self, value):
        for i, j in self.each_index():
            self[i, j] = value
        pprint(self.data)
