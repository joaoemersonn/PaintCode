class Fase:

    def __init__(self):
        self.blocosdisponiveis = list()
        self.coresdisponiveis = list()
        self.desenhoDesafio = None
        self.desenhoResposta = None
        self.nivel = 0
        self.tentativas = 0

    def gerartodosblocosCores(self):
        from model.Bloco import Bloco
        self.blocosdisponiveis.append(Bloco("mover"))
        self.blocosdisponiveis.append(Bloco("girar_esquerda"))
        self.blocosdisponiveis.append(Bloco("girar_direita"))
        self.blocosdisponiveis.append(Bloco("pintar"))
        self.blocosdisponiveis.append(Bloco("selecionar_cor"))
        self.blocosdisponiveis.append(Bloco("repetir"))
        self.coresdisponiveis.append(0)
        self.coresdisponiveis.append(1)
        self.coresdisponiveis.append(2)
        self.coresdisponiveis.append(3)
