import os
from pathlib import Path
import pygame
from pygame import mixer
from pygame_widgets.button import Button
from model.Desenho import Desenho
from model.Jogador import Jogador
from model.Fase import Fase
import platform
SISTEMA = platform.system()
WINDOW = pygame.display.set_mode((0, 0),
                                 flags=pygame.FULLSCREEN)
CARREGANDO = True
STATUSCARREGAMENTO = 0
ESCALAX = WINDOW.get_width()/1366
ESCALAY = WINDOW.get_height()/768
mixer.init()


def centerH(largura, tamH):
    return ((largura/2)-tamH)


def animarLoad():
    global STATUSCARREGAMENTO
    if CARREGANDO:
        pygame.draw.rect(WINDOW, Cores.CORSECUNDARIA,
                         (int(338*ESCALAX), int(645*ESCALAY), int(800*ESCALAX), int(40*ESCALAY)))
        pygame.draw.rect(WINDOW, Cores.CORPRINCIPAL,
                         (int(343*ESCALAX), int(650*ESCALAY), int(ESCALAX*7*STATUSCARREGAMENTO), int(30*ESCALAY)))
        pygame.display.update()
        STATUSCARREGAMENTO += 1
        # print(STATUSCARREGAMENTO)
       # for x in range(0, 25):
        #    GIF.render(WINDOW, (850, 350))
        #    pygame.display.update()


def get_cor(valor):
    if valor == 1:
        return Cores.CORPRINCIPAL
    elif valor == 2:
        return Cores.VERDE
    elif valor == 3:
        return Cores.AMARELO
    elif valor == 4:
        return Cores.VERMELHO
    else:
        return Cores.BRANCO


class Config:
    VELOCIDADE = 60
    TELACHEIA = True
    MOBILE = False


def criarBotaoFase(janela, x, y, texto):
    bt = Button(
        janela, int(x*ESCALAX), int(y*ESCALAY), int(100*ESCALAX), int(140*ESCALAY), text=texto,
        fontSize=50, margin=20,
        inactiveColour=(0, 205, 255),
        hoverColour=(0, 0, 255), radius=20,
    )
    return bt


def gerarBotaoFase(janela, t=15):
    l = list()
    y = 1
    x = 0
    for i in range(0, t):
        if i >= (y*5):
            y += 1
            x = 0
        l.append(criarBotaoFase(
            janela, (200+(200*(x))), 150+((y-1)*150), str(i+1)))
        x += 1
    return l


class Cores:
    BRANCO = pygame.Color("#FFFFFF")
    CORFUNDO = pygame.Color("#F2EFEA")
    VERDE = pygame.Color("#5EEB5B")
    AMARELO = pygame.Color("#e3ba02")
    CORPRINCIPAL = pygame.Color(0, 205, 255)
    CORSECUNDARIA = pygame.Color(153, 153, 153)
    PRETO = pygame.Color("#000000")
    TELHADO = pygame.Color("#C4875E")
    CORELEMENTO = pygame.Color(2, 60, 64, 100)
    VERMELHO = pygame.Color("#DD1C1A")
    ROXO = pygame.Color(255, 117, 249, 100)
    LARANJA = pygame.Color(255, 250, 200)
    LARANJAESCURO = pygame.Color(255, 176, 32)
    ROXOESCURO = pygame.Color(207, 101, 199, 100)
    TRANSPARENT = pygame.Color(0, 0, 0, a=180)


def get_path_projeto():
    return os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace("controller", "").replace("util",
                                                                                                                                 "")


def ler_saves():
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    print("Diretorio ler saves: ", diretorio)
    texopath = os.path.join(diretorio, "saves.saves")
    arquivo = open(texopath, 'r')
    saves = list()
    for linha in arquivo:
        linha = linha.rstrip()
        j = linha.split("$")
        saves.append(Jogador(j[0], int(j[1])))
    arquivo.close()
    return saves


def gravar_saves(saves):
    animarLoad()
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    print("Diretorio gravar saves: ", diretorio)
    texopath = os.path.join(diretorio, "saves.saves")
    arquivo = open(texopath, 'w')
    for j in saves:
        arquivo.write(str(j.getNome()) + "$" + str(j.getNivel()) + "\n")
    arquivo.close()


# FALTA TERMINAR
def ler_fases():
    animarLoad()
    fasesCriadas = list()
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    print("Diretorio ler fases: ", diretorio)
    # diretorio = os.path.join(Path.home(), ".PaintCode")
    diretorio = os.path.join(diretorio, "fasescriadas")
    # arquivo = open(diretorio, 'r')
    arquivos = os.listdir(diretorio)
    for arqName in arquivos:
        if arqName.__contains__(".level"):
            fase = Fase()
            textopath = os.path.join(diretorio, arqName)
            arquivo = open(textopath, 'r')
            tentativas = arquivo.readline()
            tentativas = tentativas.strip().replace("@", "")
            fase.tentativas = int(tentativas)
            cores = arquivo.readline().strip().split("$")
            cores.remove("")
            for cor in cores:
                fase.coresdisponiveis.append(int(cor))
            stringDesenhoDesafio = arquivo.readline().strip()
            fase.desenhoDesafio = get_desenho_string(stringDesenhoDesafio)
            stringDesenhoResposta = arquivo.readline().strip()
            fase.desenhoResposta = get_desenho_string(stringDesenhoResposta)
            fase.gerartodosblocosCores()
            fasesCriadas.append(fase)
            arquivo.close()
    if fasesCriadas.__len__() <= 0:
        fasesCriadas = None
    return fasesCriadas


