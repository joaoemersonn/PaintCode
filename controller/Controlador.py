import os
from os.path import join
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
from util.Gerador import gerarFases, getTutorials
from util.Util import gravar_saves, gravar_fase, ler_fases, ReproduzirSons, criarPastas, Cores, carrega_imagem, SONS, \
    ESCALAX
from util.Util import ler_saves
from view.Tela import Tela
from view.PainelJogo import escalarX, escalarY

TOCAREMLOOP = -1


class Controlador:
    def __init__(self):
        self._carregando = True
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        info = pygame.display.Info()
        self.largura, self.altura = info.current_w, info.current_h
        # largura = 1000
        # altura = 768
        # (largura,altura), pygame.FULLSCREEN
        self.window = self.janela = Util.WINDOW
        self.window.fill(Cores.BRANCO)
        self.tamFuncaoComando = 0
        self.tamFuncaoComandoAnterior = 0
        self.splash = carrega_imagem("splash.png", escala=2)
        # self.gif = GIFImage("loading.gif")
        self.window.blit(self.splash, ((self.largura/2) -
                                       (self.splash.get_width()/2), 150))
        #####
        # self.fps = 120
        # self.TICKS_PER_SECOND = Util.Config.VELOCIDADE
        self.SKIP_TICKS = 1000 / Util.Config.VELOCIDADE
        self.MAX_FRAMESKIP = 5
        self.next_game_tick = pygame.time.get_ticks()
        self.segurandoBloco = False
        self.tela = None
        self.i = self.index = 0
        self._velociadeAnterior = 60
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.pressNovojogo = self.executandoComando = False
        self.saves = list()
        self.tam = 0
        self.tamAnterior = 0
        self.comando = list()
        self.manterComando = False
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
        self.animarTesteVl = 0
        self.blOpcaoTrue = None
        self.faseSelecionada = 0
        self.__inicioF = None
        self.comandoAnterior = None
        self.tutoriais = None
        # self.lixeira = self.play = None
        ###
        # self.gif.executar(self.window, 950, 350)
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
        self.__inicioF = Bloco("inicioF")
        self.play = Sprite("BOTAOPLAY.PNG", 1, 2)
        self.lixeira = Sprite("lixeira.png", 1, 2)
        self.pincel = Pincel()
        self.comando.append(self.__inicio)
        self.tela.jogoPane.funcaoComando.append(self.__inicioF)
        self.tutoriais = getTutorials()
        gerarFases(self.fases, self.tutoriais)
        self.tam = 0
        self.sons.BACKGROUND.set_volume(0.2)
        self.sons.BACKGROUND.play(TOCAREMLOOP)
        self.carregarConfig()
        Util.CARREGANDO = False
        self._carregando = False

    def start(self):
        while self.rodando:
            loops = 0
            self.tela.desenhar()
            if self.jogoexecutando():
                self.desenharaviso()
                self.tela.jogoPane.desenhar(
                    self.fase, self.jogador, self.comando, self.pincel, self.tela.desenhaAlerta, self.tutoriais)
                self.verificardesenho()
            # while pygame.time.get_ticks() > self.next_game_tick and loops < self.MAX_FRAMESKIP:
            #     if self.tela.telaConfig:
            #         pass
            #     if self.executandoComando:
            #         self.executarcomando()
            #     self.tratarEventos()
            #     self.next_game_tick += self.SKIP_TICKS
            #     loops += 1

            if self.executandoComando:
                self.executarcomando()
            self.tratarEventos()
            # Desenha Animação
            # if self.animarTesteVl > 0 and self.tela.telaConfig:
            #     print("animarVl: ", self.animarTesteVl)
            #     for i in range(0, 10):
            #         print("TesteAnimação: ", i)
            #     self.tela.jogoPane.confete.animar(
            #         self.tela.janela, 1)
            if self.tela.jogoPane.tempoAnGanhou > 0:
                sc = None
                if self.tela.telaConfig:
                    sc = self.tela.janela
                    for i in range(0, 100):
                        pass
                self.tela.jogoPane.desenharAnimacaoWin(
                    self.faseanterior, self.jogador, self.comando, self.pincel, sc=sc)

            pygame.display.update()
            self.relogio.tick(Util.Config.VELOCIDADE)

    def jogoexecutando(self):
        if self.tela.telaJogo and not self.tela.desenhaConfirmacao:
            return True
        return False

    def executarcomando(self):
        if self.espera > 20:
            self.espera = 0

            concluido = self.pincel.mover(self.comando[1], self.fase.desenhoDesafio,
                                          self, comandofn=self.tela.jogoPane.funcaoComando)
            self.comando.pop(1)
            self.tam -= 1
            print(self.tam)
            if not concluido:
                self.executandoComando = False
                self.perdeu("MOVIMENTO INVÁLIDO!",
                            "Você não completou o objetivo")
                # self.sons.ALERT.play(1)
                # self.tela.jogoPane.textoaviso = "MOVIMENTO INVÁLIDO!", "Pincel só pode mover para direção de sua base!"
                # self.tela.jogoPane.exibeAviso = True
                # faseindex = self.fase.nivel-1
                # gerarFases(self.fases, getTutorials())
                # self.fase = self.fases[faseindex]
                # self.refreshDesenho()
                # self.pincel.posicaoInicial()
                # self.tam = self.tamAnterior
                # self.comando = self.comandoAnterior
            elif self.tam < 1 or len(self.comando) <= 1:
                self.refreshDesenho()
                self.executandoComando = False
                self.tam = 0
                self.verificandodesenho = True
        else:
            self.espera += ((Util.Config.VELOCIDADE/60))

    def desenharaviso(self):
        if self.tela.jogoPane.exibeAviso:
            if self.contaviso > 100:
                self.contaviso = 0
                self.tela.jogoPane.exibeAviso = False
            else:
                self.contaviso += 1

    def perdeu(self, titulo="Você não completou o objetivo.", sub=" A casa não está pintada corretamente."):
        self.sons.LOSE.play()
        self.i = self.j = 0
        self.refreshDesenho()
        self.tela.textoAlerta = (
            titulo, sub)
        self.tela.desenhaalertaCaixaPerdeu = self.tela.opcoesFases = self.tela.desenhaAlerta = True
        self.pincel.posicaoInicial()
        self.manterComando = True
        # if self.jogandoFasePersonalizada:
        #     self.tela.fasespersonalizadas = ler_fases()
        #     self.fase = self.tela.fasespersonalizadas[self.index]
        #     self.atualizarListaBlMover(self.fase.blocosdisponiveis, True)
        # else:
        #     gerarFases(self.fases, getTutorials())
        #     #self.tam = 0
        #     # self.limparFnComando()
        #     #self.fase = self.fases[self.faseSelecionada]
        #     self.atualizarListaBlMover(self.fase.blocosdisponiveis, True)

    def ganhou(self):
        self.i = self.j = 0
        if self.jogandoFasePersonalizada:
            self.sons.WIN.play()
            self.faseanterior = self.fase
            self.tela.jogoPane.reinicarAnimacaoConfete()
            self.tela.jogoPane.tempoAnGanhou = (57 * 4)
            self.tela.textoAlerta = ("Parabéns você concluiu a fase!", "")
            self.pincel.posicaoInicial()
            self.tela.fasespersonalizadas = ler_fases()
            self.tela.opcoesFases = self.tela.desenhaAlerta = True
        elif self.fase.nivel <= 14 or len(self.fases) > self.jogador.getNivel() + 1:
            self.sons.WIN.play()
            self.faseanterior = self.fase
            self.tela.jogoPane.reinicarAnimacaoConfete()
            self.tela.jogoPane.tempoAnGanhou = (57 * 4)
            self.tela.textoAlerta = ("Parabéns você concluiu o nível!", "")
            self.tela.continua = self.tela.opcoesFases = self.tela.desenhaAlerta = True
            if self.fase.nivel > int(self.jogador.getNivel()):
                self.jogador.subirNivel()

            self.pincel.posicaoInicial()
            self.limparFnComando()
            # self.fase = self.fases[self.jogador.getNivel()]
            self.atualizarListaBlMover(self.fase.blocosdisponiveis, True)
            gravar_saves(self.saves)
        else:
            self.sons.WIN.play()
            self.faseanterior = self.fase
            self.tela.jogoPane.reinicarAnimacaoConfete()
            self.tela.jogoPane.tempoAnGanhou = (57 * 4)
            self.tela.textoAlerta = (
                "Parabéns você concluiu o jogo!", "")
            self.tela.opcoesFases = self.tela.desenhaAlerta = True
            self.limparFnComando()
            self.fimdejogo = True
            self.pincel.posicaoInicial()
            gravar_saves(self.saves)

    def refreshDesenho(self):
        self.tela.desenhar()
        self.tela.jogoPane.desenhar(
            self.fase, self.jogador, self.comando, self.pincel)
        pygame.display.update()

    def tratarEventos(self):
        posicaomaouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        if self.pressNovojogo:
            self.tela.caixaTexto.listen(events)
        elif self.tela.telaMenuFases:
            for x in self.tela.botoesFases:
                x.listen(events)
                if x.clicked and int(x.string) <= int(self.jogador.getNivel())+1:
                    self.faseSelecionada = int(x.string)-1
                    gerarFases(self.fases, getTutorials())
                    self.tam = 0
                    self.limparFnComando()
                    self.fase = self.fases[self.faseSelecionada]
                    self.atualizarListaBlMover(
                        self.fase.blocosdisponiveis, True)
                    self.tela.jogoPane.exibindoTutorial = (
                        self.fase.tutorial is not None and self.tela.jogoPane.opcaosempreTutorial)
                    self.tela.jogoPane.indexTutorial = 0
                    self.tela.nivelJogador = int(self.jogador.getNivel())
                    x.clicked = False
                    self.tela.telaMenuFases = False
                    self.tela.telaJogo = True
                    self.esperaJogoAparecer = False
        elif self.tela.telaConfig:
            self.tela.sliderVl.listen(events)
            Util.Config.VELOCIDADE = self.tela.sliderVl.value
            if self.tela.jogoPane.tempoAnGanhou <= 0:
                self.tela.jogoPane.tempoAnGanhou = (60 * 4)
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.rodando = False
                sys.exit(1)
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN) and self.tela.telaJogo and self.tela.jogoPane.criando and pygame.mouse.get_pressed()[0]:
                self.colisaoDesenho(self.fase.desenhoDesafio)
            # CLIQUE MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tela.telaMenuFases:
                    if self.tela.botaoVoltar.colisao_point(posicaomaouse):
                        self.tela.telaMenuFases = False
                        self.tela.telaSaves = True
                elif self.tela.telaJogo and not self.tela.desenhaAlerta and not self.tela.desenhaConfirmacao and not self.tela.jogoPane.exibindoTutorial:
                    self._VerificarTelaJogo(posicaomaouse)
                elif self.tela.telaJogo and self.tela.jogoPane.exibindoTutorial:
                    # if self.fase.tutorial is None or len(self.fase.tutorial) <= self.tela.jogoPane.indexTutorial:
                    #     self.tela.jogoPane.exibindoTutorial = False
                    #     break
                    # img = self.fase.tutorial[self.tela.jogoPane.indexTutorial]
                    # print("x",img.get_rect().x," y:",img.get_rect().y,"w:",img.get_rect().w," h:",img.get_rect().h)
                    if self.tela.jogoPane.checkbox.colisao_point(posicaomaouse):
                        self.tela.jogoPane.opcaosempreTutorial = not self.tela.jogoPane.opcaosempreTutorial
                        if self.tela.jogoPane.opcaosempreTutorial:
                            self.tela.jogoPane.checkbox.mudarImg("boxon.png")
                        else:
                            self.tela.jogoPane.checkbox.mudarImg("boxoff.png")
                    elif self.tela.jogoPane.botaoEsquerda.colisao_point(posicaomaouse) and self.tela.jogoPane.indexTutorial > 0:
                        self.tela.jogoPane.indexTutorial -= 1
                    elif self.tela.jogoPane.botaoDireita.colisao_point(posicaomaouse) or (self.esperaJogoAparecer and pygame.Rect((
                            self.largura/2)-(793/2), (self.altura/2)-(529/2), 793, 529).collidepoint(posicaomaouse)):
                        self.tela.jogoPane.indexTutorial += 1
                    elif self.tela.jogoPane.botaoPularTutorial.colisao_point(posicaomaouse):
                        self.tela.jogoPane.exibindoTutorial = False

            elif event.type == pygame.MOUSEBUTTONUP:
                self.esperaJogoAparecer = True
                if self.tela.desenhaConfirmacao:
                    if self.tela.cancelarbotao.colisao_point(posicaomaouse):
                        self.tela.desenhaConfirmacao = False
                    if self.tela.confirmarbotao.colisao_point(posicaomaouse):
                        self.saves.remove(self.saveaexcluir)
                        gravar_saves(self.saves)
                        self.tela.desenhaConfirmacao = False
                elif self.tela.desenhaNovoJogo:
                    if self.tela.cancelarbotao.colisao_point(posicaomaouse):
                        self.tela.caixaTexto.cursorPosition = 0
                        self.tela.caixaTexto.setText("")
                        self.tela.desenhaNovoJogo = False
                    if self.tela.confirmarbotao.colisao_point(posicaomaouse):
                        if self.pressNovojogo:
                            self.gerarNovoJogo()

                elif self.tela.desenhaAlerta and self.tela.ok.colisao_point(posicaomaouse) and not self.tela.opcoesFases:
                    self.tela.jogoPane.tempoAnGanhou = 0
                    self.tela.desenhaAlerta = not self.tela.desenhaAlerta
                    # if self.fase is not None and self.fase.tentativas is not None:
                    #     self.tela.jogoPane.exibindoTutorial = True
                    #     self.tela.jogoPane.indexTutorial = 0
                    #     if self.manterComando:
                    #         self.tam = self.tamAnterior
                    #         self.comando = self.comandoAnterior
                    #         self.manterComando = False
                    # if self.jogandoFasePersonalizada:
                    #     self.jogandoFasePersonalizada = False
                    #     self.tela.telaFases = True
                    #     self.tela.telaJogo = False
                    # elif self.fimdejogo or (self.jogador is not None and self.fase.nivel <= int(self.jogador.getNivel())):
                    #     self.fimdejogo = self.tela.telaJogo = False
                    #     self.tela.telaMenuFases = True
                elif self.tela.opcoesFases and self.tela.reiniciar.colisao_point(posicaomaouse):
                    self.tela.jogoPane.tempoAnGanhou = 0
                    self.tela.desenhaalertaCaixaPerdeu = self.desenhaalertaCaixaPerdeu = self.tela.continua = self.tela.opcoesFases = self.tela.desenhaAlerta = False
                    print("reiniciou!")
                    self.sons.REINICAR.play()
                    self.pincel.posicaoInicial()
                    self.comando.clear()
                    self.comando.append(self.__inicio)
                    if self.jogandoFasePersonalizada:
                        self.tam = 0
                        self.tela.fasespersonalizadas = ler_fases()
                        self.fase = self.tela.fasespersonalizadas[self.index]
                        self.atualizarListaBlMover(
                            self.fase.blocosdisponiveis, True)
                    else:
                        faseindex = self.fase.nivel-1
                        print("fase nivel:", self.fase.nivel,
                              " index:", faseindex)
                        gerarFases(self.fases, getTutorials())
                        if self.manterComando:
                            self.tam = self.tamAnterior
                            self.comando = self.comandoAnterior
                            self.manterComando = False
                        else:
                            self.tam = 0
                        # self.limparFnComando()
                        self.fase = self.fases[faseindex]
                        self.atualizarListaBlMover(
                            self.fase.blocosdisponiveis, True)
                elif self.tela.continua and self.tela.continuar.colisao_point(posicaomaouse):
                    self.tela.jogoPane.tempoAnGanhou = 0                    
                    self.tela.desenhaalertaCaixaPerdeu = self.tela.continua = self.tela.opcoesFases = self.tela.desenhaAlerta = False
                    prox = self.fase.nivel
                    self.fase = self.fases[prox]
                    self.tela.jogoPane.exibindoTutorial = (
                        self.fase.tutorial is not None and self.tela.jogoPane.opcaosempreTutorial)
                    self.tela.jogoPane.indexTutorial = 0
                elif self.tela.opcoesFases and self.tela.menu.colisao_point(posicaomaouse):
                    self.tela.desenhaalertaCaixaPerdeu = self.tela.continua = self.tela.opcoesFases = self.tela.desenhaAlerta = False
                    if self.jogandoFasePersonalizada:
                        self.jogandoFasePersonalizada = False
                        self.tela.telaFases = True
                        self.tela.telaJogo = False
                    # self.fimdejogo or (self.jogador is not None and self.fase.nivel <= int(self.jogador.getNivel())):
                    else:
                        self.tela.nivelJogador = int(self.jogador.getNivel())
                        self.fimdejogo = self.tela.telaJogo = False
                        self.tela.telaMenuFases = True
                        self.tratarEventos()
                elif self.tela.telaCriar:
                    self._VerificarTelaCriar(posicaomaouse)
                elif self.tela.telaConfig:
                    self._VerificarTelaConfig(posicaomaouse)
                elif self.tela.telaInicio:
                    self._VerificarTelaInicio(posicaomaouse)
                elif self.tela.telaAjuda:
                    self._verificarTelaAjuda(posicaomaouse)
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
                                    self.tela.jogoPane.textoaviso = "MOVIMENTO INVÁLIDO!", "Não é possível colocar um bloco de repetição em outro!"
                                    self.tela.jogoPane.exibeAviso = True
                                else:
                                    if self.tam <= 12:
                                        if c.blocos is None:
                                            c.blocos = list()
                                        bl = Bloco(x.get_tipo(), x.get_Valor())
                                        # bl = self.atualizarblMover(bl)
                                        c.blocos.append(bl)
                                        self.tam += 1
                                    else:
                                        self.sons.ALERT.play(1)
                                        self.tela.jogoPane.textoaviso = "TAMANHO MÁXIMO!", "Comando atingiu limite máximo de blocos!"
                                        self.tela.jogoPane.exibeAviso = True
                                x.pressionado = False
                                self.segurandoBloco = False
                        for c in self.tela.jogoPane.funcaoComando:
                            if x.pressionado and c.get_tipo() == "repetir" and c.colisao_rect(x.get_rect()):
                                if x.get_tipo() == "repetir":
                                    self.sons.ALERT.play(2)
                                    self.tela.jogoPane.textoaviso = "MOVIMENTO INVÁLIDO!", "Não é possível colocar um bloco de repetição em outro!"
                                    self.tela.jogoPane.exibeAviso = True
                                else:
                                    if self.tamFuncaoComando <= 12:
                                        if c.blocos is None:
                                            c.blocos = list()
                                        bl = Bloco(x.get_tipo(), x.get_Valor())
                                        # bl = self.atualizarblMover(bl)
                                        c.blocos.append(bl)
                                        self.tamFuncaoComando += 1
                                    else:
                                        self.sons.ALERT.play(1)
                                        self.tela.jogoPane.textoaviso = "TAMANHO MÁXIMO!", "Comando atingiu limite máximo de blocos!"
                                        self.tela.jogoPane.exibeAviso = True
                                x.pressionado = False
                                self.segurandoBloco = False
                        if x.pressionado and x.colisao_rect(self.tela.jogoPane.boxFuncao) and self.tela.jogoPane.fndesenha:
                            if x.get_tipo() == "blocoF":
                                self.sons.ALERT.play(1)
                                self.tela.jogoPane.textoaviso = "MOVIMENTO INVÁLIDO!", "Bloco de Função não pode fazer parte da função!"
                                self.tela.jogoPane.exibeAviso = True

                            elif self.tamFuncaoComando <= 12:
                                if x.get_tipo() == "repetir":
                                    x.set_Valor(4)
                                    # self.tamFuncaoComando += 1
                                self.sons.COLOCAR.play()
                                if x.get_tipo() == "mover":
                                    bloco = Bloco(x.get_tipo())
                                else:
                                    bloco = Bloco(
                                        x.get_tipo(), x.get_Valor())
                                self.tela.jogoPane.funcaoComando.append(bloco)
                                self.tamFuncaoComando += 1

                            else:
                                self.sons.ALERT.play(1)
                                self.tela.jogoPane.textoaviso = "TAMANHO MÁXIMO!", "Função atingiu limite máximo de blocos!"
                                self.tela.jogoPane.exibeAviso = True

                        elif x.pressionado and x.colisao_rect(self.tela.jogoPane.get_boxExecucao()):
                            if self.tam <= 12:
                                self.sons.COLOCAR.play()
                                bloco = Bloco(x.get_tipo(), x.get_Valor())
                                if bloco.get_tipo() == "repetir":
                                    # self.tam += 1
                                    bloco.set_Valor(4)
                                # elif bloco.get_tipo() == "blocoF":
                                #     if bloco.blocos is None:
                                #         bloco.blocos = list()
                                #         bloco.blocos.append(Bloco("inicioF"))
                                # bloco = self.atualizarblMover(bloco)
                                self.comando.append(bloco)
                                self.tam += 1
                            else:
                                self.sons.ALERT.play(1)
                                self.tela.jogoPane.textoaviso = "TAMANHO MÁXIMO!", "Comando atingiu limite máximo de blocos!"
                                self.tela.jogoPane.exibeAviso = True
                        x.pressionado = self.segurandoBloco = False
                    self.atualizarListaBlMover(self.comando)
                    self.atualizarListaBlMover(
                        self.fase.blocosdisponiveis, True)

    def limparFnComando(self):
        self.tam = 0
        self.comando.clear()
        self.comando.append(self.__inicio)

        self.tamFuncaoComando = 0
        self.tela.jogoPane.funcaoComando.clear()
        self.tela.jogoPane.funcaoComando.append(self.__inicioF)

    def gerarNovoJogo(self):
        self.tela.desenhaNovoJogo = self.pressNovojogo = False
        gerarFases(self.fases, getTutorials())
        self.tam = 0
        self.limparFnComando()
        if Util.Config.MOBILE:
            self.jogador = Jogador("Save "+str(len(self.saves)+1))
        else:
            self.jogador = Jogador(
                "".join(self.tela.caixaTexto.text))
            self.tela.caixaTexto.cursorPosition = 0
            self.tela.caixaTexto.setText("")
        self.saves.append(self.jogador)
        gravar_saves(self.saves)
        self.pincel.posicaoInicial()
        self.tela.botaoPlay.append(
            Sprite("BOTAOPLAY.PNG", 1, 2))
        self.tela.nivelJogador = int(
            self.jogador.getNivel())
        self.tela.telaSaves = False
        self.tela.telaMenuFases = True

    def _verificarTelaAjuda(self, posicaomaouse):
        tutoriais = getTutorials()
        img = tutoriais[self.tela.indexAjuda]
        if self.tela.jogoPane.checkbox.colisao_point(posicaomaouse):
            self.tela.jogoPane.opcaosempreTutorial = not self.tela.jogoPane.opcaosempreTutorial
            if self.tela.jogoPane.opcaosempreTutorial:
                self.tela.jogoPane.checkbox.mudarImg("boxon.png")
            else:
                self.tela.jogoPane.checkbox.mudarImg("boxoff.png")
        elif self.tela.jogoPane.botaoEsquerda.colisao_point(posicaomaouse) and self.tela.indexAjuda > 1:
            self.tela.indexAjuda -= 1
        elif self.tela.jogoPane.botaoDireita.colisao_point(posicaomaouse) or (img is not None and pygame.Rect((
                self.largura/2)-(img.get_rect().w/2), (self.altura/2)-(img.get_rect().h/2), img.get_rect().w, img.get_rect().h).collidepoint(posicaomaouse)):
            self.tela.indexAjuda += 1
        if self.tela.jogoPane.botaoPularTutorial.colisao_point(posicaomaouse) or len(tutoriais) < self.tela.indexAjuda:
            self.tela.telaAjuda = False
            self.tela.telaInicio = True
            self.tela.indexAjuda = 1

    def _VerificarTelaConfig(self, posicaomouse):
        # if self.tela.btCimaVel.colisao_point(posicaomouse) and Util.Config.VELOCIDADE < 150:
        #     Util.Config.VELOCIDADE += 10
        # elif self.tela.btBaixoVel.colisao_point(posicaomouse) and Util.Config.VELOCIDADE > 20:
        #     Util.Config.VELOCIDADE -= 10
        if self.tela.botaoConfirmar.colisao_point(posicaomouse):
            Util.gravarConfig(Util.Config.VELOCIDADE)
            # self.SKIP_TICKS = 1000 / Util.Config.VELOCIDADE
            self.tela.telaConfig = False
            self.tela.telaInicio = True
        elif self.tela.botaoVoltar.colisao_point(posicaomouse):
            self.tela.telaConfig = False
            self.tela.telaInicio = True
            self.tela.sliderVl.value = Util.Config.VELOCIDADE = self._velociadeAnterior

    def _VerificarTelaJogo(self, posicaomouse):

        if self.tela.jogoPane.criando:
            # self.colisaoDesenho(self.fase.desenhoDesafio)
            lista = self.tela.jogoPane.coresEdicao
            for i in range(0, len(lista)):
                if lista[i].collidepoint(posicaomouse):
                    self.pinceledicao = i - 1
            self.tela.jogoPane.trocarimgPincel(self.pinceledicao)
            if self.tela.jogoPane.botaoSalvar.colisao_point(posicaomouse) and not self.tela.jogoPane.finalizacriacao:
                # self.tela.textoAlerta = (
                #    "PRONTO!", "", "Agora Modifique o desenho para ser o desafio a ser cumprido")
                self.pinceledicao = 0
                self.tela.jogoPane.trocarimgPincel(self.pinceledicao)
                self.tela.jogoPane.botaoSalvar.mudarImg("BOTAOSALVAR.PNG")
                # self.tela.desenhaAlerta = True
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
                    "Nível criado com sucesso!", "", "")
                self.tela.desenhaAlerta = True
                self.tela.telaJogo = False
                self.tela.telaInicio = True
        if self.tela.btAjuda.colisao_point(posicaomouse):
            # self.tela.indexAjuda = 1
            self.tela.jogoPane.indexTutorial = 0
            self.tela.jogoPane.exibindoTutorial = True
        elif self.tela.botaoVolume.colisao_point(posicaomouse):
            if self.volume:
                self.tela.botaoVolume.mudarImg("BOTAOVOLUMEOFF.PNG")
                self.volume = False
            else:
                self.tela.botaoVolume.mudarImg("BOTAOVOLUMEON.PNG")
                self.volume = True
        ReproduzirSons(self.volume, SONS)
        # or (self.tela.opcoesFases and self.tela.reiniciar.colisao_point(posicaomouse)):
        if self.tela.jogoPane.reiniciarbotao.colisao_point(posicaomouse):
            self.tela.desenhaalertaCaixaPerdeu = self.tela.continua = self.tela.opcoesFases = self.tela.desenhaAlerta = False
            self.sons.REINICAR.play()
            self.pincel.posicaoInicial()
            self.comando.clear()
            self.comando.append(self.__inicio)
            # self.tam = 0
            # if self.manterComando:
            #     self.tam = self.tamAnterior
            #     self.comando = self.comandoAnterior
            #     self.manterComando = False
            if self.jogandoFasePersonalizada:
                self.tam = 0
                self.tela.fasespersonalizadas = ler_fases()
                self.fase = self.tela.fasespersonalizadas[self.index]
                self.atualizarListaBlMover(self.fase.blocosdisponiveis, True)
            else:
                faseindex = self.fase.nivel-1
                gerarFases(self.fases, getTutorials())
                self.tam = 0
                self.limparFnComando()
                self.fase = self.fases[faseindex]
                self.atualizarListaBlMover(self.fase.blocosdisponiveis, True)
        elif self.tela.opcoesFases and self.tela.menu.colisao_point(posicaomouse):
            self.desenhaalertaCaixaPerdeu = self.tela.continua = self.tela.opcoesFases = self.tela.desenhaAlerta = False
            if self.jogandoFasePersonalizada:
                self.jogandoFasePersonalizada = False
                self.tela.telaFases = True
                self.tela.telaJogo = False
            # self.fimdejogo or (self.jogador is not None and self.fase.nivel <= int(self.jogador.getNivel())):
            else:
                self.fimdejogo = self.tela.telaJogo = False
                self.tela.telaMenuFases = True
        elif self.tela.jogoPane.botaoVoltar.colisao_point(posicaomouse):
            self.botaoclicado = True
            if self.tela.jogoPane.criando:
                self.tela.telaCriar = True
                self.tela.jogoPane.finalizacriacao = False
            else:
                self.comando.clear()
                self.comando.append(self.__inicio)
                if self.jogandoFasePersonalizada:
                    self.tela.telaFases = True
                    self.jogandoFasePersonalizada = False
                else:
                    self.tela.nivelJogador = int(
                        self.jogador.getNivel())
                    self.tela.telaMenuFases = True
            self.tela.telaJogo = False
        # Executar
        elif self.tela.jogoPane.get_executarButton().colisao_point(posicaomouse) and len(self.comando) > 1:
            self.tamAnterior = self.tam
            self.comandoAnterior = self.comando.copy()
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
                self.segurandoBloco = True
        i = 0
        self.tela.jogoPane.temComandoSelecionado = False
        for x in self.tela.jogoPane.funcaoComando:
            if x.selecionado:
                self.tela.jogoPane.temComandoSelecionado = True
                self.tela.jogoPane.funcaoOpcaoAtiva = True
                if self.tela.jogoPane.lixo.colisao_point(posicaomouse):
                    self.sons.DELETE.play()
                    if x.get_tipo() == "repetir" and x.blocos is not None:
                        # self.tamFuncaoComando -= 1
                        for sb in x.blocos:
                            self.tamFuncaoComando -= 1
                    self.tela.jogoPane.funcaoComando.remove(x)
                    self.tamFuncaoComando -= 1
                    break
                if self.tela.jogoPane.moverEsquerda.colisao_point(posicaomouse) and i > 1:
                    aux = self.tela.jogoPane.funcaoComando[i - 1]
                    self.tela.jogoPane.funcaoComando[i - 1] = x
                    self.tela.jogoPane.funcaoComando[i] = aux
                    break
                if self.tela.jogoPane.moverDireita.colisao_point(posicaomouse) and (i + 1) < len(self.tela.jogoPane.funcaoComando):
                    aux = self.tela.jogoPane.funcaoComando[i + 1]
                    self.tela.jogoPane.funcaoComando[i + 1] = x
                    self.tela.jogoPane.funcaoComando[i] = aux
                    break
                if self.tela.jogoPane.repetir.colisao_point(posicaomouse):
                    self.tela.jogoPane.mostrarEditBlRepetir = not self.tela.jogoPane.mostrarEditBlRepetir
                    if self.tela.jogoPane.mostrarEditBlRepetir:
                        self.blOpcaoTrue = x
                if self.tela.jogoPane.funcaoOpcao.colisao_point(posicaomouse):
                    self.tela.jogoPane.funcaoOpcaoAtiva = not self.tela.jogoPane.funcaoOpcaoAtiva
                    if self.tela.jogoPane.funcaoOpcaoAtiva:
                        self.blOpcaoTrue = x
                if self.tela.jogoPane.corOpcao.colisao_point(posicaomouse):
                    self.tela.jogoPane.mostrarEditBlCor = not self.tela.jogoPane.mostrarEditBlCor
                    if self.tela.jogoPane.mostrarEditBlCor:
                        self.blOpcaoTrue = x
                if x.get_tipo() == "repetir" and self.tela.jogoPane.mostrarEditBlRepetir:
                    if self.tela.jogoPane.seta.colisao_point(posicaomouse) and x.Value > 2:
                        x.Value -= 1
                    elif self.tela.jogoPane.seta2.colisao_point(posicaomouse) and x.Value < 9:
                        x.Value += 1
                if x.get_tipo() == "selecionar_cor" and self.tela.jogoPane.mostrarEditBlCor:
                    vl = 0
                    tambl = 70
                    posi = x.get_rect()
                    for cor in self.fase.coresdisponiveis:
                        rect = pygame.Rect(
                            (
                                posi.x + 5 + escalarX(tambl + 2) * vl, posi.y - escalarY(157), escalarX(tambl), escalarY(tambl)))
                        if rect.collidepoint(posicaomouse):
                            x.set_Valor(cor)
                        vl += 1
            auxy = 0
            if x.get_tipo() == "repetir" or x.get_tipo() == "selecionar_cor":
                auxy = 60
            tamx = 200 + auxy
            if x.get_rect().collidepoint(posicaomouse) and x.get_tipo() != "inicio":
                x.selecionado = not x.selecionado
                if not x.selecionado:
                    self.tela.jogoPane.funcaoOpcaoAtiva = False
                if x.selecionado:
                    self.tela.jogoPane.funcaoOpcaoAtiva = True
            elif x.selecionado and pygame.Rect(x.get_rect().x, x.get_rect().y - escalarY(75), escalarX(tamx), escalarY(70)).collidepoint(posicaomouse):
                pass
            elif x.selecionado and x.get_tipo() == "repetir" and (pygame.Rect(x.get_rect().x, x.get_rect().y - escalarY(175), escalarX(300), escalarY(100)).collidepoint(posicaomouse)):
                pass
            # :
            elif x.selecionado and x.get_tipo() == "blocoF" and (self.tela.jogoPane.boxFuncao.collidepoint(posicaomouse) or self.segurandoBloco):
                pass
            else:
                if self.blOpcaoTrue == x:
                    self.tela.jogoPane.mostrarEditBlCor = self.tela.jogoPane.funcaoOpcaoAtiva = self.tela.jogoPane.mostrarEditBlRepetir = False
                    self.blOpcaoTrue = None
                self.tela.jogoPane.funcaoOpcaoAtiva = False
                x.selecionado = False

            i += 1
        i = 0
        if not self.tela.jogoPane.temComandoSelecionado:
            for x in self.comando:
                if x.selecionado:
                    if self.tela.jogoPane.lixo.colisao_point(posicaomouse):
                        self.sons.DELETE.play()
                        # self.tam -= 1
                        if x.get_tipo() == "repetir" and x.blocos is not None:
                            for sb in x.blocos:
                                self.tam -= 1
                        self.comando.remove(x)
                        self.tam -= 1
                        break
                    if self.tela.jogoPane.moverEsquerda.colisao_point(posicaomouse) and i > 1:
                        aux = self.comando[i - 1]
                        self.comando[i - 1] = x
                        self.comando[i] = aux
                        break
                    if self.tela.jogoPane.moverDireita.colisao_point(posicaomouse) and (i + 1) < len(self.comando):
                        aux = self.comando[i + 1]
                        self.comando[i + 1] = x
                        self.comando[i] = aux
                        break
                    if self.tela.jogoPane.repetir.colisao_point(posicaomouse):
                        self.tela.jogoPane.mostrarEditBlRepetir = not self.tela.jogoPane.mostrarEditBlRepetir
                        if self.tela.jogoPane.mostrarEditBlRepetir:
                            self.blOpcaoTrue = x
                    if self.tela.jogoPane.funcaoOpcao.colisao_point(posicaomouse):
                        self.tela.jogoPane.funcaoOpcaoAtiva = not self.tela.jogoPane.funcaoOpcaoAtiva
                        if self.tela.jogoPane.funcaoOpcaoAtiva:
                            self.blOpcaoTrue = x
                    if self.tela.jogoPane.corOpcao.colisao_point(posicaomouse):
                        self.tela.jogoPane.mostrarEditBlCor = not self.tela.jogoPane.mostrarEditBlCor
                        if self.tela.jogoPane.mostrarEditBlCor:
                            self.blOpcaoTrue = x
                    if x.get_tipo() == "repetir" and self.tela.jogoPane.mostrarEditBlRepetir:
                        if self.tela.jogoPane.seta.colisao_point(posicaomouse) and x.Value > 2:
                            x.Value -= 1
                        elif self.tela.jogoPane.seta2.colisao_point(posicaomouse) and x.Value < 9:
                            x.Value += 1
                    if x.get_tipo() == "selecionar_cor" and self.tela.jogoPane.mostrarEditBlCor:
                        vl = 0
                        tambl = 70
                        posi = x.get_rect()
                        for cor in self.fase.coresdisponiveis:
                            rect = pygame.Rect(
                                (
                                    posi.x + 5 + escalarX(tambl + 2) * vl, posi.y - escalarY(157), escalarX(tambl), escalarY(tambl)))
                            if rect.collidepoint(posicaomouse):
                                x.set_Valor(cor)
                            vl += 1
                auxy = 0
                if x.get_tipo() == "repetir" or x.get_tipo() == "selecionar_cor":
                    auxy = 60
                tamx = 200 + auxy
                if x.get_rect().collidepoint(posicaomouse) and x.get_tipo() != "inicio":
                    x.selecionado = not x.selecionado
                elif x.selecionado and pygame.Rect(x.get_rect().x, x.get_rect().y - escalarY(75), escalarX(tamx), escalarY(70)).collidepoint(posicaomouse):
                    pass
                elif x.selecionado and x.get_tipo() == "repetir" and pygame.Rect(x.get_rect().x, x.get_rect().y - escalarY(175), escalarX(300), escalarY(100)).collidepoint(posicaomouse):
                    pass
                # :
                elif x.selecionado and x.get_tipo() == "blocoF" and (self.tela.jogoPane.boxFuncao.collidepoint(posicaomouse) or self.segurandoBloco):
                    pass
                else:
                    if self.blOpcaoTrue == x:
                        self.tela.jogoPane.mostrarEditBlCor = self.tela.jogoPane.funcaoOpcaoAtiva = self.tela.jogoPane.mostrarEditBlRepetir = False
                        self.blOpcaoTrue = None
                    x.selecionado = False
                i += 1
        else:
            for x in self.comando:
                x.selecionado = False

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
            self.tela.jogoPane.finalizacriacao = False
            self.tela.telaInicio = True
        elif self.tela.botaoProximo.colisao_point(posicaomouse) and not self.botaoclicado:
            self.tela.jogoPane.modoCriar()
            self.fase = Fase()
            self.fase.desenhoDesafio = Desenho(
                self.tela.linhas, self.tela.colunas, 0)
            self.fase.tentativas = self.tela.execucoes
            self.tela.telaCriar = False
            self.tela.jogoPane.botaoSalvar.mudarImg("BOTAOPROX.PNG")
            self.tela.telaJogo = True
            self.esperaJogoAparecer = False
        self.botaoclicado = False

    def _VerificarTelaSaves(self, posicaomouse):
        if self.tela.saves is None or len(self.saves) <= 0:
            if self.tela.btConfig.colisao_point(posicaomouse):
                self._velociadeAnterior = Util.Config.VELOCIDADE
                self.tela.telaInicio = self.tela.telaSaves = False
                self.tela.telaConfig = True
        # BOTÃO VOLUME
            elif self.tela.btAjuda.colisao_point(posicaomouse):
                self.tela.indexAjuda = 1
                self.tela.telaInicio = False
                self.tela.telaAjuda = True
            elif self.tela.botaoVolume.colisao_point(posicaomouse):
                if self.volume:
                    self.tela.botaoVolume.mudarImg("BOTAOVOLUMEOFF.PNG")
                    self.volume = False
                else:
                    self.tela.botaoVolume.mudarImg("BOTAOVOLUMEON.PNG")
                    self.volume = True
            ReproduzirSons(self.volume, SONS)
        if self.tela.botaoNovoJogo.colisao_point(posicaomouse):
            if not Util.Config.MOBILE:
                self.tela.textoAlerta = (
                    "Digite Seu Nome: ", "")
                self.tela.caixaTexto.active = True
                self.tela.caixaTexto.selected = True
                self.tela.desenhaNovoJogo = True
                self.pressNovojogo = True
            else:
                self.gerarNovoJogo()
            self.tela.botaoPlay.append(Sprite("BOTAOPLAY.PNG", 1, 2))
            self.tela.botaolixeira.append(Sprite("lixeira.png", 1, 2))

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
                    gerarFases(self.fases, getTutorials())
                    self.tam = 0
                    self.limparFnComando()
                    self.tela.telaSaves = False
                    self.jogador = self.saves[i]
                    self.pincel.posicaoInicial()
                    # self.fase = self.fases[self.jogador.getNivel()]
                    self.tela.telaSaves = False
                    self.tela.nivelJogador = int(
                        self.jogador.getNivel())
                    self.tela.telaMenuFases = True

    def atualizarListaBlMover(self, blocos, fase=False):
        for bl in blocos:
            if bl.get_tipo() == "mover":
                rotacao = self.pincel.rotacao
                for x in self.comando:
                    if x == bl and not fase:
                        break
                    if x.blocos is not None:
                        if False:  # x.get_Valor() is not None:
                            vl = x.get_Valor()
                        else:
                            vl = 1
                        for i in x.blocos:
                            if rotacao < 0:
                                rotacao += 360
                            if rotacao >= 360:
                                rotacao -= 360
                            if i.get_tipo() == "girar_esquerda":
                                rotacao += 90*vl
                            elif i.get_tipo() == "girar_direita":
                                rotacao -= 90*vl

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
                        self.tela.jogoPane.textoaviso = "AÇÃO INVÁLIDA!", "Você não adicionar janelas na posição inicial!"
                        self.tela.jogoPane.exibeAviso = True
                    elif not (self.tela.jogoPane.finalizacriacao and desenho.tiles[i][j] == -1):
                        desenho.tiles[i][j] = self.pinceledicao
                    else:
                        self.sons.ALERT.play(2)
                        self.tela.jogoPane.textoaviso = "AÇÃO INVÁLIDA!", "Você não pode remover janelas do desenho inicial!"
                        self.tela.jogoPane.exibeAviso = True

    def _VerificarTelaInicio(self, posicaomouse):
        if self.tela.btConfig.colisao_point(posicaomouse):
            self._velociadeAnterior = Util.Config.VELOCIDADE
            self.tela.telaInicio = False
            self.tela.telaConfig = True
        # BOTÃO VOLUME
        elif self.tela.btAjuda.colisao_point(posicaomouse):
            self.tela.indexAjuda = 1
            self.tela.telaInicio = False
            self.tela.telaAjuda = True
        elif self.tela.botaoVolume.colisao_point(posicaomouse):
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
                    self.atualizarListaBlMover(
                        self.fase.blocosdisponiveis, True)
                    self.tam = 0
                    self.jogandoFasePersonalizada = True
                    self.jogador = None
                    self.tela.telaFases = False
                    self.tela.telaJogo = True
                    self.esperaJogoAparecer = False
                    break

    def carregarConfig(self):
        if Util.lerConfig():
            self.tela.sliderVl.value = Util.Config.VELOCIDADE
            self.tela.telaConfig = False
            self.tela.telaInicio = True

    def verificardesenho(self):
        if self.verificandodesenho:
            if self.i < self.fase.desenhoDesafio.colunas:
                self.tela.jogoPane.desenharVerificacao(self.i, self.j)
            if True:  # self.espera > 2:
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
