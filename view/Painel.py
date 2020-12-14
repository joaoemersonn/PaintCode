import pygame


class Painel(pygame.Surface):

    def __init__(self, largura, altura, x=0, y=0):
        super().__init__((largura,altura),flags=pygame.SRCALPHA)
        self.__posicao = (x, y)
        (self.__largura, self.__altura) = (largura, altura)

    def get_posicao(self):
        return self.__posicao

    def get_altura(self):
        return self.__altura

    def get_largura(self):
        return self.__largura

