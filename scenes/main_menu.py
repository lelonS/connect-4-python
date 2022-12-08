import pygame
from classes.text_label import Label, TOP_CENTER, TOP_RIGHT
from classes.scene import Scene, SceneManager
from scenes.game_scene import GameScene, GameSceneBlind
from classes.selector import IntSelector, ModeSelector
from classes.text_box import TextBox
from classes.button import Button
from constants import WHITE, PLR_COLORS, BLIND_COLOR
from classes.player import Player


class MainMenu(Scene):
    col_selector: IntSelector
    row_selector: IntSelector
    plr_count_selector: IntSelector
    player_text_boxes: list[TextBox]
    play_button: Button
    labels: list[Label]

    def __init__(self, screen: pygame.Surface, scene_manager: SceneManager):
        super().__init__(screen, scene_manager)
        mid_x = int(screen.get_size()[0] / 2)

        # Create selectors
        self.col_selector = IntSelector(mid_x, 200, 50, 50, 7, 5, 12)
        self.row_selector = IntSelector(mid_x, 300, 50, 50, 6, 5, 12)
        self.plr_count_selector = IntSelector(mid_x, 400, 50, 50, 2, 2, 4)

        px, py, pw, ph = self.get_rect(700, 100, 'top-center', (mid_x, 25))
        self.mode_selector = ModeSelector(px, py, 100, 100, 500)

        # Create text boxes
        self.tb_width = 220
        self.tb_spacing = 50
        self.player_text_boxes = []
        for i in range(4):
            self.player_text_boxes.append(TextBox(0, 500, self.tb_width, 50, f'PLAYER{i + 1}', 7))
            self.player_text_boxes[i].border_color = PLR_COLORS[i]
        px, py, pw, ph = self.get_rect(300, 150, 'top-center', (mid_x, 575))

        # Create play button
        self.play_button = Button(px, py, pw, ph, 'PLAY', self.play)

        # Create labels
        self.labels = []
        # self.labels.append(Label('Connect4', 100, mid_x, 25, WHITE, align=TOP_CENTER))
        self.labels.append(Label('Columns:', 40, mid_x, 200, WHITE, align=TOP_RIGHT))
        self.labels.append(Label('Rows:', 40, mid_x, 300, WHITE, align=TOP_RIGHT))
        self.labels.append(Label('Players:', 40, mid_x, 400, WHITE, align=TOP_RIGHT))

    def center_textboxes(self):
        """Centers the text boxes in the middle of the screen
        """
        value = self.plr_count_selector.value
        tw = self.tb_width * value + self.tb_spacing * (value - 1)
        mid_x = int(self.screen.get_size()[0] / 2)
        start_x = mid_x - int(tw / 2)
        for i in range(4):
            self.player_text_boxes[i].rect.x = start_x + i * (self.tb_width + self.tb_spacing)

    @staticmethod
    def get_rect(width: int, height: int, align: str, pos: tuple[int, int]) -> tuple[int, int, int, int]:
        """

        Args:
            width: The width
            height: The height
            align: String of value(center, top-left, top-right)
            pos: Position to align to

        Returns: Rectangle with the new position

        """
        x = pos[0]
        y = pos[1]
        if align == 'center':
            new_x = x - width / 2
            new_y = y - height / 2
        elif align == 'top-center':
            new_x = x - width / 2
            new_y = y
        elif align == 'top-left':
            return pos[0], pos[1], width, height
        elif align == 'top-right':
            new_x = x - width
            new_y = y
        else:
            return pos[0], pos[1], width, height
        return int(new_x), int(new_y), width, height

    def check_duplicate_names(self):
        all_names = []
        for i in range(self.plr_count_selector.value):
            all_names.append(self.player_text_boxes[i].value)

        for i in range(self.plr_count_selector.value):
            textbox = self.player_text_boxes[i]
            if all_names.count(textbox.value) > 1:
                textbox.error = True
            else:
                textbox.error = False

    def tab_to_next(self, direction: int):
        """Tab to the next text box

        Returns: None

        """
        plr_count = self.plr_count_selector.value
        for i in range(plr_count):
            if self.player_text_boxes[i].is_focused:
                self.player_text_boxes[i].is_focused = False
                self.player_text_boxes[(i + direction) % plr_count].is_focused = True
                return
        # If no text box is focused, focus the first one unless the direction is negative
        if direction > 0:
            self.player_text_boxes[0].is_focused = True
        else:
            self.player_text_boxes[plr_count - 1].is_focused = True

    def play(self):
        """Starts the game with the selected settings

        Returns: None

        """
        players = []
        selected_names = []
        for i in range(self.plr_count_selector.value):
            name = self.player_text_boxes[i].value
            if name in selected_names:
                return
            selected_names.append(name)
            new_player = Player(name, PLR_COLORS[i])
            players.append(new_player)

        if self.mode_selector.value[0].lower() == 'blind4':
            game_scene = GameSceneBlind(self.screen, self.scene_manager,
                                        self.col_selector.value, self.row_selector.value, players)
        else:
            game_scene = GameScene(self.screen, self.scene_manager, self.col_selector.value,
                                   self.row_selector.value, players)

        self.scene_manager.add_scene(game_scene)

    def update(self, events: list[pygame.event.Event], seconds: float):
        """Updates the scene and handles events

        Args:
            events: A list of pygame events
            seconds: The number of seconds since the last update

        Returns:

        """
        self.scene_manager.grid_background.active_falling = True
        self.scene_manager.grid_background.amount_players = self.plr_count_selector.value
        self.scene_manager.grid_background.use_blind = self.mode_selector.value[0].lower() == 'blind4'

        for event in events:
            self.mode_selector.update(event)
            self.col_selector.update(event)
            self.row_selector.update(event)
            self.plr_count_selector.update(event)
            # Only update the selected player
            for i in range(self.plr_count_selector.value):
                self.player_text_boxes[i].update(event)
            self.play_button.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                        self.tab_to_next(-1)  # Shift is pressed, go backwards
                    else:  # Tab to the next text box
                        self.tab_to_next(1)

        self.check_duplicate_names()
        self.center_textboxes()

    def draw(self):
        """Draws the scene to the screen
        """

        # draw a circle at mouse position
        # pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 70)
        # Draw title
        for label in self.labels:
            label.draw(self.screen)
        # Draw column buttons
        self.mode_selector.draw(self.screen)
        self.col_selector.draw(self.screen)
        self.row_selector.draw(self.screen)
        self.plr_count_selector.draw(self.screen)
        for i in range(self.plr_count_selector.value):  # Only draw the number of players selected
            if self.mode_selector.value[0].lower() == 'blind4':
                self.player_text_boxes[i].border_color = BLIND_COLOR
            else:
                self.player_text_boxes[i].border_color = PLR_COLORS[i]
            self.player_text_boxes[i].draw(self.screen)
        # Draw play button
        self.play_button.draw(self.screen)

        pygame.display.update()
