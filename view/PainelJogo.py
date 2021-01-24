import os
import pygame
import pygame.gfxdraw
from model.Sprite import Sprite
from util import Util
from util.Util import Cores, get_cor, ESCALAX, ESCALAY
from view.Painel import Painel
from util.Util import carrega_imagem


def escalar(x, y, tamx, tamy):
    return int(ESCALAX * x), int(y * ESCALAY), int(ESCALAX * tamx), int(ESCALAY * tamy)


def escalarXY(x, y):
    return int(ESCALAX * x), int(y * ESCALAY)


def escalarX(x):
    return int(ESCALAX * x)


def escalarY(y):
    return int(ESCALAY * y)


def contornar(superfice, x, y, largura, altura, tam=2, cor=Cores.CORSECUNDARIA, eX=1, eY=1):
    x = int(eX * x)
    y = int(y * eY)
    largura = int(eX * largura)
    altura = int(altura * eY)

    x -= tam / 2
    y -= tam / 2
    largura += tam
    altura += tam
    # linha cima
    pygame.draw.line(superfice, cor, (x, y), ((x + largura), y), tam)
    # linha baixo
    pygame.draw.line(superfice, cor, (x, y + altura),
                     ((x + largura), y + altura), tam)
    # linha esquerda
    pygame.draw.line(superfice, cor, (x, y), (x, y + altura), tam)
    # linha direita
    pygame.draw.line(superfice, cor, (x + largura, y),
                     (x + largura, y + altura), tam)


def contornarRect(superfice, rect, cor=Cores.CORSECUNDARIA):
    # r = pygame.Rect(escalar(rect.x,rect.y,rect.w,rect.h))
    pygame.gfxdraw.rectangle(superfice, (
        rect[0], rect[1], rect[2], rect[3]), cor)


class PainelJogo(Painel):

    def __init__(self, tela, largura, altura, x=0, y=0):
        super().__init__(largura, altura, x, y)
        self.__tela = tela
        fontearquivo = os.path.dirname(os.path.abspath(
            __file__)).replace("view", "").replace("model", "")
        fontearquivo = os.path.join(fontearquivo, "lib")
        fontearquivo = os.path.join(fontearquivo, "FreeSansBold.ttf")
        self.fontetipo = 'comicsansms'
        self.botaoVoltar = Sprite("VOLTAR.png", 1, 2)
        self.botaoSalvar = Sprite("BOTAOPROX.PNG", 1, 2)
        self.maoCursor = Sprite("cursor.png", 1, 2)
        self.__janela = carrega_imagem("janela.png")
        self.__edit = carrega_imagem("edit.png")
        self.__janela2 = pygame.transform.scale(
            self.__janela, escalarXY(30, 30))
        # self.__janela2 = pygame.transform.scale(self.__janela, escalarXY(escala, escala))
        self.__tinta = carrega_imagem("tinta.png", "", 2)
        self.__corTelhado = Cores.TELHADO
        self.__executarButton = Sprite("executar.png", 1, 2)
        self.reiniciarbotao = Sprite("reiniciar.png", 1, 2)
        self.seta = Sprite("seta.png", 1, 2)
        self.seta2 = Sprite("seta.png", 1, 2)
        self._img3 = carrega_imagem("03.png", "blocos")
        self._img2 = carrega_imagem("02.png", "blocos")
        self._img1 = carrega_imagem("01.png", "blocos")
        self.lixo = Sprite("lixo.png", 1, 2)
        self.repetir = Sprite("repetir.png", 1, 2)
        self.corOpcao = Sprite("cor.png", 1, 2)
        self.moverEsquerda = Sprite("BOTAOESQUERDA.png", 1, 2, 2)
        self.moverDireita = Sprite("BOTAODIREITA.png", 1, 2, 2)
        #self.lixo.definirPosicao((1150, 410))
        self._img1 = pygame.transform.scale(
            self._img1, (int(self._img1.get_rect().w / 2), int(self._img1.get_rect().h / 2)))
        self._img2 = pygame.transform.scale(
            self._img2, (int(self._img2.get_rect().w / 2), int(self._img2.get_rect().h / 2)))
        # pygame.transform.rotate(self.__seta2.sheet, 180)
        self.seta2.sheet = pygame.transform.flip(
            self.seta2.sheet, True, False)
        self.__executarButton.definirPosicao((980, 550))
        self.botaoVoltar.definirPosicao((1080, 570))
        self.botaoSalvar.definirPosicao((810, 570))
        self.reiniciarbotao.definirPosicao((960, 25))
        self.__boxExecucao = pygame.rect.Rect(escalar(20, 550, 950, 100))
        self.fontePequena = pygame.font.Font(fontearquivo, escalarX(12))
        self.fonten = pygame.font.Font(fontearquivo, escalarX(17))
        self.fonteg = pygame.font.Font(fontearquivo, escalarX(32))
        self.fontexg = pygame.font.Font(fontearquivo, escalarX(52))
        self.fontexxg = pygame.font.Font(fontearquivo, escalarX(150))
        self.infoCriando = self.fonteg.render(
            "Utilize as ferramentas para pintar a casa que será o desafio da fase criada!", True, Cores.PRETO)
        self.infoCriando2 = self.fonteg.render(
            "Agora modifique o desenho para definir como a casa aparecerá inicialmente!", True, Cores.PRETO)
        self.back = carrega_imagem("back.png")
        self.exibeAviso = False
        self.mostrarEditBlRepetir = self.mostrarEditBlCor = False

        self.transparent = pygame.Surface(
            (self.__tela.largura, self.__tela.altura), pygame.SRCALPHA)

        self.exibindoTutorial = False
        self.botaoPularTutorial = Sprite("BOTAOPULAR.png", 1, 2)
        self.botaoEsquerda = Sprite("BOTAOESQUERDA.png", 1, 2)
        self.botaoDireita = Sprite("BOTAODIREITA.png", 1, 2)
        self.botaoEsquerda.definirPosicao((60, 350))
        self.botaoDireita.definirPosicao((1220, 350))
        self.botaoPularTutorial.definirPosicao((590, 650))
        self.indexTutorial = 0

        self.destaque = False
        self.c3 = carrega_imagem("c3.png")
        self.textoaviso = "", ""  # self.tituloaviso = ""
        self.desenharGuiaDesenhoBoolean = False
        self.guiDesenhoRect = pygame.rect.Rect(escalar(40, 320, 300, 200))
        self.criando = self.finalizacriacao = False
        self.imgPincel = pygame.transform.rotate(carrega_imagem(
            "pincel" + str(1) + ".png", escala=2), 45)
        self.confete = Sprite("confete.png", 1, 59)
        self.confete2 = Sprite("confete.png", 1, 59)
        self.confete3 = Sprite("confete2.png", 1, 59)
        self.confete4 = Sprite("confete2.png", 1, 59)
        self.confete.definirPosicao((-100, 450))
        self.confete2.definirPosicao((1100, 450))
        self.confete3.definirPosicao((-100, -150))
        self.confete4.definirPosicao((1100, -150))
        self.confete.animacao = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                                 55, 56, 57, 58, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        self.confete2.animacao = self.confete3.animacao = self.confete4.animacao = self.confete.animacao
        self.tempoAnGanhou = 0
        self.fase = None
        self.contornoFase = Sprite("contorno4.png", 1, 2)
        # CORESEDICAO
        self.coresEdicao = list()
        self.coresEdicao.append(pygame.Rect(
            escalar(790 + self.__tela.ajuste, 115, 75, 75)))
        self.coresEdicao.append(pygame.Rect(
            escalar(700 + self.__tela.ajuste, 115, 75, 75)))
        self.coresEdicao.append(pygame.Rect(
            escalar(875 + self.__tela.ajuste, 30, 75, 75)))
        self.coresEdicao.append(pygame.Rect(
            escalar(790 + self.__tela.ajuste, 30, 75, 75)))
        self.coresEdicao.append(pygame.Rect(
            escalar(700 + self.__tela.ajuste, 30, 75, 75)))

    def desenhar(self, fase, jogador=None, comando=None, pincel=None, alerta=False):
        if not alerta:
            self.fase = fase
            desenho = fase.desenhoDesafio
            self.__tela.jogoPane.fill(self.__tela.corfundo)

            if fase.tutorial is None or len(fase.tutorial) <= self.indexTutorial:
                self.exibindoTutorial = False
                self.indexTutorial = 0
                img = None
            else:
                img = fase.tutorial[self.indexTutorial]

            if not self.exibindoTutorial:
                self.botaoVoltar.desenharBt(self)
            self.desenharDesenho(desenho, pincel)
            if not self.criando:
                if not self.exibindoTutorial:
                    self.reiniciarbotao.desenharBt(self)
                self.desenharDesenhoGuia(fase.desenhoResposta)
                self.desenharCaixaExecucao(comando, fase)
                self.desenharCaixaBlocos(fase)
                self.desenharInfo(fase, jogador)

            else:
                if not self.finalizacriacao:
                    self.blit(self.infoCriando, (20, 540))
                else:
                    self.blit(self.infoCriando2, (20, 540))
                self.botaoSalvar.desenharBt(self)
                self.desenharFerramentasEdicao()
                self.desenharPincelWidget()

            if self.exibeAviso:
                self.aviso(self.textoaviso[0], self.textoaviso[1])
            if self.exibindoTutorial:
                self.desenharTutorial(img, self)

    def desenharTutorial(self, img, s, c=(0, 0, 0, 180)):
        self.transparent.fill(c)
        s.blit(self.transparent, (0, 0))
        s.blit(img, ((
            self.__tela.largura/2)-(img.get_rect().w/2), (self.__tela.altura/2)-(img.get_rect().h/2)))
        self.botaoDireita.desenharBt(s)
        self.botaoEsquerda.desenharBt(s)
        self.botaoPularTutorial.desenharBt(s)

    def reinicarAnimacaoConfete(self):
        self.confete.spriteativo = self.confete2.spriteativo = self.confete3.spriteativo = self.confete4.spriteativo = 0

    def desenharAnimacaoWin(self, fase=None, jogador=None, comando=None, pincel=None, fps=0, sc=None):
        if sc is None:
            sc = self
            self.confete.definirPosicao((-100, 450))
            self.confete2.definirPosicao((1100, 450))
            self.confete3.definirPosicao((-100, -150))
            self.confete4.definirPosicao((1100, -150))
        else:
            self.confete.definirPosicao((800, 80))
            self.confete2.definirPosicao((850, 80))
            self.confete3.definirPosicao((800, 80))
            self.confete4.definirPosicao((850, 80))
        if fase is not None:
            self.__tela.jogoPane.desenhar(
                fase, jogador, comando, pincel=pincel)

        self.tempoAnGanhou = self.confete.animar(
            sc, self.tempoAnGanhou, fps=fps)
        self.tempoAnGanhou = self.confete2.animar(
            sc, self.tempoAnGanhou, fps=fps)
        self.tempoAnGanhou = self.confete3.animar(
            sc, self.tempoAnGanhou, fps=fps)
        self.tempoAnGanhou = self.confete4.animar(
            sc, self.tempoAnGanhou, fps=fps)

    def desenharInfo(self, fase, jogador):
        cor = Cores.BRANCO
        self.blit(self.__tinta, escalarXY(20, 20))
        if jogador is not None:
            nome = self.fontePequena.render(
                ("Jogador: " + jogador.getNome()), True, cor)
            faserender = self.fontePequena.render(
                ("Fase: " + str(fase.nivel)), True, cor)
            self.blit(nome, escalarXY(70, 40))
            self.blit(faserender, escalarXY(70, 60))
        tentativas = self.fonten.render("Tentativas Restantes:", True, cor)
        if self.destaque:
            tentativas2 = self.fontexxg.render(
                str(fase.tentativas), True, Cores.VERMELHO)
        else:
            tentativas2 = self.fonteg.render(str(fase.tentativas), True, cor)
        self.blit(tentativas, escalarXY(70, 90))
        self.blit(tentativas2, escalarXY(150, 110))

    def aviso(self, titulo, texto):
        self.blit(self.c3, escalar(400, 200, 500, 150))
        titulor = self.fonteg.render(titulo, True, Cores.VERMELHO)
        textor = self.fonten.render(texto, True, Cores.PRETO)
        self.blit(titulor, escalarXY(520, 300))
        self.blit(textor, escalarXY(470, 400))

    def trocarimgPincel(self, num):
        if num >= 0:
            self.imgPincel = pygame.transform.rotate(carrega_imagem(
                "pincel" + str(num) + ".png", escala=2*ESCALAX), 45)
        else:
            self.imgPincel = carrega_imagem("janela.png", escala=2*ESCALAX)

    def desenharPincelWidget(self):
        pos = pygame.mouse.get_pos()
        self.blit(self.imgPincel, (pos[0] | +5, pos[1] + 5))

    def desenharVerificacao(self, i, j, janela=False, passou=True):
        inty = 30
        intx = 150
        if not passou:
            pygame.draw.rect(self, Util.get_cor(4),
                             escalar((self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75))
        contornar(self, (self.__tela.ajuste / 2) + intx + 85 + (75 * i),
                  85 + inty + (75 * j), 75, 75, 5, eX=ESCALAX, eY=ESCALAY)

    def desenharDesenho(self, desenho, pincel):
        inty = 30
        intx = 150
        self.blit(self.back, (20, 20))
        pygame.gfxdraw.filled_trigon(self, escalarX((self.__tela.ajuste / 2) + intx + 85 + ((75 * desenho.colunas) / 2)),
                                     escalarY(inty + 30),
                                     escalarX(
                                         (self.__tela.ajuste / 2) + intx + 80),
                                     escalarY(85 + inty),
                                     escalarX((self.__tela.ajuste / 2) +
                                              intx + 90 + 75 * desenho.colunas),
                                     escalarY(85 + inty), self.__corTelhado)
        for i in range(0, desenho.colunas):
            for j in range(0, desenho.linhas):
                if int(desenho.tiles[i][j]) >= 0:
                    pygame.draw.rect(self, Util.get_cor(int(desenho.tiles[i][j])),
                                     escalar((self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75))
                else:
                    self.blit(self.__janela,
                              escalar((self.__tela.ajuste / 2) + intx + 85 + (75 * i), 85 + inty + (75 * j), 75, 75))
                contornar(self, (self.__tela.ajuste / 2) + intx + 85 + (75 * i),
                          85 + inty + (75 * j), 75, 75, 1, eY=ESCALAY, eX=ESCALAX)
        contornar(self, (self.__tela.ajuste / 2) + intx + 85, inty + 85,
                  75 * desenho.colunas, 75 * desenho.linhas, eY=ESCALAY, eX=ESCALAX)
        if not self.criando:
            self.blit(pincel.image,
                      escalar(
                          (self.__tela.ajuste / 2) + intx +
                          85 + (75 * pincel.posicaoX),
                          85 + inty + (75 * pincel.posicaoY),
                          75,
                          75))

    def desenharCaixaExecucao(self, comando, fase):
        pygame.gfxdraw.box(self, self.__boxExecucao, Cores.BRANCO)
        contornar(self, self.__boxExecucao.x, self.__boxExecucao.y,
                  self.__boxExecucao.w, self.__boxExecucao.h)
        if not self.exibindoTutorial:
            self.__executarButton.desenharBt(self)
        y = 565
        xspace = -60
        img1 = self._img1
        img2 = self._img2
        for x in comando:
            if x.get_tipo() == "repetir":
                numRepet = self.fontePequena.render(
                    str(x.get_Valor()), True, Cores.CORSECUNDARIA)
                x.definirPosicao(((xspace + 83)/ESCALAX, y - 15))
                self.blit(img1, escalar((xspace + 83)/ESCALAX, y -
                                        15, img1.get_rect().w, img1.get_rect().h))
                if x.blocos is not None:
                    for bl in x.blocos:
                        img = self._img3
                        img = pygame.transform.scale(
                            img, (int(img.get_rect().w / 2), int(img.get_rect().h / 2)))
                        aux = self._img3
                        aux = pygame.transform.scale(
                            aux, (int(aux.get_rect().w / 2), int(aux.get_rect().h / 2)))
                        self.blit(img, (xspace + 120, escalarY(y - 14)))
                        self.blit(aux, (xspace + 140, escalarY(y - 14)))
                        bl.definirPosicao(((xspace + 115)/ESCALAX, y))
                        bl.desenhar(self)
                        xspace += bl.get_rect().w - (12*ESCALAX)
                    x.set_rect(pygame.rect.Rect(x.get_rect().x, x.get_rect().y, (65 * x.blocos.__len__()) + 105,
                                                img2.get_rect().h))
                    self.blit(img2, (xspace + 60, escalarY(y - 15)))
                    self.blit(numRepet, escalarXY(xspace + 147, (y + 70)))
                else:
                    self.blit(img2, escalarXY(xspace + 123, y - 15))
                    self.blit(numRepet, escalarXY(xspace + 210, y + 70))
                    xspace += 65*ESCALAX
                xspace += 100*ESCALAX
            else:
                x.definirPosicao(((xspace + 80)/ESCALAX, y))
                xspace += x.get_rect().w - (ESCALAX*15)
                x.desenhar(self)

            if x.selecionado:
                auxy = 0
                if x.get_tipo() == "repetir" or x.get_tipo() == "selecionar_cor":
                    auxy = 60
                pos = x.get_rect()
                tamx = 200 + auxy
                tamy = 70
                #x.get_rect().width/2 - tamx/2
                pygame.draw.rect(
                    self, Cores.BRANCO, (pos.x, pos.y - escalarY(75), escalarX(tamx), escalarY(tamy)))
                contornar(self, pos.x, pos.y - escalarY(75),
                          escalarX(tamx - 1), escalarY(tamy - 1), 4, Cores.CORPRINCIPAL)

                self.lixo.definirPosicao(
                    (pos.x + escalarX(80), pos.y - escalarY(60)), False)
                self.lixo.desenharBt(self)

                self.moverEsquerda.definirPosicao(
                    (pos.x + escalarX(10), pos.y - escalarY(60)), False)
                self.moverEsquerda.desenharBt(self)

                self.moverDireita.definirPosicao(
                    (pos.x + escalarX(150+auxy), pos.y - escalarY(60)), False)
                self.moverDireita.desenharBt(self)

                if x.get_tipo() == "repetir":
                    self.repetir.definirPosicao(
                        (pos.x + escalarX(140), pos.y - escalarY(65)), False)
                    self.repetir.desenharBt(self)
                    if self.mostrarEditBlRepetir:
                        pygame.draw.rect(
                            self, Cores.LARANJA, (pos.x, pos.y - escalarY(175), escalarX(300), escalarY(100)))
                        contornar(self, pos.x, pos.y - escalarY(175),
                                  escalarX(299), escalarY(99), 4, Cores.LARANJAESCURO)

                        numRepet = self.fontexg.render(
                            str(x.get_Valor()), True, Cores.CORSECUNDARIA)
                        self.blit(numRepet, (pos.x + escalarX(140),
                                             pos.y - escalarY(145)))
                        self.seta.definirPosicao(
                            (pos.x + escalarX(20), pos.y - escalarY(160)), False)
                        self.seta.desenharBt(self)

                        self.seta2.definirPosicao(
                            (pos.x + escalarX(210), pos.y - escalarY(160)), False)
                        self.seta2.desenharBt(self)

                elif x.get_tipo() == "selecionar_cor":
                    self.corOpcao.definirPosicao(
                        (pos.x + escalarX(140), pos.y - escalarY(65)), False)
                    self.corOpcao.desenharBt(self)
                    if self.mostrarEditBlCor:
                        pygame.draw.rect(
                            self, Cores.ROXO, (pos.x, pos.y - escalarY(175), escalarX(300), escalarY(100)))
                        contornar(self, pos.x, pos.y - escalarY(175),
                                  escalarX(299), escalarY(99), 4, Cores.ROXOESCURO)
                        vl = 0
                        tambl = 70
                        for cor in fase.coresdisponiveis:
                            pygame.draw.rect(self, Util.get_cor(cor), (
                                pos.x + 5 + escalarX(tambl + 2) * vl, pos.y - escalarY(157), escalarX(tambl), escalarY(tambl)))
                            contornarRect(self, (
                                pos.x + 5 + escalarX(tambl + 2) * vl, pos.y - escalarY(157), escalarX(tambl), escalarY(tambl)))
                            vl += 1

            if x.selecionado and x.get_tipo() != "inicio" or (x.get_tipo() != "inicio" and x.colisao_point(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and not self.seta2.colisao_point(pygame.mouse.get_pos()) and not self.seta.colisao_point(
                    pygame.mouse.get_pos())):
                # MUITO USO DE MEMORIA VER DEPOIS
                s = pygame.Surface(
                    (x.get_rect().width, x.get_rect().height), pygame.SRCALPHA)
                s.fill((0, 0, 0, 100))
                s.blit(self.__edit, (x.get_rect().width/2 - self.__edit.get_rect().w/2,
                                     x.get_rect().height/2 - self.__edit.get_rect().h/2))
                self.blit(s, (x.get_rect().x, x.get_rect().y))
                contornar(self, x.get_rect().x, x.get_rect().y, x.get_rect(
                ).w, x.get_rect().h, tam=3, cor=Cores.CORPRINCIPAL)

    def desenharCaixaBlocos(self, fase):
        pygame.gfxdraw.box(self, escalar(
            680 + self.__tela.ajuste, 20, 300, 510), Cores.BRANCO)
        contornar(self, 680 + self.__tela.ajuste, 20,
                  300, 510, eX=ESCALAX, eY=ESCALAY)
        x = fase.blocosdisponiveis
        xspace = escalarX(300)
        ajustex = ajustey = 0
        mousep = pygame.mouse.get_pos()
        mouseV = True
        for i in range(0, fase.blocosdisponiveis.__len__()):
            x[i].definirPosicao(
                (680 + ajustex + self.__tela.ajuste, 30 + ajustey))
            x[i].desenhar(self)
            if x[i].get_tipo() == "selecionar_cor":
                pos = x[i].get_rect()
                if x[i].get_Valor() < 0:
                    pygame.draw.rect(
                        self, Cores.ROXO, (pos.x, pos.y + escalarY(75), escalarX(300), escalarY(100)))
                    contornar(self, pos.x, pos.y + escalarY(74),
                              escalarX(299), escalarY(99), 4, Cores.ROXOESCURO)
                    vl = 0
                    tambl = 70
                    for cor in fase.coresdisponiveis:
                        pygame.draw.rect(self, Util.get_cor(cor), (pos.x + 5 + escalarX(
                            tambl+2) * vl, pos.y + escalarY(87), escalarX(tambl), escalarY(tambl)))
                        contornarRect(self, (pos.x + 5 + escalarX(tambl+2) * vl,
                                             pos.y + escalarY(87), escalarX(tambl), escalarY(tambl)))
                        vl += 1
            xspace -= x[i].get_rect().w
            if i + 1 < x.__len__() and escalarX(xspace) <= x[i + 1].get_rect().w:
                ajustey += 100
                ajustex = 0
                xspace = 300
            else:
                ajustex += x[i].get_rect().w
            # if x[i].colisao_point(mousep):
            #     mouseV = False
            #     if pygame.mouse.get_pressed()[0]:
            #         self.maoCursor.desenhar(self, 1, mousep[0], mousep[1])
            #     else:
            #         self.maoCursor.desenhar(self, 0, mousep[0], mousep[1])
        # pygame.mouse.set_visible(mouseV)

    def desenharDesenhoGuia(self, desenho, escala=30):
        inty = 250
        intx = -200
        aux = auxX = 0
        if desenho.colunas <= 3:
            auxX = 60
        if desenho.linhas < 4:
            aux = 60
        self.contornoFase.definirPosicao((intx + 230, inty - 20))
        self.contornoFase.desenhar(self)
        # desenhando Telhado
        pygame.gfxdraw.filled_trigon(self,
                                     escalarX((self.__tela.ajuste / 2) + intx + auxX + + 85 + (
                                             (escala * desenho.colunas) / 2)),
                                     escalarY(inty + aux + 50),
                                     escalarX(
                                         (self.__tela.ajuste / 2) + intx + auxX + 80),
                                     escalarY(85 + inty + aux),
                                     escalarX(
                                         (self.__tela.ajuste / 2) + intx + auxX + 90 + escala * desenho.colunas),
                                     escalarY(85 + inty + aux), Cores.TELHADO)

        for i in range(0, desenho.colunas):
            for j in range(0, desenho.linhas):
                if int(desenho.tiles[i][j]) >= 0:
                    pygame.draw.rect(self, get_cor(int(desenho.tiles[i][j])),
                                     escalar((self.__tela.ajuste / 2) + intx + auxX + 85 + (escala * i),
                                             85 + inty + aux + (escala * j),
                                             escala, escala))
                else:
                    self.blit(self.__janela2,
                              escalar((self.__tela.ajuste / 2) + intx + auxX + 85 + (escala * i),
                                      85 + inty + aux + (escala * j), escala,
                                      escala))
        contornar(self, (self.__tela.ajuste / 2) + intx + auxX + 85, inty + aux + 85,
                  escala * desenho.colunas,
                  escala * desenho.linhas, eX=ESCALAX, eY=ESCALAY)

    def desenharFerramentasEdicao(self):
        pygame.gfxdraw.box(self, escalar(
            680 + self.__tela.ajuste, 20, 300, 510), Cores.BRANCO)
        contornar(self, 680 + self.__tela.ajuste, 20,
                  300, 510, eY=ESCALAY, eX=ESCALAX)

        # COR1
        pygame.draw.rect(self, Util.get_cor(3), escalar(
            700 + self.__tela.ajuste, 30, 75, 75))
        contornar(self, 700 + self.__tela.ajuste, 30,
                  75, 75, 1, eY=ESCALAY, eX=ESCALAX)
        # COR2
        pygame.draw.rect(self, Util.get_cor(2), escalar(
            790 + self.__tela.ajuste, 30, 75, 75))
        contornar(self, 790 + self.__tela.ajuste, 30,
                  75, 75, 1, eY=ESCALAY, eX=ESCALAX)
        # COR3
        pygame.draw.rect(self, Util.get_cor(1), escalar(
            875 + self.__tela.ajuste, 30, 75, 75))
        contornar(self, 875 + self.__tela.ajuste, 30,
                  75, 75, 1, eY=ESCALAY, eX=ESCALAX)
        # COR4
        pygame.draw.rect(self, Util.get_cor(0), escalar(
            700 + self.__tela.ajuste, 115, 75, 75))
        contornar(self, 700 + self.__tela.ajuste, 115,
                  75, 75, 1, eY=ESCALAY, eX=ESCALAX)
        # Janela
        if not self.finalizacriacao:
            self.blit(self.__janela, escalar(
                790 + self.__tela.ajuste, 115, 75, 75))
            contornar(self, 790 + self.__tela.ajuste, 115,
                      75, 75, 1, eY=ESCALAY, eX=ESCALAX)

    def modoCriar(self):
        self.criando = True

    def modoJogar(self):
        self.criando = False

    def get_executarButton(self):
        return self.__executarButton

    def get_boxExecucao(self):
        return self.__boxExecucao

    def get_seta(self):
        return self.seta

    def get_seta2(self):
        return self.seta2
