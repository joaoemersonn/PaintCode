

class Desenho:
    def __init__(self, linhas, colunas, tintapadrao=0):
        self.tiles = [[i for i in range(linhas)] for j in range(colunas)]
        self.linhas = linhas
        self.colunas = colunas
        for i in range(0, colunas):
            for j in range(0, linhas):
                self.tiles[i][j] = tintapadrao
