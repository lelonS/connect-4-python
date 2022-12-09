import pygame
import json
from constants import WIDTH, HEIGHT
from classes.scene import SceneManager
from scenes.main_menu import MainMenu


def load_data():
    try:
        with open("highscores/high_score.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open("highscores/high_score.json", "w") as f:
        json.dump(data, f, indent=4)


def main():
    # Initialize pygame
    pygame.init()
    pygame.key.set_repeat(500, 50)

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    pygame.display.set_icon(logo)

    # Create scene manager
    scene_manager = SceneManager(screen, load_data())
    scene_manager.add_scene(MainMenu(screen, scene_manager))

    # Create clock
    clock = pygame.time.Clock()

    # Main menu
    while True:

        # Get clock info
        ms = clock.tick(60)
        seconds = ms / 1000

        # Check events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                save_data(scene_manager.highscores)
                pygame.quit()
                exit()
        scene_manager.update(events, seconds)

        # Draw
        scene_manager.draw()


if __name__ == '__main__':
    main()
