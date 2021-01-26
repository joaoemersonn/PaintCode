import pygame
from util.Util import carrega_imagem, SONS


class Pincel:
    def __init__(self):
        self.posicaoX = 0
        self.posicaoY = 0
        self.cor = 1
        self.image = pygame.transform.rotate(
            carrega_imagem("pincel" + str(self.cor) + ".png"), 0)
        self.rotacao = 0

    def posicaoInicial(self):
        self.posicaoX = 0
        self.posicaoY = 0
        self.rotacao = 0
        self.image = pygame.transform.rotate(carrega_imagem("pincel1.png"), 0)
        self.cor = 1

    def mover(self, comando, desenho, controller=None):
        x = comando
        if x is not None:
            if self.rotacao < 0:
                self.rotacao += 360
            if self.rotacao > 360:
                self.rotacao -= 360
            if x.get_tipo() == "mover":
                SONS.MOVE.play()
                if self.rotacao == 90 and self.posicaoX < desenho.colunas - 1 and int(desenho.tiles[self.posicaoX + 1][
                        self.posicaoY]) >= 0:
                    self.posicaoX += 1
                elif self.rotacao == 180 and self.posicaoY > 0 and int(desenho.tiles[self.posicaoX][self.posicaoY - 1]) >= 0:
                    self.posicaoY -= 1
                elif (self.rotacao == 360 or self.rotacao == 0) and self.posicaoY < desenho.linhas - 1 and \
                        int(desenho.tiles[self.posicaoX][self.posicaoY + 1]) >= 0:
                    self.posicaoY += 1
                elif self.rotacao == 270 and self.posicaoX > 0 and int(desenho.tiles[self.posicaoX - 1][self.posicaoY]) >= 0:
                    self.posicaoX -= 1

            elif x.get_tipo() == "girar_esquerda":
                SONS.MOVE.play()
                self.image = pygame.transform.rotate(self.image, 90)
                self.rotacao += 90
            elif x.get_tipo() == "girar_direita":
                SONS.MOVE.play()
                self.image = pygame.transform.rotate(self.image, -90)
                self.rotacao -= 90
            elif x.get_tipo() == "pintar":
                SONS.PAINT.play()
                desenho.tiles[self.posicaoX][self.posicaoY] = self.cor
            elif x.get_tipo() == "selecionar_cor":
                SONS.COLORCHANGE.play()
                self.cor = x.get_Valor()
                self.image = pygame.transform.rotate(
                    carrega_imagem("pincel" + str(self.cor) + ".png"), self.rotacao)
            elif x.get_tipo() == "repetir" and x.blocos is not None:
                for j in range(0, x.get_Valor()):
                    for bloc in x.blocos:
                        if controller is not None:
                            controller.refreshDesenho()
                            self.mover(bloc, desenho)
                            pygame.time.delay(100)
                        else:
                            self.mover(bloc, desenho)
            elif x.get_tipo() == "blocoF" and x.blocos is not None:
                for bloc in x.blocos:
                    if controller is not None:
                        controller.refreshDesenho()
                        self.mover(bloc, desenho)
                        pygame.time.delay(100)
                    else:
                        self.mover(bloc, desenho)
