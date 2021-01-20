from pygame import image
from pygame_widgets.button import ButtonArray
from util.Util import Cores, carrega_imagem
import pygame
from pygame_widgets import Slider
from pygame_widgets import TextBox, Button
pygame.init()
pygame.mixer.quit()
win = pygame.display.set_mode((1000, 600))

button = Button(
    win, 100, 100, 100, 150, text='1',
    fontSize=50, margin=20,
    inactiveColour=(0, 205, 255),
    hoverColour=(0, 0, 255), radius=20,

    #onClick=lambda: print('Click')
)
button2 = Button(
    win, 230, 100, 100, 150, text='2',
    fontSize=50, margin=20,
    inactiveColour=(153, 153, 153),
    hoverColour=(153, 153, 153), radius=20,
    # image=carrega_imagem("cadeado.png")
    #onClick=lambda: print('Click')
)
buttonArray = ButtonArray(win, 50, 50, 900, 800, (5, 3),
                          inactiveColour=(0, 205, 255),
                          hoverColour=(0, 0, 255), radius=20,
                          border=100, texts=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15')
                          )
button2.setImage(carrega_imagem("cadeado.png"))
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

    # slider.listen(events)
    # slider.draw()
    # textbox.listen(events)
    # textbox.draw()

    # output.setText(slider.getValue())

    # output.draw()
    # button.listen(events)
    # button2.listen(events)
    # button.draw()
    # button2.draw()
    buttonArray.listen(events)
    buttonArray.draw()
    pygame.display.update()
