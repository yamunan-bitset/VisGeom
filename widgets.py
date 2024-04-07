import pygame


class Button:
    def __init__(self, surface, colour, hover_colour, click_colour, font, text, text_colour, x, y, width, height):
        self.surface = surface
        self.colour = colour
        self.hover_colour = hover_colour
        self.click_colour = click_colour
        self.render_colour = colour
        self.render_buff = colour
        self.font = font
        self.text = text
        self.text_colour = text_colour
        self.rect = pygame.Rect(x, y, width, height)

        self.clicked = False

    def handle_event(self, event, mousepos):
        if 0 < mousepos[0] - self.rect.x < self.rect.width and 0 < mousepos[1] - self.rect.y < self.rect.height:
            self.render_colour = self.hover_colour
        else:
            self.render_colour = self.colour
        if event.type == pygame.MOUSEBUTTONUP:
            if 0 < mousepos[0] - self.rect.x < self.rect.width and 0 < mousepos[1] - self.rect.y < self.rect.height:
                self.clicked = True
                return True

        #self.clicked = False
        return False

    def render(self):
        if self.clicked:
            self.render_colour = self.click_colour

        pygame.draw.rect(self.surface, self.render_colour, self.rect)
        size = self.font.size(self.text)
        self.surface.blit(self.font.render(self.text, True, self.text_colour), (
        self.rect.x + (self.rect.width / 2) - (size[0] / 2), self.rect.y + (self.rect.height / 2) - (size[1] / 2)))


class Label:
    def __init__(self, surface, font, text, colour, x, y, width, height):
        self.surface = surface
        self.font = font
        self.text = text
        self.colour = colour
        self.rect = pygame.Rect(x, y, width, height)

    def render(self):
        size = self.font.size(self.text)
        self.surface.blit(self.font.render(self.text, True, self.colour), (
        self.rect.x + (self.rect.width / 2) - (size[0] / 2), self.rect.y + (self.rect.height / 2) - (size[1] / 2)))
