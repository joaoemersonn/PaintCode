import pygame
import os
from util.Util import Cores


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(w, h, x, y)
        self.color = Cores.PRETO
        self.text = text
        fontearquivo = os.path.dirname(os.path.abspath(__file__)).replace("view", "").replace("model", "")
        fontearquivo = os.path.join(fontearquivo, "lib")
        fontearquivo = os.path.join(fontearquivo, "FreeSansBold.ttf")
        print("Tentando Carregar fonte: ",fontearquivo)
        self.font = pygame.font.Font(fontearquivo, (32-8))
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_DOLLAR:
                    print("Caractere Reservado!")
                else:
                    if not (event.key == pygame.K_DOLLAR):
                        self.text += event.unicode
                    else:
                        print("Caractere Reservado!")
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        # Blit the rect.
        pygame.gfxdraw.box(screen, self.rect, Cores.BRANCO)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
