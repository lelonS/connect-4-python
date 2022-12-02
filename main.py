import pygame
from constants import WIDTH, HEIGHT
from classes.scene import SceneManager
from scenes.main_menu import MainMenu

pygame.init()
pygame.key.set_repeat(500, 50)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect4")


def main():
    # Create scene manager
    scene_manager = SceneManager()
    # scene_manager.add_scene(GameScene(screen, BOARD_BOTTOM_LEFT, 7, 6, []))
    scene_manager.add_scene(MainMenu(screen))

    # Create clock
    clock = pygame.time.Clock()

    # Main menu
    while True:

        # Get clock info
        ms = clock.tick()
        seconds = ms / 1000

        # Check events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        scene_manager.update(events, seconds)

        # Draw
        scene_manager.draw()

    # Open game screen
    # game_screen = GameScreen(screen, (0, 600), 7, 6, [])
    # game_screen.run_game()


if __name__ == '__main__':
    main()
