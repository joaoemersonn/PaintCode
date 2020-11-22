import os
import pygame
import pygame.gfxdraw
from model.Sprite import Sprite
from util import Util
from util.Util import Cores, get_cor
from view.Painel import Painel
from util.Util import carrega_imagem


def contornar(superfice, x, y, largura, altura, tam=2, cor=Cores.CORSECUNDARIA):
    x -= tam / 2
    y -= tam / 2
    largura += tam
    altura += tam
    # linha cima
    pygame.draw.line(superfice, cor, (x, y), ((x + largura), y), tam)
    # linha baixo
    pygame.draw.line(superfice, cor, (x, y + altura), ((x + largura), y + altura), tam)
    # linha esquerda
    pygame.draw.line(superfice, cor, (x, y), (x, y + altura), tam)
    # linha direita
    pygame.draw.line(superfice, cor, (x + largura, y), (x + largura, y + altura), tam)


def contornarRect(superfice, rect, cor=Cores.CORSECUNDARIA):
    pygame.gfxdraw.rectangle(superfice, rect, cor)


class PainelJogo(Painel):

    def __init__(self, tela, largura, altura, x=0, y=0):
        super().__init__(largura, altura, x, y)
        self.__tela = tela
        fontearquivo = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "")
        fontearquivo = os.path.join(fontearquivo, "lib")
        fontearquivo = os.path.join(fontearquivo, "FreeSansBold.ttf")
        self.fontetipo = 'comicsansms'
        self.botaoVoltar = Sprite("VOLTAR.png", 1, 2)
        self.botaoSalvar = Sprite("BOTAOPROX.PNG", 1, 2)
        self.maoCursor = Sprite("cursor.png", 1, 2)
        self.__janela = carrega_imagem("janela.png")
        self.__janela2 = pygame.transform.scale(self.__janela, (60, 60))
        self.__tinta = carrega_imagem("tinta.png", "", 2)
        self.__corTelhado = Cores.TELHADO
        self.__executarButton = Sprite("executar.png", 1, 2)
        self.reiniciarbotao = Sprite("reiniciar.png", 1, 2)
        self.__seta = Sprite("seta.png", 1, 2)
        self.__seta2 = Sprite("seta.png", 1, 2)
        self._img3 = carrega_imagem("03.png", "blocos")
        self._img2 = carrega_imagem("02.png", "blocos")
        self._img1 = carrega_imagem("01.png", "blocos")
        self.__seta2.sheet = pygame.transform.rotate(self.__seta2.sheet, 180)
        self.__executarButton.definirPosicao((980, 550))
        self.botaoVoltar.definirPosicao((1080, 570))
        self.botaoSalvar.definirPosicao((810, 570))
        self.reiniciarbotao.definirPosicao((960, 25))
        self.__boxExecucao = pygame.rect.Rect(20, 550, 950, 100)
        self.fontePequena = pygame.font.Font(fontearquivo, 20 - 8)
        self.fonten = pygame.font.Font(fontearquivo, 25 - 8)
        self.fonteg = pygame.font.Font(fontearquivo, 40 - 8)
        self.fontexg = pygame.font.Font(fontearquivo, 60 - 8)
        self.back = carrega_imagem("back.png")
        self.exibeAviso = False
        self.destaque = False
        self.c3 = carrega_imagem("c3.png")
        self.textoaviso = "", ""  # self.tituloaviso = ""
        self.desenharGuiaDesenhoBoolean = False
        self.guiDesenhoRect = pygame.rect.Rect(40, 320, 300, 200)
        self.criando = self.finalizacriacao = False
        self.imgPincel = pygame.transform.rotate(carrega_imagem("pincel" + str(1) + ".png", escala=2), 45)
        self.confete = Sprite("confete.png",1,59)
        self.confete2 = Sprite("confete.png",1,59)
        self.confete3 = Sprite("confete2.png",1,59)
        self.confete4 = Sprite("confete2.png",1,59)
        self.confete.definirPosicao((-100,450))
        self.confete2.definirPosicao((1100,450))
        self.confete3.definirPosicao((-100,-150))
        self.confete4.definirPosicao((1100,-150))
        self.confete.animacao = [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
        self.confete2.animacao = self.confete3.animacao = self.confete4.animacao = self.confete.animacao
        self.tempoAnGanhou = 0
        self.fase = None
        self.contornoFase = Sprite("contorno4.png",1,2)
        # CORESEDICAO
        self.coresEdicao = list()
        self.coresEdicao.append(pygame.Rect(790 + self.__tela.ajuste, 115, 75, 75))
        self.coresEdicao.append(pygame.Rect(700 + self.__tela.ajuste, 115, 75, 75))
        self.coresEdicao.append(pygame.Rect(875 + self.__tela.ajuste, 30, 75, 75))
        self.coresEdicao.append(pygame.Rect(790 + self.__tela.ajuste, 30, 75, 75))
        self.coresEdicao.append(pygame.Rect(700 + self.__tela.ajuste, 30, 75, 75))

    def desenhar(self, fase, jogador=None, comando=None, pincel=None,alerta = False):
        if not alerta:
            self.fase = fase
            desenho = fase.desenhoDesafio
            self.__tela.jogoPane.fill(self.__tela.corfundo)

            self.botaoVoltar.desenharBt(self)
            self.desenharDesenho(desenho, pincel)
            if not self.criando:
                self.reiniciarbotao.desenharBt(self)
                self.desenharDesenhoGuia(fase.desenhoResposta)
                self.desenharCaixaExecucao(comando, fase)
                self.desenharCaixaBlocos(fase)
                self.desenharInfo(fase, jogador)

            else:
                self.botaoSalvar.desenharBt(self)
                self.desenharFerramentasEdicao()
                self.desenharPincelWidget()
            if self.exibeAviso:
                self.aviso(self.textoaviso[0], self.textoaviso[1])
    def desenharAnimacaoWin(self,fase,jogador,comando,pincel,fps=0):
        if self.tempoAnGanhou > 0:
             self.__tela.jogoPane.desenhar(fase,jogador,comando,pincel=pincel)
        self.tempoAnGanhou = self.confete.animar(self, self.tempoAnGanhou, fps=fps)
        self.tempoAnGanhou = self.confete2.animar(self, self.tempoAnGanhou, fps=fps)
        self.tempoAnGanhou = self.confete3.animar(self, self.tempoAnGanhou, fps=fps)
        self.tempoAnGanhou = self.confete4.animar(self, self.tempoAnGanhou, fps=fps)

    def desenharInfo(self, fase, jogador):
        cor = Cores.BRANCO
        self.blit(self.__tinta, (20, 20))
        if jogador is not None:
            nome = self.fontePequena.render(("Jogador: " + jogador.getNome()), True, cor)
            faserender = self.fontePequena.render(("Fase: " + str(fase.nivel)), True, cor)
            self.blit(nome, (70, 40))
            self.blit(faserender, (70, 60))
        tentativas = self.fonten.render("Tentativas Restantes:", True, cor)
        if self.destaque:
            tentativas2 = self.fontexg.render(str(fase.tentativas), True, cor)
        else:
            tentativas2 = self.fonteg.render(str(fase.tentativas), True, cor)
        self.blit(tentativas, (70, 90))
        self.blit(tentativas2, (150, 110))

    def aviso(self, titulo, texto):
        self.blit(self.c3,(400, 200, 500, 150))
        titulor = self.fonteg.render(titulo, True, Cores.VERMELHO)
        textor = self.fonten.render(texto, True, Cores.PRETO)
        self.blit(titulor, (520, 300))
        self.blit(textor, (470, 400))

    def trocarimgPincel(self, num):
        if num >= 0:
            self.imgPincel = pygame.transform.rotate(carrega_imagem("pincel" + str(num) + ".png", escala=2), 45)
        else:
            self.imgPincel = carrega_imagem("janela.png", escala=2)

    def desenharPincelWidget(self):
        pos = pygame.mouse.get_pos()
        self.blit(self.imgPincel, (pos[0] | +5, pos[1] + 5))

    def desenharVerificacao(self,i,j,janela=False,passou= True):
        inty = 30
        intx = 150
        if not passou:
            pygame.draw.rect(self, Util.get_cor(4),
                             ((self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75))
        contornar(self, (self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75, 5)

    def desenharDesenho(self, desenho, pincel):
        inty = 30
        intx = 150
        self.blit(self.back, (20, 20))
        pygame.gfxdraw.filled_trigon(self, int(self.__tela.ajuste / 2) + intx + 85 + int((75 * desenho.colunas) / 2),
                                     inty + 30,
                                     int(self.__tela.ajuste / 2) + intx + 80, 85 + inty,
                                     int(self.__tela.ajuste / 2) + intx + 90 + 75 * desenho.colunas,
                                     85 + inty, self.__corTelhado)
        for i in range(0, desenho.colunas):
            for j in range(0, desenho.linhas):
                if int(desenho.tiles[i][j]) >= 0:
                    pygame.draw.rect(self, Util.get_cor(int(desenho.tiles[i][j])),
                                     ((self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75))
                else:
                    self.blit(self.__janela,
                              ((self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75))
                contornar(self, (self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75, 1)
        contornar(self, (self.__tela.ajuste / 2) + intx + 85, inty + 85, 75 * desenho.colunas, 75 * desenho.linhas)
        if not self.criando:
            self.blit(pincel.image,
                      (
                          (self.__tela.ajuste / 2) + intx + 85 + (75 * pincel.posicaoX),
                          85 + inty + (75 * pincel.posicaoY),
                          75,
                          75))

    def desenharCaixaExecucao(self, comando, fase):
        pygame.gfxdraw.box(self, self.__boxExecucao, Cores.BRANCO)
        contornar(self, self.__boxExecucao.x, self.__boxExecucao.y, self.__boxExecucao.w, self.__boxExecucao.h)
        self.__executarButton.desenharBt(self)
        y = 565
        xspace = -60
        img1 = self._img1
        img2 = self._img2
        img1 = pygame.transform.scale(img1, (int(img1.get_rect().w / 2), int(img1.get_rect().h / 2)))
        img2 = pygame.transform.scale(img2, (int(img2.get_rect().w / 2), int(img2.get_rect().h / 2)))
        for x in comando:
            if x.get_tipo() == "repetir":
                numRepet = self.fontePequena.render(str(x.get_Valor()), True, Cores.CORSECUNDARIA)
                x.definirPosicao((xspace + 83, y - 15))
                self.blit(img1, (xspace + 83, y - 15, img1.get_rect().w, img1.get_rect().h))
                if x.blocos is not None:
                    for bl in x.blocos:
                        img = self._img3
                        img = pygame.transform.scale(img, (int(img.get_rect().w / 2), int(img.get_rect().h / 2)))
                        aux = self._img3
                        aux = pygame.transform.scale(aux, (int(aux.get_rect().w / 2), int(aux.get_rect().h / 2)))
                        self.blit(img, (xspace + 123, y - 14))
                        self.blit(aux, (xspace + 143, y - 14))
                        bl.definirPosicao((xspace + 115, y))
                        bl.desenhar(self)
                        if bl.get_tipo() == "selecionar_cor":
                            pos = bl.get_rect()
                            pygame.draw.rect(self, Util.get_cor(bl.get_Valor()), (pos.x + 28, pos.y + 23, 25, 25))
                            contornarRect(self, (pos.x + 28, pos.y + 23, 25, 25))
                            if bl.get_Valor() < 0:
                                pygame.draw.rect(self, Cores.BRANCO, (pos.x, pos.y + 75, 80, 40))
                                contornarRect(self, (pos.x, pos.y + 75, 80, 40))
                                vl = 0
                                for cor in fase.coresdisponiveis:
                                    pygame.draw.rect(self, Util.get_cor(cor),
                                                     (pos.x + 5 + 16 * vl, pos.y + 87, 15, 15))
                                    contornarRect(self, (pos.x + 5 + 16 * vl, pos.y + 87, 15, 15))
                                    vl += 1
                        xspace += bl.get_rect().w - 12
                    x.set_rect(pygame.rect.Rect(x.get_rect().x, x.get_rect().y, (65 * x.blocos.__len__()) + 105,
                                                img2.get_rect().h))
                    self.blit(img2, (xspace + 60, y - 15))

                    self.blit(numRepet, (xspace + 147, y + 70))

                    self.__seta.definirPosicao((xspace + 120, x.get_rect().y + x.get_rect().h - 25))
                    x.seta1 = pygame.rect.Rect(xspace + 120, x.get_rect().y + x.get_rect().h - 25, self.__seta.rect.w,
                                               self.__seta.rect.h)
                    self.__seta2.definirPosicao((xspace + 162,
                                                 x.get_rect().y + x.get_rect().h - 25))
                    x.seta2 = pygame.rect.Rect(xspace + 162,
                                               x.get_rect().y + x.get_rect().h - 25, self.__seta2.rect.w,
                                               self.__seta2.rect.h)
                    if self.__seta.colisao_point(pygame.mouse.get_pos()):
                        self.__seta.desenhar(self, 1)
                    else:
                        self.__seta.desenhar(self, 0)

                    if self.__seta2.colisao_point(pygame.mouse.get_pos()):
                        self.__seta2.desenhar(self, 0)
                    else:
                        self.__seta2.desenhar(self, 1)
                else:
                    self.blit(img2, (xspace + 123, y - 15))
                    self.blit(numRepet, (xspace + 210, y + 70))
                    xspace += 65
                xspace += 100
            else:
                x.definirPosicao((xspace + 80, y))
                xspace += x.get_rect().w - 15
                x.desenhar(self)
                if x.get_tipo() == "selecionar_cor":
                    pos = x.get_rect()
                    pygame.draw.rect(self, Util.get_cor(x.get_Valor()), (pos.x + 28, pos.y + 23, 25, 25))
                    contornarRect(self, (pos.x + 28, pos.y + 23, 25, 25))
                    if x.get_Valor() < 0:
                        pygame.draw.rect(self, Cores.BRANCO, (pos.x, pos.y + 75, 80, 40))
                        contornarRect(self, (pos.x, pos.y + 75, 80, 40))
                        vl = 0
                        for cor in fase.coresdisponiveis:
                            pygame.draw.rect(self, Util.get_cor(cor), (pos.x + 5 + 16 * vl, pos.y + 87, 15, 15))
                            contornarRect(self, (pos.x + 5 + 16 * vl, pos.y + 87, 15, 15))
                            vl += 1
            if x.get_tipo() != "inicio" and x.colisao_point(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                0] and not self.__seta2.colisao_point(pygame.mouse.get_pos()) and not self.__seta.colisao_point(
                pygame.mouse.get_pos()):
                repetajuste = 0
                if x.get_tipo() == "repetir":
                    repetajuste = -30
                print(x.get_rect().top, x.get_rect().left + x.get_rect().height)
                pygame.draw.line(self, Cores.VERMELHO, (x.get_rect().x, x.get_rect().y), (
                    x.get_rect().x + x.get_rect().width, x.get_rect().y + x.get_rect().height + repetajuste), 5)
                pygame.draw.line(self, Cores.VERMELHO, (x.get_rect().x + x.get_rect().width, x.get_rect().y),
                                 (x.get_rect().x, x.get_rect().y + x.get_rect().height + repetajuste), 5)

    def desenharCaixaBlocos(self, fase):
        pygame.gfxdraw.box(self, (680 + self.__tela.ajuste, 20, 300, 510), Cores.BRANCO)
        contornar(self, 680 + self.__tela.ajuste, 20, 300, 510)
        x = fase.blocosdisponiveis
        xspace = 300
        ajustex = ajustey = 0
        mousep = pygame.mouse.get_pos()
        mouseV = True
        for i in range(0, fase.blocosdisponiveis.__len__()):
            x[i].definirPosicao((680 + ajustex + self.__tela.ajuste, 30 + ajustey))
            x[i].desenhar(self)
            if x[i].get_tipo() == "selecionar_cor":
                pos = x[i].get_rect()
                pygame.draw.rect(self, Util.get_cor(x[i].get_Valor()), (pos.x + 28, pos.y + 23, 25, 25))
                contornarRect(self, (pos.x + 28, pos.y + 23, 25, 25))
                if x[i].get_Valor() < 0:
                    pygame.draw.rect(self, Cores.BRANCO, (pos.x, pos.y + 75, 80, 40))
                    contornarRect(self, (pos.x, pos.y + 75, 80, 40))
                    vl = 0
                    for cor in fase.coresdisponiveis:
                        pygame.draw.rect(self, Util.get_cor(cor), (pos.x + 5 + 16 * vl, pos.y + 87, 15, 15))
                        contornarRect(self, (pos.x + 5 + 16 * vl, pos.y + 87, 15, 15))
                        vl += 1
            xspace -= x[i].get_rect().w
            if i + 1 < x.__len__() and xspace <= x[i + 1].get_rect().w:
                ajustey += 100
                ajustex = 0
                xspace = 300
            else:
                ajustex += x[i].get_rect().w
            if x[i].colisao_point(mousep):
                mouseV = False
                if pygame.mouse.get_pressed()[0]:
                    self.maoCursor.desenhar(self, 1, mousep[0], mousep[1])
                else:
                    self.maoCursor.desenhar(self, 0, mousep[0], mousep[1])
        #pygame.mouse.set_visible(mouseV)

    def desenharDesenhoGuia(self, desenho, escala=30):
        if escala != self.__janela2.get_rect().h:
            self.__janela2 = pygame.transform.scale(self.__janela, (escala, escala))
        inty = 250
        intx = -200
        aux = auxX = 0
        if desenho.colunas <= 3: auxX = 60
        if desenho.linhas < 4: aux = 60
        self.contornoFase.definirPosicao((intx + 230, inty - 20))
        self.contornoFase.desenhar(self)
            # desenhando Telhado
        pygame.gfxdraw.filled_trigon(self,
                                         int(self.__tela.ajuste / 2) + intx + auxX + + 85 + int(
                                             (escala * desenho.colunas) / 2),
                                         inty + aux + 50,
                                         int(self.__tela.ajuste / 2) + intx + auxX  + 80, 85 + inty + aux,
                                         int(self.__tela.ajuste / 2) + intx + auxX  + 90 + escala * desenho.colunas,
                                         85 + inty + aux, Cores.TELHADO)

        for i in range(0, desenho.colunas):
            for j in range(0, desenho.linhas):
                if int(desenho.tiles[i][j]) >= 0:
                    pygame.draw.rect(self, get_cor(int(desenho.tiles[i][j])),
                                         ((self.__tela.ajuste / 2) + intx + auxX  + 85 + (escala * i),
                                          85 + inty + aux + (escala * j),
                                          escala, escala))
                else:
                    self.blit(self.__janela2,
                                         ((self.__tela.ajuste / 2) + intx + auxX + 85 + (escala * i),
                                          85 + inty + aux + (escala * j), escala,
                                          escala))
        contornar(self, (self.__tela.ajuste / 2) + intx + auxX  + 85, inty + aux + 85,
                      escala * desenho.colunas,
                      escala * desenho.linhas)

    def desenharFerramentasEdicao(self):
        pygame.gfxdraw.box(self, (680 + self.__tela.ajuste, 20, 300, 510), Cores.BRANCO)
        contornar(self, 680 + self.__tela.ajuste, 20, 300, 510)

        # COR1
        pygame.draw.rect(self, Util.get_cor(3), (700 + self.__tela.ajuste, 30, 75, 75))
        contornar(self, 700 + self.__tela.ajuste, 30, 75, 75, 1)
        # COR2
        pygame.draw.rect(self, Util.get_cor(2), (790 + self.__tela.ajuste, 30, 75, 75))
        contornar(self, 790 + self.__tela.ajuste, 30, 75, 75, 1)
        # COR3
        pygame.draw.rect(self, Util.get_cor(1), (875 + self.__tela.ajuste, 30, 75, 75))
        contornar(self, 875 + self.__tela.ajuste, 30, 75, 75, 1)
        # COR4
        pygame.draw.rect(self, Util.get_cor(0), (700 + self.__tela.ajuste, 115, 75, 75))
        contornar(self, 700 + self.__tela.ajuste, 115, 75, 75, 1)
        # Janela
        if not self.finalizacriacao:
            self.blit(self.__janela, (790 + self.__tela.ajuste, 115, 75, 75))
            contornar(self, 790 + self.__tela.ajuste, 115, 75, 75, 1)

    def modoCriar(self):
        self.criando = True

    def modoJogar(self):
        self.criando = False

    def get_executarButton(self):
        return self.__executarButton

    def get_boxExecucao(self):
        return self.__boxExecucao

    def get_seta(self):
        return self.__seta

    def get_seta2(self):
        return self.__seta2