def get_desenho_string(stringDesenho):
    colunas = stringDesenho.split("@")
    colunas.remove("")
    desenhodesafio = None
    for i in range(0, len(colunas)):
        linhas = colunas[i].strip().split(",")
        linhas.remove("")
        for j in range(0, len(linhas)):
            if desenhodesafio is None:
                desenhodesafio = Desenho(len(linhas), len(colunas))
            desenhodesafio.tiles[i][j] = linhas[j]
    return desenhodesafio


def gravar_fase(fase):
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    print("Diretorio gravar fase: ", diretorio)
    # diretorio = os.path.join(Path.home(), ".PaintCode")
    diretorio = os.path.join(diretorio, "fasescriadas")
    arquivos = os.listdir(diretorio)
    texopath = os.path.join(diretorio, str(len(arquivos)) + ".level")
    arquivo = open(texopath, 'w')
    arquivo.write("@" + str(fase.tentativas) + "\n")
    for j in fase.coresdisponiveis:
        arquivo.write(str(j) + "$")
    arquivo.write("\n")
    for i in range(0, fase.desenhoDesafio.colunas):
        arquivo.write("@")
        for j in range(0, fase.desenhoDesafio.linhas):
            arquivo.write(str(fase.desenhoDesafio.tiles[i][j]) + ",")
    arquivo.write("\n")
    for i in range(0, fase.desenhoResposta.colunas):
        arquivo.write("@")
        for j in range(0, fase.desenhoResposta.linhas):
            arquivo.write(str(fase.desenhoResposta.tiles[i][j]) + ",")
    arquivo.close()


def lerConfig():
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    path = os.path.join(diretorio, "config.cfg")
    if not os.path.isfile(path):
        return False
    else:
        arquivo = open(os.path.join(diretorio, "config.cfg"), 'r')

        for linha in arquivo:
            linha = linha.rstrip()
            cfg = linha.split("$")
            Config.VELOCIDADE = int(cfg[1])
        arquivo.close()
        return True


def gravarConfig(velocidade=80):
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    arquivo = open(os.path.join(diretorio, "config.cfg"), 'w')
    arquivo.write(str("VELOCIDADE") + "$" + str(velocidade) + "\n")
    arquivo.close()


def criarPastas():
    animarLoad()
    if SISTEMA == "Windows":
        diretorio = os.path.join(Path.home(), ".PaintCode")
    else:
        diretorio = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "").replace(
            "controller",
            "").replace("util",
                        "").replace("lib",
                                    "")
        diretorio = os.path.join(diretorio, ".PaintCode")
    # diretorio = os.path.join(Path.home(), ".PaintCode")
    print("Diretorio criado: ", diretorio)
    if not os.path.isdir(diretorio):
        os.mkdir(diretorio)
        os.mkdir(os.path.join(diretorio, "fasescriadas"))
        arquivo = open(os.path.join(diretorio, "saves.saves"), 'w')
        arquivo.close()


def carregar_som(nome):
    animarLoad()
    diretorio = get_path_projeto()
    diretorio = os.path.join(diretorio, 'lib')
    diretorio = os.path.join(diretorio, 'sons')
    sompath = os.path.join(diretorio, nome)
    print("tentando carregar Som: ", sompath)
    som = mixer.Sound(sompath)
    return som


def carrega_imagem(imagem_nome, subdir="", escala=1):
    animarLoad()
    diretorio = get_path_projeto()
    diretorio = os.path.join(diretorio, "lib")
    diretorio = os.path.join(diretorio, "imagens")
    diretorio = os.path.join(diretorio, subdir)
    iagempath = os.path.join(diretorio, imagem_nome)
    print("carregando Imagem:", iagempath)
    try:
        image = pygame.image.load(iagempath)
        if escala > 1 or (ESCALAX != 1 and imagem_nome != "confete.png" and imagem_nome != "confete2.png"):
            img1 = image
            image = pygame.transform.smoothscale(
                img1.convert_alpha(), (int((img1.get_rect().w / escala) * ESCALAX), int((img1.get_rect().h / escala) * ESCALAY)))
    except pygame.error:
        print("Não foi possivel carregar Imagem:", iagempath)
        raise SystemExit
    return image


