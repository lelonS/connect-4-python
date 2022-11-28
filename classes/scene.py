import pygame


class Scene:
    screen: pygame.Surface

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def update(self, events: list[pygame.event.Event], dt: float, scene_manager: 'SceneManager'):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError


class SceneManager:
    scenes: list[Scene]

    def __init__(self):
        self.scenes = []

    def add_scene(self, scene):
        self.scenes.append(scene)

    def go_back(self):
        if len(self.scenes) > 0:
            del self.scenes[-1]

    def go_to_origin_scene(self):
        while len(self.scenes) > 1:
            self.go_back()

    def update(self, events: list[pygame.event.Event], dt: float):
        if len(self.scenes) > 0:
            self.scenes[-1].update(events, dt, self)

    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw()
