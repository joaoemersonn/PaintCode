from util.Util import Cores
import pygame
from pygame_widgets import Slider
from pygame_widgets import TextBox
pygame.init()
win = pygame.display.set_mode((1000, 600))

slider = Slider(win, 100, 100, 800, 40, min=20, max=250, step=1)
output = TextBox(win, 475, 200, 50, 50, fontSize=30)
textbox = TextBox(win, 100, 200, 800, 80, fontSize=50,
                  borderColour=Cores.CORPRINCIPAL, textColour=(0, 0, 0),
                  onSubmit=output, radius=10, borderThickness=5)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    slider.listen(events)
    slider.draw()
    textbox.listen(events)
    textbox.draw()

    output.setText(slider.getValue())

    output.draw()

    pygame.display.update()
