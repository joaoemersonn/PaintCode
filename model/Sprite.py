import pygame
from util.Util import carrega_imagem, SONS, ESCALAX, ESCALAY
from view.Painel import Painel


class Sprite:
    def __init__(self, nomearquivo, colunas, linhas, escala=None, rotacao=None):
        self.sheet = carrega_imagem(nomearquivo).convert_alpha()
        if escala is not None:
            self.sheet = pygame.transform.smoothscale(self.sheet, (
                int(self.sheet.get_rect().w / escala), int(self.sheet.get_rect().h / escala)))
        if rotacao is not None:
            self.sheet = pygame.transform.rotate(self.sheet, rotacao)
        self.colunas = colunas
        self.spriteativo = self.aux = 0
        self.animacao = None
        self.linhas = linhas
        self.posicaoRelativa = (0, 0)
        self.totalCellCount = colunas * linhas
        self.rect = self.sheet.get_rect()
        self.rect.width = w = self.cellWidth = self.rect.width / colunas
        self.rect.height = h = self.cellHeight = self.rect.height / linhas
        hw, hh = self.cellCenter = (w / 2, h / 2)

        self.cells = list([(index % colunas * w, index / colunas * h, w, h)
                           for index in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ])

    def desenhar(self, surface, cellIndex=-1, x=-1, y=-1, handle=0):
        if not x == y == -1:
            (self.rect.left, self.rect.top) = (x, y)
        if cellIndex == -1:
            cellIndex = self.spriteativo
        if type(surface) == Painel:
            self.posicaoRelativa = surface.get_posicao()
        surface.blit(self.sheet, (self.rect.left + self.handle[handle][0], self.rect.top + self.handle[handle][1]),
                     self.cells[cellIndex])

    def animar(self, surface, tempo, fps=0):
        if tempo <= 0:
            self.spriteativo = 0
        else:
            if self.spriteativo >= len(self.animacao):
                self.spriteativo = 0
            surface.blit(self.sheet, (self.rect.left + self.handle[0][0], self.rect.top + self.handle[0][1]),
                         self.cells[self.animacao[self.spriteativo]])
            self.spriteativo += 1
            return tempo - 1
        return 0

    def desenharBt(self, surface, handle=0):
        if type(surface) == Painel:
            self.posicaoRelativa = surface.get_posicao()
        cellIndex = 0
        if self.colisao_point(pygame.mouse.get_pos()):
            cellIndex = 1
            if self.spriteativo == 0:
                SONS.TICK.play()
            self.spriteativo = 1
        else:
            self.spriteativo = 0
        surface.blit(self.sheet, (self.rect.left + self.handle[handle][0], self.rect.top + self.handle[handle][1]),
                     self.cells[cellIndex])

    def mover(self, posicao):
        self.rect.move_ip((posicao[0], posicao[1]))

    def definirPosicao(self, posicao, escalar=True):
        if escalar:
            (self.rect.left, self.rect.top) = (
                int(posicao[0] * ESCALAX), posicao[1] * ESCALAY)
        else:
            (self.rect.left, self.rect.top) = (posicao[0], posicao[1])

    def colisao_point(self, point):
        if self.rect.collidepoint((point[0] - self.posicaoRelativa[0], point[1] - self.posicaoRelativa[1])):
            return True
        return False

    def mudarImg(self, nomearquivo):
        self.sheet = carrega_imagem(nomearquivo).convert_alpha()

    def colisao_rect(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False
