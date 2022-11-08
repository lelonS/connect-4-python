
#vilken font
font = pygame.font.Font('freesansbold.ttf', 16)
#colours
PURPLE = (230, 230, 250)
colour2_hotpink = (255,105,180)
colour3_red = (255,0,0)
#vilken text
text1 = font.render('Congratulations!!!', 400, 640, PURPLE)
text2 = font.render('You are a winner!', 320, 640, colour2_hotpink)
text3_Play_AGAIN = ('Play again?...press key', 160, 640, colour3_red)
# koordinater
text_pos_x = 400
text_pos_Y = 640


def draw_text(screen, text, size, x, y):

    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render('text', True, WHITE)
    screen.blit(text, (x, y))