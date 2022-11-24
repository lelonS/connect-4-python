import pygame

class Button:
    text: str
    rect: pygame.Rect
    text_color: tuple[int, int, int]
    bg_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    border_width: int
    font: pygame.font.Font
    font_size: int


    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.border_width = 2
        self.font_size = height
        self.font = pygame.font.SysFont("consolas", self.font_size)


    def draw(self, screen: pygame.Surface):
        # Draw background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        #draw text
        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.rect.x, self.rect.y))

    def isClicked(self, event) -> bool:
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pos):
                    return True


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Button")

    button = Button(50, 50, 200, 60, 'test')

    run = True

    while run:
        for event in pygame.event.get():
            if button.isClicked(event):
                print('Clicked')
            if event.type == pygame.QUIT:
                run = False

        screen.fill((0, 0, 0))
        button.draw(screen)
        pygame.display.update()

    pygame.quit()

