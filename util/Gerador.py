from model.Bloco import Bloco
from model.Desenho import Desenho
from model.Fase import Fase
from util.Util import carrega_imagem

tutoriais = None
blocos = None


class Blocos():
    def __init__(self):
        self.mover = self.pintar = self.baixo = self.cima = self.direita = self.esquerda = self.girar_esquerda = self.girar_direita = self.repetir = self.mudarCor = None
        self.inicializar()

    def inicializar(self):
        self.mover = Bloco("mover")
        self.pintar = Bloco("pintar")
        self.girar_esquerda = Bloco("girar_esquerda")
        self.girar_direita = Bloco("girar_direita")
        self.repetir = Bloco("repetir")
        self.mudarCor = Bloco("selecionar_cor")
        self.blocoF = Bloco("blocoF")
        self.baixo = Bloco("baixo")
        self.cima = Bloco("cima")
        self.direita = Bloco("direita")
        self.esquerda = Bloco("esquerda")


def getTutorials():
    global tutoriais
    if tutoriais is None:
        tutoriais = list()
        t1 = carrega_imagem("t1.png")
        t2 = carrega_imagem("t2.png")
        t3 = carrega_imagem("t3.png")
        t32 = carrega_imagem("t3.2.png")
        tf = carrega_imagem("tf.png")
        tutoriais.append(tf)
        tutoriais.append(t1)
        tutoriais.append(t2)
        tutoriais.append(t3)
        tutoriais.append(t32)
        tutoriais.append(carrega_imagem("t4.png"))
        tutoriais.append(carrega_imagem("t5.png"))
        tutoriais.append(carrega_imagem("t6.png"))
        tutoriais.append(carrega_imagem("t7.png"))
        tutoriais.append(carrega_imagem("t8.png"))
        tutoriais.append(carrega_imagem("t9.png"))
        tutoriais.append(carrega_imagem("t10.png"))
        tutoriais.append(carrega_imagem("t11.png"))
        tutoriais.append(carrega_imagem("t12.png"))
        tutoriais.append(carrega_imagem("t13.png"))
        tutoriais.append(carrega_imagem("t14.png"))
        tutoriais.append(carrega_imagem("t16.png"))
        tutoriais.append(carrega_imagem("t17.png"))
    return tutoriais


