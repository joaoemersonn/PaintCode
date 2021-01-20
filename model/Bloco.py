import pygame
from pygame.constants import PREALLOC

from view.Painel import Painel
from util.Util import ESCALAY, ESCALAX, carregar_imagem_blocos
from util import Util
from view.PainelJogo import contornarRect, escalar, escalarX, escalarY


class Bloco:
    def __init__(self, tipo, value=0):
        self.imagem = carregar_imagem_blocos(str(tipo) + ".png")
        self.imagem = pygame.transform.scale(self.imagem,
                                             (int(self.imagem.get_rect().w / 2), int(self.imagem.get_rect().h / 2)))
        self.__tipo = tipo
        self.blocos = None
        self.pressionado = False
        self.Value = value
        self.posicaoRelativa = (0, 0)
        self.rect = self.imagem.get_rect()
        self.selecionado = False
        #self.seta1 = self.seta2 = None
        if type(value) is not int:
            self.atualizaImgMover()

    def atualizaImgMover(self):
        self.imagem = carregar_imagem_blocos(str(self.Value) + ".png")
        self.imagem = pygame.transform.scale(self.imagem,
                                             (int(self.imagem.get_rect().w / 2), int(self.imagem.get_rect().h / 2)))
        self.rect = self.imagem.get_rect()

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def get_Valor(self):
        return self.Value

    def set_Valor(self, value):
        self.Value = value

    def get_tipo(self):
        return self.__tipo

    def desenhar(self, surface, x=-1, y=-1):
        if not x == y == -1:
            (self.rect.left, self.rect.top) = (x, y)
        if type(surface) == Painel:
            self.posicaoRelativa = surface.get_posicao()
        if self.pressionado:
            (self.rect.centerx, self.rect.centery) = (pygame.mouse.get_pos())
        surface.blit(self.imagem, self.rect)
        if self.__tipo == "selecionar_cor":
            pos = self.get_rect()
            pygame.draw.rect(surface, Util.get_cor(self.get_Valor()),
                             (pos.x + escalarX(28), pos.y + escalarY(23), escalarX(25), escalarY(25)))
            contornarRect(surface, (pos.x + escalarX(28), pos.y +
                                    escalarY(23), escalarX(25), escalarY(25)))

    def definirPosicao(self, posicao):
        (self.rect.left, self.rect.top) = (
            posicao[0]*ESCALAX, posicao[1]*ESCALAY)

    def colisao_point(self, point):
        if self.rect.collidepoint((point[0] - self.posicaoRelativa[0], point[1] - self.posicaoRelativa[1])):
            return True
        return False

    def colisao_rect(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False
