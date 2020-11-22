class Jogador:
    def __init__(self,nome="",nivel=0):
        self.__nome = nome
        self.__nivel = nivel


    def getNome(self):
        return self.__nome

    def setNome(self,nome):
        self.__nome = nome

    def getNivel(self):
        return self.__nivel

    def setNivel(self, nivel):
        self.__nivel = nivel
    def subirNivel(self):
        self.__nivel += 1