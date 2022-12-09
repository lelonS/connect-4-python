from classes.scene import Scene, SceneManager
from classes.text_label import Label,  TOP_CENTER
from classes.button import Button
import pygame


class HighscoreScene(Scene):
    back_button: Button
    labels: list[Label]
    sorted_list: list[tuple[str, dict]]  # list[tuple[plr_name, saved_data]]

    def __init__(self, screen: pygame.Surface, scene_manager: SceneManager) -> None:
        super().__init__(screen, scene_manager)
        highscore_dict = scene_manager.highscores
        self.sorted_list = sorted(highscore_dict.items(), key=self.sorter_key, reverse=True)
        self.back_button = Button(40, screen.get_height() - 100, 100, 50, 'BACK', self.scene_manager.go_back)

        self.labels = []
        self.labels.append(Label("HIGH SCORES", 100,  screen.get_width() / 2, 10, (255, 255, 255), TOP_CENTER))

        name_chars = 10
        win_chars = 6
        tie_chars = 6
        lose_chars = 6
        win_rate_chars = 6

        counter = 0

        start_y = 200
        start_x = self.screen.get_width() / 2

        padding = 50

        text = f" # |{'NAME':^{name_chars}}|{'WINS':^{win_chars}}|" + \
            f"{'TIES':^{tie_chars}}|{'LOSSES':^{lose_chars}}|{'WIN%':^{win_rate_chars}}|"

        info_label = Label(text, 32, start_x, start_y + counter * padding, (255, 255, 255), TOP_CENTER)

        self.labels.append(info_label)
        for plr_name, data in self.sorted_list:
            counter += 1
            if counter > 10:
                break
            win_rate = f"{data['wins'] / data['games'] * 100:.0f}%"
            text = f"{counter:>2}.|{plr_name:<{name_chars}}|{data['wins']:>{win_chars}}|" + \
                f"{data['ties']:>{tie_chars}}|{data['losses']:>{lose_chars}}|{win_rate:>{win_rate_chars}}|"

            label = Label(text, 32, start_x, start_y + counter * padding, (255, 255, 255), TOP_CENTER)
            self.labels.append(label)

    @staticmethod
    def sorter_key(val):
        data = val[1]
        score = 0
        score += data["wins"] * 1000
        score += data["ties"] * 1
        score += data["losses"] * -1

        return score

    def draw(self):
        self.back_button.draw(self.screen)
        for label in self.labels:
            label.draw(self.screen)
        pygame.display.update()

    def update(self, events: list[pygame.event.Event], dt: float):
        for event in events:
            self.back_button.update(event)
