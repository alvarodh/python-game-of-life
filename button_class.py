import pygame

class Button:

    def __init__(self, x, y, width, height,
                 text=None,
                 colour=(73,73,73), 
                 highLightedColour=(189,189,189),
                 function=None,
                 params=None,
                 highLighted=False):
    
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.colour = colour
        self.highLightedColour = highLightedColour
        self.highLighted = highLighted
        self.function = function
        self.params = params
        self.width = width
        self.height = height

    def update(self, mouse):
    
        if self.rect.collidepoint(mouse):
            self.highLighted = True
        else:
            self.highLighted = False

    def draw(self, screen):
    
        self.image.fill(self.highLightedColour if self.highLighted else self.colour)
        self.drawText()
        screen.blit(self.image, self.pos)

    def click(self):

        if self.params:
            self.function(self.params)
        else:
            self.function()

    def updateParams(self, params):
    
        self.params = params

    def drawText(self):
    
        font = pygame.font.SysFont('CutiveMono-Regular.ttf', 30)
        text = font.render(self.text, False, (0,0,0))
        width, height = text.get_size()
        x = (self.width - width) / 2
        y = (self.height - height) / 2
        self.image.blit(text, (x, y))
