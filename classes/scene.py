import pygame
from classes.grid_background import GridBackground


class Scene:
    screen: pygame.Surface
    scene_manager: 'SceneManager'

    def __init__(self, screen: pygame.Surface, scene_manager: 'SceneManager') -> None:
        self.screen = screen
        self.scene_manager = scene_manager

    def update(self, events: list[pygame.event.Event], dt: float):
        """Updates the scene

        Args:
            events (list[pygame.event.Event]): All events that have happened since the last update excluding quit events
            dt (float): Time since last update in seconds
            scene_manager (SceneManager): The scene manager that is managing this scene

        Raises:
            NotImplementedError: If update is not implemented
        """
        raise NotImplementedError

    def draw(self):
        """Draws the scene

        Raises:
            NotImplementedError: If draw is not implemented
        """
        raise NotImplementedError


class SceneManager:
    scenes: list[Scene]
    grid_background: GridBackground
    highscores: dict[str, dict[str, int]]

    def __init__(self, screen: pygame.Surface, highscores: dict[str, dict[str, int]]):
        self.scenes = []
        self.grid_background = GridBackground(screen)
        self.highscores = highscores

    def add_scene(self, scene: Scene):
        """Adds a scene, and goes to it

        Args:
            scene (Scene): The scene to add
        """
        self.scenes.append(scene)

    def go_back(self):
        """Goes back to the previous scene
        """
        if len(self.scenes) > 0:
            del self.scenes[-1]

    def go_to_origin_scene(self):
        """Goes to the first scene (the origin scene)
        """
        while len(self.scenes) > 1:
            self.go_back()

    def update(self, events: list[pygame.event.Event], dt: float):
        """Updates the current scene

        Args:
            events (list[pygame.event.Event]): All events except a quit event
            dt (float): Time since last update in seconds
        """
        if len(self.scenes) > 0:
            self.grid_background.update(dt)
            self.scenes[-1].update(events, dt)

    def draw(self):
        """Draws the current scene
        """
        if len(self.scenes) > 0:
            self.grid_background.draw()
            self.scenes[-1].draw()
