class Matriz:
    def __init__(self, filas, columnas):
        self._filas, self._columnas = filas, columnas
        self.data = [[False for j in range(columnas)] for i in range(filas)]

    @property
    def filas(self):
        return self._filas

    @property
    def columnas(self):
        return self._columnas

    def set(self):
        self.__reset__(True)

    def clear(self):
        self.__reset__(False)

    def each_index(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                yield i, j

    def __setitem__(self, position, value):
        i, j = position
        self.data[i][j] = value

    def __getitem__(self, position):
        i, j = position
        return self.data[i][j]

    def __reset__(self, value):
        for i, j in self.each_index():
            self.data[i][j] = value