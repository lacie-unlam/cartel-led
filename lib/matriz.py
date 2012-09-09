class Matriz:
    def __init__(self, filas, columnas):
        self.data = [[False for j in range(columnas)] for i in range(filas)]

    def set(self):
        self.__reset__(True)

    def clear(self):
        self.__reset__(False)

    def __reset__(self, value):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = value