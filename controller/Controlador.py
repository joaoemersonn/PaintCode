import os
import sys
from copy import deepcopy

import pygame

from model.Bloco import Bloco
from model.Desenho import Desenho
from model.Fase import Fase
from model.Jogador import Jogador
from model.Pincel import Pincel
from model.Sprite import Sprite
from util import Util
from util.GIFImage import GIFImage
from util.Gerador import gerarFases
from util.Util import gravar_saves, gravar_fase, ler_fases, ReproduzirSons, criarPastas, Cores, carrega_imagem, SONS, \
    ESCALAX
from util.Util import ler_saves
from view.Tela import Tela

TOCAREMLOOP = -1


class Controlador:
    def __init__(self):
        self._carregando = True
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        info = pygame.display.Info()
        self.largura, self.altura = info.current_w, info.current_h
        print("TELA: largura: ", self.largura, " altura: ", self.altura)
        #largura = 1000
        #altura = 768
        #(largura,altura), pygame.FULLSCREEN
        self.window = self.janela = Util.WINDOW
        self.window.fill(Cores.BRANCO)
        self.splash = carrega_imagem("splash.png", escala=2)
        #self.gif = GIFImage("loading.gif")
        print("splash")
        self.window.blit(self.splash, ((self.largura/2) -
                                       (self.splash.get_width()/2), 150))
        #####
        #self.fps = 120
        self.TICKS_PER_SECOND = 40
        self.SKIP_TICKS = 1000 / self.TICKS_PER_SECOND
        self.MAX_FRAMESKIP = 5
        self.next_game_tick = pygame.time.get_ticks()

        self.tela = None
        self.i = self.index = 0
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.pressNovojogo = self.executandoComando = False
        self.saves = list()
        self.tam = 1
        self.comando = list()
        self.__inicio = None
        self.jogador = None
        self.fase = self.faseanterior = None
        self.saveaexcluir = None
        self.fases = list()
        self.pincel = None
        self.pinceledicao = 1
        self.botaoclicado = False
        self.volume = True
        self.jogandoFasePersonalizada = self.fimdejogo = False
        self.espera = self.esperaperda = 0
        self.contaviso = self.j = self.i = 0
        self.verificandodesenho = False
        self.exibindoperda = False
        ###
        #self.gif.executar(self.window, 950, 350)
        self.inicializar()
        # self.gif.pause()

    def inicializar(self):
        criarPastas()
        pygame.mixer.init()
        Util.SONS.iniciar()
        self.tela = Tela(self.window, self.largura, self.altura)
        self.sons = Util.SONS
        self.tela.saves = self.carregarSaves()
        self.__inicio = Bloco("inicio")
        self.pincel = Pincel()
        self.comando.append(self.__inicio)
        Util.CARREGANDO = False
        gerarFases(self.fases)
        self.sons.BACKGROUND.set_volume(0.2)
        self.sons.BACKGROUND.play(TOCAREMLOOP)
        self._carregando = False

    def start(self):
        while self.rodando:
            loops = 0
            self.tela.desenhar()
            if self.jogoexecutando():
                self.desenharaviso()
                self.tela.jogoPane.desenhar(
                    self.fase, self.jogador, self.comando, self.pincel, self.tela.desenhaAlerta)
            while pygame.time.get_ticks() > self.next_game_tick and loops < self.MAX_FRAMESKIP:
                if self.executandoComando:
                    self.executarcomando()
                self.tratarEventos()
                self.verificardesenho()
                self.next_game_tick += self.SKIP_TICKS
                loops += 1
            # Desenha Animação
            if self.tela.jogoPane.tempoAnGanhou > 0:
                self.tela.jogoPane.desenharAnimacaoWin(
                    self.faseanterior, self.jogador, self.comando, self.pincel)

            pygame.display.update()
            # self.relogio.tick(self.fps)

    def jogoexecutando(self):
        if self.tela.telaJogo and not self.tela.desenhaConfirmacao:
            return True
        return False

    def executarcomando(self):
        if self.espera > 20:
            self.espera = 0
            self.pincel.mover(self.comando[1], self.fase.desenhoDesafio, self)
            self.comando.pop(1)
            self.tam -= 1
            if self.tam < 1 or len(self.comando) <= 1:
                self.refreshDesenho()
                self.executandoComando = False
                self.tam = 1
                self.verificandodesenho = True
        else:
            self.espera += 1

    def desenharaviso(self):
        if self.tela.jogoPane.exibeAviso:
            if self.contaviso > 150:
                self.contaviso = 0
                self.tela.jogoPane.exibeAviso = False
            else:
                self.contaviso += 1

    def perdeu(self):
        self.sons.LOSE.play()
        self.i = self.j = 0
        self.refreshDesenho()
        self.tela.textoAlerta = (
            "Acabaram suas Execuções!,", "e a casa não está como o cliente pediu!",
            "Pressione OK para tentar novamente")
        self.tela.desenhaAlerta = True
        self.pincel.posicaoInicial()
        if self.jogandoFasePersonalizada:
            self.tela.fasespersonalizadas = ler_fases()
            self.fase = self.tela.fasespersonalizadas[self.index]
        else:
            gerarFases(self.fases)
            self.fase = self.fases[self.jogador.getNivel()]

    def ganhou(self):
        self.i = self.j = 0
        if self.jogandoFasePersonalizada:
            self.sons.WIN.play()
            self.faseanterior = self.fase
            self.tela.jogoPane.tempoAnGanhou = (50 * 4)
            self.tela.textoAlerta = (
                "Parabéns Você Concluiu a Fase!", "Pressione OK para Retornar!")
            self.pincel.posicaoInicial()
            self.tela.fasespersonalizadas = ler_fases()
            self.tela.desenhaAlerta = True
        elif len(self.fases) > self.jogador.getNivel() + 1:
            self.sons.WIN.play()
            self.faseanterior = self.fase
            self.tela.jogoPane.tempoAnGanhou = (50 * 4)
            self.tela.textoAlerta = (
                "Parabéns Você Passou de Nível!", "Pressione OK para continuar!")
            self.tela.desenhaAlerta = True
            self.jogador.subirNivel()
            self.pincel.posicaoInicial()
            self.fase = self.fases[self.jogador.getNivel()]
            gravar_saves(self.saves)
        else:
            self.sons.WIN.play()
            self.faseanterior = self.fase
            self.tela.jogoPane.tempoAnGanhou = (50 * 4)
            self.tela.textoAlerta = (
                "Parabéns Você Concluiu o Jogo!", "Pressione OK para continuar!")
            self.tela.desenhaAlerta = True
            self.fimdejogo = True
            self.pincel.posicaoInicial()
            gravar_saves(self.saves)

    def refreshDesenho(self):
        self.tela.desenhar()
        self.tela.jogoPane.desenhar(
            self.fase, self.jogador, self.comando, self.pincel)
        pygame.display.update()

    def tratarEventos(self):
        for event in pygame.event.get():
            posicaomaouse = pygame.mouse.get_pos()
            self.botaoclicado = False
            if self.tela.caixaTexto.active:
                self.tela.caixaTexto.handle_event(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.rodando = False
                sys.exit(1)
            # CLIQUE MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tela.telaJogo and not self.tela.desenhaAlerta and not self.tela.desenhaConfirmacao and not self.tela.jogoPane.exibindoTutorial:
                    self._VerificarTelaJogo(posicaomaouse)
                elif self.tela.jogoPane.exibindoTutorial:
                    if self.tela.jogoPane.botaoEsquerda.colisao_point(posicaomaouse) and self.tela.jogoPane.indexTutorial > 0:
                        self.tela.jogoPane.indexTutorial -= 1
                    elif self.tela.jogoPane.botaoDireita.colisao_point(posicaomaouse):
                        self.tela.jogoPane.indexTutorial += 1

            if event.type == pygame.MOUSEBUTTONUP:
                if self.tela.desenhaConfirmacao:
                    if self.tela.cancelarbotao.colisao_point(posicaomaouse):
                        self.tela.desenhaConfirmacao = False
                    if self.tela.confirmarbotao.colisao_point(posicaomaouse):
                        self.saves.remove(self.saveaexcluir)
                        gravar_saves(self.saves)
                        self.tela.desenhaConfirmacao = False
                elif self.tela.desenhaNovoJogo:
                    if self.tela.cancelarbotao.colisao_point(posicaomaouse):
                        self.tela.desenhaNovoJogo = False
                    if self.tela.confirmarbotao.colisao_point(posicaomaouse):
                        if self.pressNovojogo:
                            self.tela.caixaTexto.active = self.tela.desenhaNovoJogo = self.pressNovojogo = False
                            gerarFases(self.fases)
                            self.jogador = Jogador(self.tela.caixaTexto.text)
                            self.tela.caixaTexto.text = ""
                            self.saves.append(self.jogador)
                            gravar_saves(self.saves)
                            self.fase = self.fases[self.jogador.getNivel()]
                            self.pincel.posicaoInicial()
                            self.tela.botaoPlay.append(
                                Sprite("BOTAOPLAY.PNG", 1, 2))
                            self.tela.telaSaves = False
                            self.tela.telaJogo = True

                elif self.tela.desenhaAlerta and self.tela.ok.colisao_point(posicaomaouse):
                    self.tela.desenhaAlerta = not self.tela.desenhaAlerta
                    if self.fase.tentativas is not None:
                        self.tela.jogoPane.exibindoTutorial = True
                    if self.jogandoFasePersonalizada:
                        self.jogandoFasePersonalizada = False
                        self.tela.telaFases = True
                        self.tela.telaJogo = False
                    elif self.fimdejogo:
                        self.fimdejogo = self.tela.telaJogo = False
                        self.tela.telaSaves = True

                elif self.tela.telaCriar:
                    self._VerificarTelaCriar(posicaomaouse)
                elif self.tela.telaInicio:
                    self._VerificarTelaInicio(posicaomaouse)
                elif self.tela.telaSaves:
                    self._VerificarTelaSaves(posicaomaouse)
                elif self.tela.telaFases:
                    self._VerificarTelaFases(posicaomaouse)
                elif self.tela.telaJogo:
                    for x in self.fase.blocosdisponiveis:
                        for c in self.comando:
                            if x.pressionado and c.get_tipo() == "repetir" and c.colisao_rect(x.get_rect()):
                                if x.get_tipo() == "repetir":
                                    self.sons.ALERT.play(2)
                                    self.tela.jogoPane.textoaviso = "MOVIMENTO INVÁLIDO!", "Não é possivel colocar um bloco de repetição em outro!"
                                    self.tela.jogoPane.exibeAviso = True
                                else:
                                    if self.tam < 12:
                                        if c.blocos is None:
                                            c.blocos = list()
                                        bl = Bloco(x.get_tipo(), x.get_Valor())
                                        # bl = self.atualizarblMover(bl)
                                        c.blocos.append(bl)
                                        if len(c.blocos) > 1:
                                            self.tam += 1
                                    else:
                                        self.sons.ALERT.play(1)
                                        self.tela.jogoPane.textoaviso = "TAMANHO MÁXIMO!", "Comando atingiu limite máximo de blocos!"
                                        self.tela.jogoPane.exibeAviso = True
                                x.pressionado = False
                        if x.pressionado and x.colisao_rect(self.tela.jogoPane.get_boxExecucao()):
                            if self.tam <= 12:
                                self.sons.COLOCAR.play()
                                bloco = Bloco(x.get_tipo(), x.get_Valor())
                                if bloco.get_tipo() == "repetir":
                                    # self.tam += 1
                                    bloco.set_Valor(3)
                                # bloco = self.atualizarblMover(bloco)
                                self.comando.append(bloco)
                                self.tam += 1
                            else:
                                self.sons.ALERT.play(1)
                                self.tela.jogoPane.textoaviso = "TAMANHO MÁXIMO!", "Comando atingiu limite máximo de blocos!"
                                self.tela.jogoPane.exibeAviso = True
                        x.pressionado = False
                    self.atualizarListaBlMover(self.comando)
                    self.atualizarListaBlMover(
                        self.fase.blocosdisponiveis, True)

    def _VerificarTelaJogo(self, posicaomouse):

        if self.tela.jogoPane.criando:
            self.colisaoDesenho(self.fase.desenhoDesafio)
            lista = self.tela.jogoPane.coresEdicao
            for i in range(0, len(lista)):
                if lista[i].collidepoint(posicaomouse):
                    self.pinceledicao = i - 1
            self.tela.jogoPane.trocarimgPincel(self.pinceledicao)
            if self.tela.jogoPane.botaoSalvar.colisao_point(posicaomouse) and not self.tela.jogoPane.finalizacriacao:
                self.tela.textoAlerta = (
                    "PRONTO!", "", "Agora Modifique o desenho para ser o desafio a ser cumprido")
                self.pinceledicao = 0
                self.tela.jogoPane.trocarimgPincel(self.pinceledicao)
                self.tela.jogoPane.botaoSalvar.mudarImg("BOTAOSALVAR.PNG")
                self.tela.desenhaAlerta = True
                self.tela.jogoPane.finalizacriacao = True
                self.fase.desenhoResposta = deepcopy(self.fase.desenhoDesafio)
            elif self.tela.jogoPane.botaoSalvar.colisao_point(posicaomouse):
                self.fase.coresdisponiveis.append(0)
                self.fase.coresdisponiveis.append(1)
                self.fase.coresdisponiveis.append(2)
                self.fase.coresdisponiveis.append(3)
                gravar_fase(self.fase)
                self.tela.jogoPane.finalizacriacao = False
                self.tela.textoAlerta = (
                    "Nível Criado Com Sucesso!", "", "Pressione OK para voltar ao inicio")
                self.tela.desenhaAlerta = True
                self.tela.telaJogo = False
                self.tela.telaInicio = True

        if self.tela.jogoPane.reiniciarbotao.colisao_point(posicaomouse):
            self.sons.REINICAR.play()
            self.pincel.posicaoInicial()
            self.comando.clear()
            self.comando.append(self.__inicio)
            self.tam = 1
            if self.jogandoFasePersonalizada:
                self.tela.fasespersonalizadas = ler_fases()
                self.fase = self.tela.fasespersonalizadas[self.index]
            else:
                gerarFases(self.fases)
                self.fase = self.fases[self.jogador.getNivel()]
        if self.tela.jogoPane.botaoVoltar.colisao_point(posicaomouse):
            self.botaoclicado = True
            if self.tela.jogoPane.criando:
                self.tela.telaCriar = True
            else:
                self.comando.clear()
                self.comando.append(self.__inicio)
                if self.jogandoFasePersonalizada:
                    self.tela.telaFases = True
                    self.jogandoFasePersonalizada = False
                else:
                    self.tela.telaSaves = True
            self.tela.telaJogo = False
        # Executar
        if self.tela.jogoPane.get_executarButton().colisao_point(posicaomouse) and len(self.comando) > 1:
            self.executandoComando = True
        #  Arrastar BLoco comando
        for x in self.fase.blocosdisponiveis:
            pos = pygame.Rect((x.get_rect().x + 11, x.get_rect().y +
                               58, x.get_rect().w - 30, x.get_rect().h - 58))
            if x.get_tipo() == "selecionar_cor" and pos.collidepoint(posicaomouse):
                if x.get_Valor() < 0:
                    x.set_Valor(0)
                else:
                    x.set_Valor(-1)
            elif x.get_tipo() == "selecionar_cor" and x.get_Valor() < 0:
                vl = 0
                tambl = 70
                pos = x.get_rect()
                for cor in self.fase.coresdisponiveis:
                    rect = pygame.Rect(
                        (pos.x + 5 + self.tela.escalarX(tambl+2) * vl, pos.y + self.tela.escalarY(87), self.tela.escalarX(tambl), self.tela.escalarY(tambl)))
                    if rect.collidepoint(posicaomouse):
                        x.set_Valor(cor)
                    vl += 1
            elif x.colisao_point(posicaomouse):
                self.sons.PEGAR.play()
                x.pressionado = True

        for x in self.comando:
            remove = True
            if x.get_tipo() == "repetir" and x.blocos is not None:
                seta1 = x.seta1  # self.tela.jogoPane.get_seta()
                seta2 = x.seta2  # self.tela.jogoPane.get_seta2()
                if seta1.collidepoint(posicaomouse) or seta2.collidepoint(posicaomouse):
                    remove = False
                if seta1.collidepoint(posicaomouse) and x.Value > 2:
                    x.Value -= 1
                elif seta2.collidepoint(posicaomouse) and x.Value < 9:
                    x.Value += 1
            if x.get_tipo() == "selecionar_cor" and x.get_Valor() < 0:
                vl = 0
                tambl = 70
                posi = x.get_rect()
                for cor in self.fase.coresdisponiveis:
                    rect = pygame.Rect(
                        (posi.x + 5 + self.tela.escalarX(tambl + 2) * vl, posi.y + self.tela.escalarY(87), self.tela.escalarX(tambl), self.tela.escalarY(tambl)))
                    if rect.collidepoint(posicaomouse):
                        x.set_Valor(cor)
                    vl += 1
            elif x.colisao_point(posicaomouse) and x.get_tipo() != "inicio":
                pos = pygame.Rect(
                    (x.get_rect().x + 11, x.get_rect().y + 58, x.get_rect().w - 30, x.get_rect().h - 58))
                if x.get_tipo() == "selecionar_cor" and pos.collidepoint(posicaomouse):
                    if x.get_Valor() < 0:
                        x.set_Valor(0)
                    else:
                        x.set_Valor(-1)

                elif remove:
                    self.sons.DELETE.play()
                    if x.get_tipo() == "repetir" and x.blocos is not None:
                        for sb in x.blocos:
                            self.tam -= 1
                    self.comando.remove(x)
                    self.tam -= 1

    def _VerificarTelaCriar(self, posicaomouse):
        if self.tela.btCimaEx.colisao_point(posicaomouse) and self.tela.execucoes < 9:
            self.tela.execucoes += 1
        elif self.tela.btBaixoEx.colisao_point(posicaomouse) and self.tela.execucoes > 1:
            self.tela.execucoes -= 1
        elif self.tela.btCimaLi.colisao_point(posicaomouse) and self.tela.linhas < 5:
            self.tela.linhas += 1
        elif self.tela.btBaixoLi.colisao_point(posicaomouse) and self.tela.linhas > 2:
            self.tela.linhas -= 1
        elif self.tela.btCimaCol.colisao_point(posicaomouse) and self.tela.colunas < 7:
            self.tela.colunas += 1
        elif self.tela.btBaixoCol.colisao_point(posicaomouse) and self.tela.colunas > 2:
            self.tela.colunas -= 1

        elif self.tela.botaoVoltarCriar.colisao_point(posicaomouse) and not self.botaoclicado:
            self.tela.telaCriar = False
            self.tela.telaInicio = True
        elif self.tela.botaoProximo.colisao_point(posicaomouse) and not self.botaoclicado:
            self.tela.jogoPane.modoCriar()
            self.fase = Fase()
            if self.fase.tutorial is not None:
                self.tela.jogoPane.exibindoTutorial = True
            self.fase.desenhoDesafio = Desenho(
                self.tela.linhas, self.tela.colunas, 0)
            self.fase.tentativas = self.tela.execucoes
            self.tela.telaCriar = False
            self.tela.jogoPane.botaoSalvar.mudarImg("BOTAOPROX.PNG")
            self.tela.telaJogo = True

    def _VerificarTelaSaves(self, posicaomouse):
        if self.tela.botaoNovoJogo.colisao_point(posicaomouse):
            self.tela.textoAlerta = (
                "Digite Seu Nome: ", "Pressione OK para continuar")
            self.tela.botaoPlay.append(Sprite("BOTAOPLAY.PNG", 1, 2))
            self.tela.botaolixeira.append(Sprite("lixeira.png", 1, 2))
            self.tela.desenhaNovoJogo = self.tela.caixaTexto.active = True
            self.pressNovojogo = True
        elif self.tela.botaoFasesPersonalizadas.colisao_point(posicaomouse):
            self.tela.fasespersonalizadas = ler_fases()
            if self.tela.fasespersonalizadas is not None:
                self.tela.telaSaves = False
                self.tela.rolagemCriacoes = 0
                self.tela.carregarContornos()
                self.tela.telaFases = True
            else:
                self.tela.textoAlerta = (
                    "Não Existem Fases Criadas", "Crie Novas Fases na opção Criar!")
                self.tela.desenhaAlerta = True

        elif self.tela.botaoVoltar.colisao_point(posicaomouse):
            self.tela.telaSaves = False
            self.tela.telaInicio = True

        elif self.tela.botaoCima.colisao_point(posicaomouse) and self.tela.rolagem < 0:
            self.tela.rolagem += 117
        elif self.tela.botaoBaixo.colisao_point(posicaomouse) and self.tela.rolagem > (
                -117 * (len(self.saves) - 4)):
            self.tela.rolagem -= 117
        else:
            for i in range(0, len(self.tela.saves)):
                x = self.tela.botaoPlay[i]
                l = self.tela.botaolixeira[i]
                if l.colisao_point(posicaomouse) and not self.tela.desenhaConfirmacao:
                    self.tela.desenhaConfirmacao = True
                    self.saveaexcluir = self.saves[i]
                if x.colisao_point(posicaomouse):
                    gerarFases(self.fases)
                    self.tela.telaSaves = False
                    self.jogador = self.saves[i]
                    self.pincel.posicaoInicial()
                    self.fase = self.fases[self.jogador.getNivel()]
                    if self.fase.tutorial is not None:
                        self.tela.jogoPane.exibindoTutorial = True
                    self.tela.telaJogo = True

    def atualizarListaBlMover(self, blocos, fase=False):
        for bl in blocos:
            if bl.get_tipo() == "mover":
                rotacao = self.pincel.rotacao
                for x in self.comando:
                    if x == bl and not fase:
                        break
                    if rotacao < 0:
                        rotacao += 360
                    if rotacao >= 360:
                        rotacao -= 360
                    if x.get_tipo() == "girar_esquerda":
                        rotacao += 90
                    elif x.get_tipo() == "girar_direita":
                        rotacao -= 90
                if rotacao == 0 or rotacao == 360:
                    bl.set_Valor("baixo")
                elif rotacao == 90 or rotacao == 450:
                    bl.set_Valor("direita")
                elif rotacao == 180:
                    bl.set_Valor("cima")
                elif rotacao == 270 or rotacao == -90:
                    bl.set_Valor("esquerda")
                bl.atualizaImgMover()

    def atualizarblMover(self, bl):
        if bl.get_tipo() == "mover":
            rotacao = self.pincel.rotacao
            for x in self.comando:
                if rotacao < 0:
                    rotacao += 360
                if rotacao > 360:
                    rotacao -= 360
                if x.get_tipo() == "girar_esquerda":
                    rotacao += 90
                elif x.get_tipo() == "girar_direita":
                    rotacao -= 90
            if rotacao == 0:
                bl.set_Valor("baixo")
            elif rotacao == 90:
                bl.set_Valor("direita")
            elif rotacao == 180:
                bl.set_Valor("cima")
            else:
                bl.set_Valor("esquerda")
            bl.atualizaImgMover()
        return bl

    def colisaoDesenho(self, desenho):
        intx = 30
        inty = 150
        for i in range(0, desenho.colunas):
            for j in range(0, desenho.linhas):
                quad = pygame.Rect(
                    (self.tela.ajuste / 2) + intx + 85 + (int(75*ESCALAX) * i), 85 + inty + (int(75*ESCALAX) * j), int(75*ESCALAX), int(75*ESCALAX))
                pos = pygame.mouse.get_pos()
                if quad.collidepoint(pos[0] - 115, pos[1] + 115):
                    if (self.pinceledicao == -1 and i == j == 0):
                        self.sons.ALERT.play(2)
                        self.tela.jogoPane.textoaviso = "AÇÃO INVALIDA!", "Você não adicionar janelas na posição inicial!"
                        self.tela.jogoPane.exibeAviso = True
                    elif not (self.tela.jogoPane.finalizacriacao and desenho.tiles[i][j] == -1):
                        desenho.tiles[i][j] = self.pinceledicao
                    else:
                        self.sons.ALERT.play(2)
                        self.tela.jogoPane.textoaviso = "AÇÃO INVALIDA!", "Você não pode remover janelas no desenho desafio!"
                        self.tela.jogoPane.exibeAviso = True

    def _VerificarTelaInicio(self, posicaomouse):
        # BOTÃO VOLUME
        if self.tela.botaoVolume.colisao_point(posicaomouse):
            if self.volume:
                self.tela.botaoVolume.mudarImg("BOTAOVOLUMEOFF.PNG")
                self.volume = False
            else:
                self.tela.botaoVolume.mudarImg("BOTAOVOLUMEON.PNG")
                self.volume = True
            ReproduzirSons(self.volume, SONS)
        # BOTÃO SAIR
        elif self.tela.botaoSair.colisao_point(posicaomouse):
            self.rodando = False
            sys.exit(1)
        # BOTAO JOGAR
        elif self.tela.botaostart.colisao_point(posicaomouse):
            self.tela.telaInicio = False
            self.tela.jogoPane.modoJogar()
            self.tela.botaoPlay.clear()
            self.tela.botaolixeira.clear()
            for x in self.tela.saves:
                self.tela.botaoPlay.append(Sprite("BOTAOPLAY.PNG", 1, 2))
                self.tela.botaolixeira.append(Sprite("lixeira.png", 1, 2))
            self.tela.telaSaves = True
        # BOTAO Criar
        elif self.tela.botaoCriar.colisao_point(posicaomouse):
            self.tela.telaInicio = False
            self.tela.telaCriar = True

    def carregarSaves(self):
        self.saves = ler_saves()
        return self.saves

    def _VerificarTelaFases(self, posicaomaouse):
        if self.tela.botaoEsquerda.colisao_point(posicaomaouse) and self.tela.rolagemCriacoes < 0:
            self.tela.rolagemCriacoes += int(1400*ESCALAX)
        elif self.tela.botaoDireita.colisao_point(posicaomaouse) and self.tela.rolagemCriacoes > (
                -700 * (len(self.tela.fasespersonalizadas) - 2)):
            self.tela.rolagemCriacoes -= int(1400*ESCALAX)
        elif self.tela.btVoltarFases.colisao_point(posicaomaouse):
            self.tela.telaFases = False
            self.tela.telaSaves = True
        else:
            for i in range(0, len(self.tela.contornoFase)):
                if self.tela.contornoFase[i].colisao_point(posicaomaouse):
                    self.index = i
                    self.fase = self.tela.fasespersonalizadas[i]
                    self.jogandoFasePersonalizada = True
                    self.jogador = None
                    self.tela.telaFases = False
                    self.tela.telaJogo = True
                    break

    def verificardesenho(self):
        if self.verificandodesenho:
            if self.i < self.fase.desenhoDesafio.colunas:
                self.tela.jogoPane.desenharVerificacao(self.i, self.j)
            if self.espera > 4:
                # print("Teste["+str(self.i)+","+str(self.j)+"]")
                self.espera = 0
                if self.i < self.fase.desenhoDesafio.colunas:
                    if int(self.fase.desenhoDesafio.tiles[self.i][self.j]) != int(self.fase.desenhoResposta.tiles[self.i][self.j]):
                        self.sons.NEGAR.play()
                        self.verificandodesenho = False
                        self.exibindoperda = True

                    self.i += 1
                    self.sons.CONFIRMAR.play()
                elif self.j < self.fase.desenhoDesafio.linhas-1:
                    self.i = 0
                    self.j += 1
                else:
                    self.verificandodesenho = False
                    self.i = self.j = 0
                    self.ganhou()
            else:
                self.espera += 1
        elif self.exibindoperda:
            # if self.fase.tentativas > 1:
            self.tela.jogoPane.destaque = True
            self.tela.jogoPane.desenharVerificacao(
                self.i-1, self.j, passou=False)
            if self.esperaperda > 20:
                self.esperaperda = 0
                self.exibindoperda = False
                self.i = self.j = 0
                # if self.fase.tentativas > 1:
                self.sons.MENOS.play()
                self.tela.jogoPane.destaque = False
                self.fase.tentativas -= 1
                # else:
                if self.fase.tentativas < 1:
                    self.perdeu()
            else:
                self.esperaperda += 1