def gerarFases(listaFases, t):
    l = listaFases
    global blocos
    if blocos is None:
        blocos = Blocos()
    l.clear()
    tutoriais = list()

    # fase 1
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.tutorial = list()
    fase.tutorial.append(t[1])
    fase.tutorial.append(t[2])
    fase.tutorial.append(t[3])
    fase.tutorial.append(t[4])
    fase.tutorial.append(t[0])
    fase.desenhoDesafio.tiles[0][2] = 0
    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoResposta = Desenho(4, 5, 1)
    fase.desenhoResposta.tiles[2][3] = -1
    fase.tentativas = 1
    fase.nivel = 1
    l.append(fase)
    #######################################################################
    # fase 2
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    fase.tutorial = list()
    fase.tutorial.append(t[5])
    fase.tutorial.append(t[6])
    fase.tutorial.append(t[7])
    fase.tutorial.append(t[0])

    fase.desenhoDesafio.tiles[2][2] = 0

    fase.desenhoDesafio.tiles[2][1] = -1
    fase.desenhoResposta.tiles[2][1] = -1
    fase.tentativas = 1
    fase.nivel = 2
    l.append(fase)

    #######################################################################
    # fase 3
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    fase.desenhoDesafio.tiles[2][2] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 1
    fase.nivel = 3
    l.append(fase)
    #######################################################################
    # fase 4
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.tutorial = list()
    # fase.tutorial.append(t[8])
    # fase.tutorial.append(t[0])
    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)
    fase.desenhoDesafio.tiles[0][3] = 0
    # for i in range(0, 5):
    #     for j in range(0, 2):
    #         fase.desenhoDesafio.tiles[i][j] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 1
    fase.nivel = 4
    l.append(fase)

    #######################################################################
    # fase 5
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        fase.desenhoDesafio.tiles[i][0] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 1
    fase.nivel = 5
    l.append(fase)
    #######################################################################
    # fase 6
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.tutorial = list()
    fase.tutorial.append(t[9])
    fase.tutorial.append(t[10])
    fase.tutorial.append(t[11])
    fase.tutorial.append(t[0])
    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        for j in range(0, 2):
            fase.desenhoDesafio.tiles[i][j] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 1
    fase.nivel = 6
    l.append(fase)
    #######################################################################
    # fase 7
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)

    fase.desenhoDesafio = Desenho(4, 5, 0)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(1, 4):
        for j in range(0, 3):
            fase.desenhoDesafio.tiles[i][j] = 1

    # fase.desenhoResposta.tiles[0][2] = -1
    fase.desenhoDesafio.tiles[0][0] = 1
    fase.desenhoDesafio.tiles[4][0] = 1
    fase.tentativas = 1
    fase.nivel = 7
    l.append(fase)
    #######################################################################
    # fase 8
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)
    fase.tutorial = list()
    fase.tutorial.append(t[12])
    fase.tutorial.append(t[13])
    fase.tutorial.append(t[0])
    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        fase.desenhoDesafio.tiles[i][0] = 0

    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][0] = 2

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 1
    fase.nivel = 8
    l.append(fase)
    #######################################################################
    # fase 9
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    # fase.blocosdisponiveis.append(blocos.blocoF)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][0] = 3
        fase.desenhoResposta.tiles[i][2] = 3

    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoResposta.tiles[2][3] = -1
    fase.tentativas = 1
    fase.nivel = 9
    l.append(fase)
    #######################################################################
    # fase 10
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 5, 1)
    fase.desenhoResposta = Desenho(5, 5, 1)

    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][i] = 2
    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][4 - i] = 2
        fase.desenhoDesafio.tiles[i][4 - i] = 2

    fase.tentativas = 1
    fase.nivel = 10
    l.append(fase)
    #######################################################################
    # fase 11
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 5, 1)
    fase.desenhoResposta = Desenho(5, 5, 1)

    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][i] = 2
    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][4 - i] = 2
        fase.desenhoDesafio.tiles[i][4 - i] = 2

    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoResposta.tiles[2][3] = -1
    fase.tentativas = 1
    fase.nivel = 11
    l.append(fase)
    #######################################################################
    # fase 12
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.cima)
    fase.blocosdisponiveis.append(blocos.esquerda)
    fase.blocosdisponiveis.append(blocos.direita)
    fase.blocosdisponiveis.append(blocos.baixo)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.tutorial = list()
    fase.tutorial.append(t[16])
    fase.tutorial.append(t[17])
    fase.tutorial.append(t[0])

    fase.desenhoDesafio = Desenho(3, 3, 1)
    fase.desenhoResposta = Desenho(3, 3, 1)

    fase.desenhoDesafio.tiles[1][1] = 0
    fase.desenhoDesafio.tiles[2][2] = 0
    #fase.desenhoResposta.tiles[5][4] = -1
    fase.tentativas = 1
    fase.nivel = 12
    l.append(fase)
    #######################################################################
    # fase 13
    fase = Fase()
    # fase.blocosdisponiveis.append(blocos.mover)
    fase.blocosdisponiveis.append(blocos.cima)
    fase.blocosdisponiveis.append(blocos.esquerda)
    fase.blocosdisponiveis.append(blocos.direita)
    fase.blocosdisponiveis.append(blocos.baixo)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.blocosdisponiveis.append(blocos.blocoF)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.tutorial = list()
    fase.tutorial.append(t[14])
    fase.tutorial.append(t[15])
    fase.tutorial.append(t[0])

    fase.desenhoDesafio = Desenho(5, 6, 1)
    fase.desenhoResposta = Desenho(5, 6, 1)

    for i in range(0, 6):
        fase.desenhoResposta.tiles[i][0] = 2
        #fase.desenhoResposta.tiles[i][4] = 2
       # fase.desenhoResposta.tiles[0][i] = 2
    fase.desenhoResposta.tiles[5][4] = 2
    # fase.desenhoResposta.tiles[0][2] = 2
    # fase.desenhoResposta.tiles[0][3] = 2
    fase.desenhoResposta.tiles[5][1] = 2
    fase.desenhoResposta.tiles[5][2] = 2
    fase.desenhoResposta.tiles[5][3] = 2
    fase.desenhoDesafio.tiles[3][3] = -1
    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoDesafio.tiles[3][2] = -1
    fase.desenhoDesafio.tiles[2][2] = -1
    fase.desenhoResposta.tiles[3][3] = -1
    fase.desenhoResposta.tiles[2][3] = -1
    fase.desenhoResposta.tiles[3][2] = -1
    fase.desenhoResposta.tiles[2][2] = -1

    fase.tentativas = 1
    fase.nivel = 13
    l.append(fase)
    #######################################################################
    # fase 14
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.cima)
    fase.blocosdisponiveis.append(blocos.esquerda)
    fase.blocosdisponiveis.append(blocos.direita)
    fase.blocosdisponiveis.append(blocos.baixo)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.blocosdisponiveis.append(blocos.blocoF)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 6, 1)
    fase.desenhoResposta = Desenho(5, 6, 1)

    for i in range(0, 6):
        fase.desenhoResposta.tiles[i][0] = 2
    for i in range(0, 5):
        fase.desenhoResposta.tiles[5][i] = 2

    fase.desenhoDesafio.tiles[5][4] = -1
    fase.desenhoResposta.tiles[5][4] = -1
    fase.desenhoResposta.tiles[4][4] = 2
    fase.tentativas = 1
    fase.nivel = 14
    l.append(fase)

    #######################################################################
    # fase 15
    fase = Fase()
    fase.blocosdisponiveis.append(blocos.cima)
    fase.blocosdisponiveis.append(blocos.esquerda)
    fase.blocosdisponiveis.append(blocos.direita)
    fase.blocosdisponiveis.append(blocos.baixo)
    fase.blocosdisponiveis.append(blocos.girar_esquerda)
    fase.blocosdisponiveis.append(blocos.girar_direita)
    fase.blocosdisponiveis.append(blocos.pintar)
    fase.blocosdisponiveis.append(blocos.repetir)
    fase.blocosdisponiveis.append(blocos.mudarCor)
    fase.blocosdisponiveis.append(blocos.blocoF)
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 6, 1)
    fase.desenhoResposta = Desenho(5, 6, 1)

    fase.desenhoDesafio.tiles[3][3] = -1
    fase.desenhoResposta.tiles[3][3] = -1
    for i in range(0, 6):
        fase.desenhoResposta.tiles[i][1] = 2
        fase.desenhoResposta.tiles[i][4] = 2
    fase.desenhoResposta.tiles[5][2] = 3
    fase.desenhoResposta.tiles[5][3] = 3

    fase.tentativas = 1
    fase.nivel = 15
    l.append(fase)

    return l
