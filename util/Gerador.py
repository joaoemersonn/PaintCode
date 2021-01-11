from model.Bloco import Bloco
from model.Desenho import Desenho
from model.Fase import Fase
from util.Util import carrega_imagem


def gerarFases(listaFases):
    l = listaFases
    tf = carrega_imagem("tf.png")
    l.clear()

    # fase 1
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    # fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    # fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.tutorial = list()
    fase.tutorial.append(carrega_imagem("t1.png"))
    fase.tutorial.append(carrega_imagem("t2.png"))
    fase.tutorial.append(carrega_imagem("t3.png"))
    fase.tutorial.append(carrega_imagem("t3.2.png"))
    fase.tutorial.append(tf)
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
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    fase.tutorial = list()
    fase.tutorial.append(carrega_imagem("t4.png"))
    fase.tutorial.append(carrega_imagem("t5.png"))
    fase.tutorial.append(carrega_imagem("t6.png"))
    fase.tutorial.append(tf)

    fase.desenhoDesafio.tiles[2][2] = 0

    fase.desenhoDesafio.tiles[2][1] = -1
    fase.desenhoResposta.tiles[2][1] = -1
    fase.tentativas = 2
    fase.nivel = 2
    l.append(fase)

    #######################################################################
    # fase 3
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    fase.desenhoDesafio.tiles[2][2] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 3
    fase.nivel = 3
    l.append(fase)
    #######################################################################
    # fase 4
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        fase.desenhoDesafio.tiles[i][0] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 1
    fase.nivel = 4
    l.append(fase)
    #######################################################################
    # fase 5
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.tutorial = list()
    fase.tutorial.append(carrega_imagem("t7.png"))
    fase.tutorial.append(tf)
    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        for j in range(0, 2):
            fase.desenhoDesafio.tiles[i][j] = 0

    fase.desenhoDesafio.tiles[0][2] = -1
    fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 3
    fase.nivel = 5
    l.append(fase)
    #######################################################################
    # fase 6
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.tutorial = list()
    fase.tutorial.append(carrega_imagem("t8.png"))
    fase.tutorial.append(carrega_imagem("t9.png"))
    fase.tutorial.append(carrega_imagem("t10.png"))
    fase.tutorial.append(tf)
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
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))

    fase.desenhoDesafio = Desenho(4, 5, 0)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(1, 4):
        for j in range(1, 3):
            fase.desenhoDesafio.tiles[i][j] = 1

    # fase.desenhoDesafio.tiles[0][2] = -1
    # fase.desenhoResposta.tiles[0][2] = -1
    fase.tentativas = 2
    fase.nivel = 7
    l.append(fase)
    #######################################################################
    # fase 8
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)
    fase.tutorial = list()
    fase.tutorial.append(carrega_imagem("t11.png"))
    fase.tutorial.append(carrega_imagem("t12.png"))
    fase.tutorial.append(tf)
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
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(4, 5, 1)
    fase.desenhoResposta = Desenho(4, 5, 1)

    for i in range(0, 5):
        fase.desenhoResposta.tiles[i][0] = 2
        fase.desenhoResposta.tiles[i][2] = 2

    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoResposta.tiles[2][3] = -1
    fase.tentativas = 1
    fase.nivel = 9
    l.append(fase)
    #######################################################################
    # fase 10
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
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
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
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
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 6, 0)
    fase.desenhoResposta = Desenho(5, 6, 1)

    fase.desenhoDesafio.tiles[5][4] = -1
    fase.desenhoResposta.tiles[5][4] = -1
    fase.tentativas = 4
    fase.nivel = 12
    l.append(fase)
    #######################################################################
    # fase 13
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 6, 0)
    fase.desenhoResposta = Desenho(5, 6, 1)

    for i in range(0, 6):
        fase.desenhoResposta.tiles[i][2] = 2

    fase.desenhoDesafio.tiles[5][4] = -1
    fase.desenhoResposta.tiles[5][4] = -1
    fase.tentativas = 4
    fase.nivel = 13
    l.append(fase)
    #######################################################################
    # fase 14
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 6, 0)
    fase.desenhoResposta = Desenho(5, 6, 1)

    fase.desenhoDesafio.tiles[3][3] = -1
    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoDesafio.tiles[3][2] = -1
    fase.desenhoDesafio.tiles[2][2] = -1
    fase.desenhoResposta.tiles[3][3] = -1
    fase.desenhoResposta.tiles[2][3] = -1
    fase.desenhoResposta.tiles[3][2] = -1
    fase.desenhoResposta.tiles[2][2] = -1

    fase.tentativas = 5
    fase.nivel = 14
    l.append(fase)
    #######################################################################
    # fase 15
    fase = Fase()
    fase.blocosdisponiveis.append(Bloco("mover"))
    fase.blocosdisponiveis.append(Bloco("girar_esquerda"))
    fase.blocosdisponiveis.append(Bloco("girar_direita"))
    fase.blocosdisponiveis.append(Bloco("pintar"))
    fase.blocosdisponiveis.append(Bloco("repetir"))
    fase.blocosdisponiveis.append(Bloco("selecionar_cor"))
    fase.coresdisponiveis.append(0)
    fase.coresdisponiveis.append(1)
    fase.coresdisponiveis.append(2)
    fase.coresdisponiveis.append(3)

    fase.desenhoDesafio = Desenho(5, 6, 0)
    fase.desenhoResposta = Desenho(5, 6, 1)

    for i in range(0, 6):
        fase.desenhoResposta.tiles[i][2] = 2

    fase.desenhoDesafio.tiles[3][3] = -1
    fase.desenhoDesafio.tiles[2][3] = -1
    fase.desenhoDesafio.tiles[3][2] = -1
    fase.desenhoDesafio.tiles[2][2] = -1
    fase.desenhoResposta.tiles[3][3] = -1
    fase.desenhoResposta.tiles[2][3] = -1
    fase.desenhoResposta.tiles[3][2] = -1
    fase.desenhoResposta.tiles[2][2] = -1

    fase.tentativas = 5
    fase.nivel = 15
    l.append(fase)

    return l
