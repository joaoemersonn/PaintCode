import pygame
import os

from util import Util
from util.Util import Cores, get_cor
from view.Painel import Painel
from model.Sprite import Sprite
from model.TextInput import InputBox
from view.PainelJogo import PainelJogo
from util.Util import carrega_imagem
from view.PainelJogo import contornarRect
from view.PainelJogo import contornar


class Tela:
    def __init__(self,window,largura,altura):
        pygame.init()
        fontearquivo = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "")
        fontearquivo = os.path.join(fontearquivo, "lib")
        fontearquivo = os.path.join(fontearquivo, "FreeSansBold.ttf")
        self.fa = fontearquivo
        self.altura = altura
        self.fontetipo = 'comicsansms'
        self.ajuste = 360
        self.largura = largura + self.ajuste
        self.tamanho = (self.largura, self.altura)
        self.janela = window#pygame.display.set_mode(self.tamanho,pygame.SCALED)
        self.__janela = carrega_imagem("janela.png")
        self.__janela2 = pygame.transform.scale(self.__janela, (60, 60))

        #FONTES
        self.fonteGrande = pygame.font.Font(fontearquivo, 30 - 8)
        self.fontePequena = pygame.font.Font(fontearquivo, 20 - 8)
        self.fonteTitulo = pygame.font.Font(fontearquivo, 80 - 25)



        self.corBranca = Cores.BRANCO
        self.corfundo = Cores.CORFUNDO
        self.corPrincipal = Cores.CORPRINCIPAL
        self.corSecundaria = Cores.CORSECUNDARIA
        self.corTexto = Cores.CORSECUNDARIA
        self.cor1Elemento = Cores.CORELEMENTO
        self.telaInicio = True
        self.telaSaves = self.telaJogo = self.telaCriar = self.telaFases = False
        self.rolagem = 0
        pygame.display.set_icon(carrega_imagem("icon.png"))
        pygame.display.set_caption("PaintCoding")
        #pygame.display.set_mode((self.largura, self.altura),pygame.FULLSCREEN)
        self.ok = Sprite("ok.png", 1, 2)
        self.ok.definirPosicao((760, 380))
        self.desenhaAlerta = self.desenhaNovoJogo = False
        self.textoAlerta = ("TEXTO TITULO!", "PRESSIONE OK PARA CONTINUAR!")
        self.caixaTexto = InputBox(100, 30, 550, 300)
        # INICIO
        self.botaostart = Sprite("BOTAOJOGAR.PNG", 1, 2)
        self.botaoCriar = Sprite("BOTAOCRIAR.PNG", 1, 2)
        self.botaoSair = Sprite("BOTAOSAIR.PNG", 1, 2)
        self.botaoVolume = Sprite("BOTAOVOLUMEON.PNG", 1, 2)
        self.img = carrega_imagem("img2.png")
        self.c1 = carrega_imagem("c1.png")
        self.c2 = carrega_imagem("c2.png")
        self.c4 = carrega_imagem("c4.png")
        self.botaostart.definirPosicao((350 + (self.ajuste / 2), 330))
        self.botaoCriar.definirPosicao((350 + (self.ajuste / 2), 450))
        self.botaoSair.definirPosicao((350 + (self.ajuste / 2), 590))
        self.botaoVolume.definirPosicao((930 + self.ajuste, 15))
        # ESCOLHERSAVE
        self.botaoNovoJogo = Sprite("BOTAONOVOJOGO.PNG", 1, 2)
        self.botaoFasesPersonalizadas = Sprite("BOTAOCRIACOES.PNG", 1, 2)
        self.botaoVoltar = Sprite("VOLTAR.png", 1, 2)
        self.botaoCima = Sprite("BOTAOCIMA.png", 1, 2)
        self.botaoBaixo = Sprite("BOTAOBAIXO.png", 1, 2)
        self.botaoNovoJogo.definirPosicao((90 + (self.ajuste / 2), 580))
        self.botaoFasesPersonalizadas.definirPosicao((350 + (self.ajuste / 2), 580))
        self.botaoVoltar.definirPosicao((650 + (self.ajuste / 2), 580))
        self.botaoCima.definirPosicao((860 + (self.ajuste / 2), 54))
        self.botaoBaixo.definirPosicao((860 + (self.ajuste / 2), 480))
        self.savesPane = Painel(943, 493, 25 + (self.ajuste / 2), 70)
        self.moverretangulo = False
        self.botaoPlay = []
        self.botaolixeira = []
        self.saves = None
        #self.fasesPersonalizadas = None

        #CRIAR
        self.colunas = self.linhas = 2
        self.execucoes = 1
        self.btCimaCol = Sprite("BOTAOCIMA.png", 1, 2,2)
        self.btCimaLi = Sprite("BOTAOCIMA.png", 1, 2,2)
        self.btBaixoCol = Sprite("BOTAOBAIXO.png", 1, 2,2)
        self.btBaixoLi = Sprite("BOTAOBAIXO.png", 1, 2,2)
        self.btCimaEx = Sprite("BOTAOCIMA.png", 1, 2,2)
        self.btBaixoEx = Sprite("BOTAOBAIXO.png", 1, 2,2)
        self.btCimaCol.definirPosicao((90,180))
        self.btBaixoCol.definirPosicao((90,250))
        self.btCimaLi.definirPosicao((200, 180))
        self.btBaixoLi.definirPosicao((200, 250))
        self.btCimaEx.definirPosicao((250,380))
        self.btBaixoEx.definirPosicao((250, 450))
        self.botaoProximo = Sprite("BOTAOPROX.PNG", 1, 2)
        self.botaoVoltarCriar = Sprite("VOLTAR.png", 1, 2)
        self.botaoVoltarCriar.definirPosicao((750 + (self.ajuste / 2), 580))
        self.botaoProximo.definirPosicao((500 + (self.ajuste / 2), 580))

        #TELA FASES PERSONALIZADAS
        self.botaoEsquerda = Sprite("BOTAOESQUERDA.png", 1, 2)
        self.botaoDireita = Sprite("BOTAODIREITA.png", 1, 2)
        self.botaoEsquerda.definirPosicao((60, 350))
        self.botaoDireita.definirPosicao((1220, 350))
        self.contornoFase = None
        self.btVoltarFases = Sprite("VOLTAR.png",1,2)
        self.btVoltarFases.definirPosicao((950, 600))
        self.fasespersonalizadas = None
        self.rolagemCriacoes = 0

        # MSG PERRGUNTA
        self.desenhaConfirmacao = False
        self.textopergunta = ("Confirma a exclusão do Progresso?"," Essa ação não poderá ser desfeita!")
        self.confirmarbotao = Sprite("confirmar.png", 1, 2)
        self.cancelarbotao = Sprite("cancelar.png", 1, 2)
        self.confirmarbotao.definirPosicao((850, 390))
        self.cancelarbotao.definirPosicao((695, 390))
        # JOGO
        self.jogoPane = PainelJogo(self, self.largura, self.altura, 0, 0)  # 943, 493, 25, 70)

        # IMAGEM
        self.imagemConteiner = carrega_imagem("conteiner.png")

        # TEXTOS
        self.tituloTelaSave = self.fonteTitulo.render("Jogar", True, self.corPrincipal)
        self.tituloTelaFases = self.fonteTitulo.render("Fases Personalizadas", True, self.corPrincipal)
        self.txt_pane = self.fonteTitulo.render("Selecione as Carateristicas da Fase: ", True, self.corTexto)
        self.txt_desenho = self.fonteGrande.render("Selecione a Quantidade de Linhas e Colunas do Desenho: ", True,
                                              self.corTexto)
        self.txt_col_lin = self.fonteGrande.render("Colunas  x  Linhas: ", True, self.corPrincipal)
        self.txt_X = self.fonteGrande.render("X", True, self.corPrincipal)
        self.txt_qntvidas = self.fonteGrande.render("Selecione a Quantidade de Execuções Disponíveis Para concluir o desenho:", True, self.corTexto)
        self.txt_ex = self.fonteGrande.render("Nº Execuções:", True, self.corPrincipal)

    def desenhar(self):

        if not self.desenhaNovoJogo and not self.desenhaAlerta and not self.desenhaConfirmacao:
            self.janela.fill(self.corBranca)

            # TELA INICIO
            if self.telaInicio:
                # BOTÕES
                self.botaoVolume.desenharBt(self.janela)
                self.janela.blit(self.img, (300, 0))
                self.botaostart.desenharBt(self.janela)
                self.botaoCriar.desenharBt(self.janela)
                self.botaoSair.desenharBt(self.janela)

            # TELA SAVES
            elif self.telaSaves:
                self.savesPane.fill(self.corfundo)
                contornar(self.janela, 25 + (self.ajuste / 2), 70, 943, 493, 4)
                self.janela.blit(self.tituloTelaSave, ((self.largura / 2) - 80, 7))
                self.desenharPainelSaves(self.saves)
                self.janela.blit(self.savesPane, self.savesPane.get_posicao())

                # BOTÕES
                self.botaoNovoJogo.desenharBt(self.janela)
                self.botaoFasesPersonalizadas.desenharBt(self.janela)
                self.botaoVoltar.desenharBt(self.janela)
                self.botaoCima.desenharBt(self.janela)
                self.botaoBaixo.desenharBt(self.janela)

            #TELA FASES PERS
            elif self.telaFases:
                self.janela.blit(self.tituloTelaFases, ((self.largura / 2) - 250, 15))
                self.botaoEsquerda.desenharBt(self.janela)
                self.botaoDireita.desenharBt(self.janela)
                self.desenharDesenhoGuia(self.fasespersonalizadas, self.rolagemCriacoes)
                self.btVoltarFases.desenharBt(self.janela)

        if self.telaJogo:
            self.janela.blit(self.jogoPane, self.jogoPane.get_posicao())

        elif self.telaCriar:
            self.desenharPainelCriar()

        if self.desenhaAlerta:
            self.deesenharAlerta(self.textoAlerta)

        if self.desenhaConfirmacao:
            self.deesenharMsgPergunta(self.textopergunta)

        if self.desenhaNovoJogo:
            self.desenharNovoJogo()

    def desenharPainelCriar(self):
        self.janela.blit(self.txt_pane,(20,50))
        self.janela.blit(self.txt_desenho,(50,130))
        self.janela.blit(self.txt_col_lin, (70, 160))

        self.btBaixoLi.desenharBt(self.janela)
        self.btCimaLi.desenharBt(self.janela)
        self.btCimaCol.desenharBt(self.janela)
        self.btBaixoCol.desenharBt(self.janela)

        self.janela.blit(self.txt_X,(163,230))
        txt_col = self.fonteGrande.render(str(self.colunas), True, self.corTexto)
        txt_li = self.fonteGrande.render(str(self.linhas), True, self.corTexto)
        self.janela.blit(txt_col,(110,230))
        self.janela.blit(txt_li, (220, 230))
        contornar(self.janela,90,225,50,30)
        contornar(self.janela,200,225,50,30)

        self.janela.blit(self.txt_qntvidas,(50, 350))
        self.janela.blit(self.txt_ex,(70, 430))
        self.btCimaEx.desenharBt(self.janela)
        self.btBaixoEx.desenharBt(self.janela)
        txt_execucoes = self.fonteGrande.render(str(self.execucoes), True, self.corTexto)
        self.janela.blit(txt_execucoes,(270, 430))
        contornar(self.janela, 250, 425, 50, 30)
        self.botaoVoltarCriar.desenharBt(self.janela)
        self.botaoProximo.desenharBt(self.janela)

    def desenharPainelSaves(self, jogador):
        espaco = 117
        qntsaves = 0

        text2 = self.fontePequena.render("PROGRESSO: ", True, self.corSecundaria)
        text3 = self.fontePequena.render("Jogar ", True, self.corSecundaria)
        for x in jogador:
            text = self.fonteGrande.render("NOME: " + x.getNome(), True, self.corSecundaria)
            self.savesPane.blit(self.imagemConteiner, (25, (espaco * qntsaves) + 10 + self.rolagem))
            self.savesPane.blit(text, (55, (espaco * qntsaves) + 25 + self.rolagem))
            self.savesPane.blit(text2, (75, (espaco * qntsaves) + 60 + self.rolagem))
            self.savesPane.blit(text3, (710, (espaco * qntsaves) + 90 + self.rolagem))
            pygame.draw.rect(self.savesPane, self.corSecundaria, (75, (espaco * qntsaves) + 75 + self.rolagem, 580, 30))
            pygame.draw.rect(self.savesPane, self.corPrincipal,
                             (75, (espaco * qntsaves) + 75 + self.rolagem, 40 * x.getNivel(), 30))

            self.botaoPlay[qntsaves].definirPosicao((700, (espaco * qntsaves) + 30 + self.rolagem))
            self.botaolixeira[qntsaves].definirPosicao((653, (espaco * qntsaves) + 72 + self.rolagem))

            # BOTAO
            self.botaolixeira[qntsaves].desenharBt(self.savesPane)
            self.botaoPlay[qntsaves].desenharBt(self.savesPane)
            qntsaves += 1

    def deesenharAlerta(self, textolist):
        superfice = self.janela
        texto = textolist[0]
        texto2 = textolist[1]
        rect = pygame.Rect((superfice.get_rect().w / 4), (superfice.get_rect().h / 4), 600, 150)
        font = pygame.font.Font(self.fa, 35 - 12)
        textod = font.render(texto, True, Cores.PRETO)
        textod2 = font.render(texto2, True, Cores.PRETO)
        superfice.blit(self.c4, rect)
        superfice.blit(textod, (rect.x + 80, rect.y + 90))
        superfice.blit(textod2, (rect.x + 80, rect.y + 110))
        if len(textolist) > 2:
            font = pygame.font.Font(self.fa, 20 - 8)
            textod3 = font.render(textolist[2], True, Cores.PRETO)
            superfice.blit(textod3, (rect.x + 100, rect.y + 180))
        self.ok.desenharBt(superfice)

    def desenharNovoJogo(self):
        superfice = self.janela
        rect = pygame.Rect((300, 150, 800, 416))
        font = pygame.font.Font(self.fa, 25)
        font2 = pygame.font.Font(self.fa, 25 - 8)
        novojogo = font.render("Novo Jogo", True, Cores.CORPRINCIPAL)
        textod2 = font2.render("Digite seu Nome:", True, Cores.PRETO)
        superfice.blit(self.c1, rect)
        superfice.blit(novojogo, (rect.x + 350, rect.y + 80))
        superfice.blit(textod2, (rect.x + 100, rect.y + 155))
        self.caixaTexto.update()
        self.caixaTexto.draw(superfice)
        self.confirmarbotao.desenharBt(superfice)
        self.cancelarbotao.desenharBt(superfice)

    def deesenharMsgPergunta(self, texto):
        superfice = self.janela
        rect = pygame.Rect((300, 150, 800, 416))
        font = pygame.font.Font(self.fa, 25)
        font2 = pygame.font.Font(self.fa, 25 - 8)
        textod = font.render(texto[0], True, Cores.PRETO)
        textod2 = font2.render(texto[1], True, Cores.PRETO)
        superfice.blit(self.c2,rect)
        superfice.blit(textod, (rect.x + 90, rect.y + 120))
        superfice.blit(textod2, (rect.x + 90, rect.y + 150))
        self.confirmarbotao.desenharBt(superfice)
        self.cancelarbotao.desenharBt(superfice)

    def desenharDesenhoGuia(self, fases,x=0,y=0, escala=30):
        if fases is not None:
            if escala != self.__janela2.get_rect().h:
                self.__janela2 = pygame.transform.scale(self.__janela, (escala, escala))
            inty = 270 + y
            intx = -60 + x
            espaco = 700
            qntdFase = 0
            for fase in fases:
                desenho = fase.desenhoResposta
                aux = auxX = 0
                if desenho.colunas <= 3: auxX = 60
                if desenho.linhas < 4: aux = 60
                self.contornoFase[qntdFase].definirPosicao((intx+(espaco * qntdFase)+230, inty-20))
                self.contornoFase[qntdFase].desenharBt(self.janela)
                #desenhando Telhado
                pygame.gfxdraw.filled_trigon(self.janela,
                                             int(self.ajuste / 2) + intx+auxX +(espaco * qntdFase) + + 85 + int((escala * desenho.colunas) / 2),
                                             inty+aux + 50,
                                             int(self.ajuste / 2) + intx+auxX +(espaco * qntdFase)+ 80, 85 + inty+aux,
                                             int(self.ajuste / 2) + intx+auxX+(espaco * qntdFase) + 90 + escala * desenho.colunas,
                                             85 + inty+aux, Cores.TELHADO)

                for i in range(0, desenho.colunas):
                    for j in range(0, desenho.linhas):
                        if int(desenho.tiles[i][j]) >= 0:
                            pygame.draw.rect(self.janela, get_cor(int(desenho.tiles[i][j])),
                                             ((self.ajuste / 2) + intx+auxX+(espaco * qntdFase) + 85 + (escala * i), 85 + inty+aux + (escala * j),
                                              escala, escala))
                        else:
                            self.janela.blit(self.__janela2,
                                      ((self.ajuste / 2) + intx+auxX+(espaco * qntdFase) + 85 + (escala * i), 85 + inty +aux+ (escala * j), escala,
                                       escala))
                contornar(self.janela, (self.ajuste / 2) + intx+auxX+(espaco * qntdFase) + 85, inty+aux + 85, escala * desenho.colunas,
                          escala * desenho.linhas)
                qntdFase += 1

    def carregarContornos(self):
        self.contornoFase = list()
        for fase in self.fasespersonalizadas:
            self.contornoFase.append(Sprite("contorno4.png", 1, 2))