class ImgBlocos:
    def __init__(self):
        self.bl01 = None
        self.bl02 = None
        self.bl03 = None
        self.baixo = None
        self.cima = None
        self.direita = None
        self.esquerda = None
        self.girar_direita = None
        self.girar_esquerda = None
        self.inicio = None
        self.mover = None
        self.repetir = None
        self.selecionar_cor = None
        self.blocoF = None

    def iniciar(self):
        self.bl01 = carrega_imagem('01.png', "blocos")
        self.bl02 = carrega_imagem('02.png', "blocos")
        self.bl03 = carrega_imagem('03.png', "blocos")
        self.baixo = carrega_imagem('baixo.png', "blocos")
        self.cima = carrega_imagem('cima.png', "blocos")
        self.direita = carrega_imagem('direita.png', "blocos")
        self.esquerda = carrega_imagem('esquerda.png', "blocos")
        self.girar_esquerda = carrega_imagem('girar_esquerda.png', "blocos")
        self.girar_direita = carrega_imagem('girar_direita.png', "blocos")
        self.inicio = carrega_imagem('inicio.png', "blocos")
        self.mover = carrega_imagem('mover.png', "blocos")
        self.pintar = carrega_imagem('pintar.png', "blocos")
        self.repetir = carrega_imagem('repetir.png', "blocos")
        self.selecionar_cor = carrega_imagem('selecionar_cor.png', "blocos")
        self.blocoF = carrega_imagem('blocoF.png', "blocos")


IMGBLOCOS = ImgBlocos()


def carregar_imagem_blocos(imagem_nome):
    global IMGBLOCOS
    if IMGBLOCOS.mover is None:
        print("BLOCOS IMG COLETADAS")
        IMGBLOCOS.iniciar()
    if imagem_nome == "mover.png":
        return IMGBLOCOS.mover
    elif imagem_nome == "baixo.png":
        return IMGBLOCOS.baixo
    elif imagem_nome == "cima.png":
        return IMGBLOCOS.cima
    elif imagem_nome == "direita.png":
        return IMGBLOCOS.direita
    elif imagem_nome == "esquerda.png":
        return IMGBLOCOS.esquerda
    elif imagem_nome == "inicio.png":
        return IMGBLOCOS.inicio
    elif imagem_nome == "girar_direita.png":
        return IMGBLOCOS.girar_direita
    elif imagem_nome == "girar_esquerda.png":
        return IMGBLOCOS.girar_esquerda
    elif imagem_nome == "inicio.png":
        return IMGBLOCOS.inicio
    elif imagem_nome == "pintar.png":
        return IMGBLOCOS.pintar
    elif imagem_nome == "selecionar_cor.png":
        return IMGBLOCOS.selecionar_cor
    elif imagem_nome == "blocoF.png":
        return IMGBLOCOS.blocoF
    elif imagem_nome == "repetir.png":
        return IMGBLOCOS.repetir
    elif imagem_nome == "01.png":
        return IMGBLOCOS.bl01
    elif imagem_nome == "02.png":
        return IMGBLOCOS.bl02
    elif imagem_nome == "03.png":
        return IMGBLOCOS.bl03


def ReproduzirSons(somativo, sons):
    if somativo:
        sons.BACKGROUND.set_volume(0.2)
        sons.WIN.set_volume(1)
        sons.LOSE.set_volume(1)
        sons.CLICK.set_volume(1)
        sons.TICK.set_volume(1)
        sons.ALERT.set_volume(1)
        sons.CONFIRMAR.set_volume(0.5)
        sons.NEGAR.set_volume(1)
    else:
        sons.WIN.set_volume(0)
        sons.BACKGROUND.set_volume(0)
        sons.LOSE.set_volume(0)
        sons.CLICK.set_volume(0)
        sons.TICK.set_volume(0)
        sons.ALERT.set_volume(0)
        sons.CONFIRMAR.set_volume(0)
        sons.NEGAR.set_volume(0)


class Sons:
    def __init__(self):
        self.WIN = None
        self.LOSE = None
        self.CLICK = None
        self.TICK = None
        self.ALERT = None
        self.MOVE = None
        self.PAINT = None
        self.COLORCHANGE = None
        self.REINICAR = None
        self.COLOCAR = None
        self.PEGAR = None
        self.DELETE = None
        self.BACKGROUND = None
        self.CONFIRMAR = None
        self.NEGAR = None
        self.MENOS = None

    def iniciar(self):
        self.WIN = carregar_som('win.ogg')
        self.LOSE = carregar_som('lose.ogg')
        self.CLICK = carregar_som('click.ogg')
        self.TICK = carregar_som('tick.ogg')
        self.ALERT = carregar_som('alarm.ogg')
        self.MOVE = carregar_som('move.ogg')
        self.PAINT = carregar_som('paint.ogg')
        self.COLORCHANGE = carregar_som('colorChange.ogg')
        self.REINICAR = carregar_som('reiniciar.ogg')
        self.COLOCAR = carregar_som('colocar.ogg')
        self.PEGAR = carregar_som('pegar.ogg')
        self.DELETE = carregar_som('delete.ogg')
        self.BACKGROUND = carregar_som('back.ogg')
        self.CONFIRMAR = carregar_som('confirmar.ogg')
        self.NEGAR = carregar_som('negar.ogg')
        self.MENOS = carregar_som('menos.ogg')


SONS = Sons()
