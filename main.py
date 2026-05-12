import pygame
import random
import json
import os
from enum import Enum

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Цвета
COLOR_BACKGROUND = (20, 20, 20)
COLOR_SNAKE = (0, 200, 0)
COLOR_SNAKE_HEAD = (0, 255, 0)
COLOR_APPLE = (200, 0, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (50, 50, 50)
COLOR_BUTTON_HOVER = (80, 80, 80)
COLOR_BUTTON_BORDER = (100, 100, 100)
COLOR_SETTINGS_BG = (30, 30, 30)

# Файлы данных
DATA_FILE = "snake_data.json"

# Локализация
TRANSLATIONS = {
    "ru": {
        "play": "Играть",
        "statistics": "Статистика",
        "exit": "Выйти",
        "settings": "⚙",
        "back": "Назад",
        "language": "Язык",
        "russian": "Русский",
        "english": "English",
        "games_played": "Игр сыграно",
        "avg_apples": "Среднее яблок за игру",
        "max_apples": "Максимум яблок",
        "score": "Счёт",
        "game_over": "Игра окончена!",
        "restart": "Нажмите R для рестарта или ESC для меню",
        "no_data": "Нет данных",
        "pause": "Пауза",
        "continue": "Продолжить",
    },
    "en": {
        "play": "Play",
        "statistics": "Statistics",
        "exit": "Exit",
        "settings": "⚙",
        "back": "Back",
        "language": "Language",
        "russian": "Russian",
        "english": "English",
        "games_played": "Games played",
        "avg_apples": "Avg apples per game",
        "max_apples": "Max apples",
        "score": "Score",
        "game_over": "Game Over!",
        "restart": "Press R to restart or ESC for menu",
        "no_data": "No data",
        "pause": "Pause",
        "continue": "Continue",
    }
}


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    STATISTICS = 4
    SETTINGS = 5
    PAUSED = 6


class DataManager:
    def __init__(self):
        self.data = {
            "language": "ru",
            "games_played": 0,
            "total_apples": 0,
            "max_apples": 0,
        }
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except Exception:
                pass

    def save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_language(self):
        return self.data.get("language", "ru")

    def set_language(self, lang):
        self.data["language"] = lang
        self.save()

    def add_game_result(self, apples):
        self.data["games_played"] += 1
        self.data["total_apples"] += apples
        if apples > self.data["max_apples"]:
            self.data["max_apples"] = apples
        self.save()

    def get_stats(self):
        games = self.data["games_played"]
        total = self.data["total_apples"]
        max_a = self.data["max_apples"]
        avg = total / games if games > 0 else 0
        return {
            "games_played": games,
            "avg_apples": avg,
            "max_apples": max_a,
        }


class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.hovered = False
        self.font = pygame.font.SysFont("arial", font_size)

    def draw(self, screen):
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_BUTTON_BORDER, self.rect, 2, border_radius=8)

        text_surface = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.data_manager = DataManager()
        self.state = GameState.MENU
        self.running = True

        # Шрифты
        self.font_large = pygame.font.SysFont("arial", 48)
        self.font_medium = pygame.font.SysFont("arial", 32)
        self.font_small = pygame.font.SysFont("arial", 24)

        # Кнопки меню
        btn_width, btn_height = 250, 50
        start_y = 200
        gap = 20
        center_x = WINDOW_WIDTH // 2 - btn_width // 2

        self.menu_buttons = {
            "play": Button(center_x, start_y, btn_width, btn_height, ""),
            "statistics": Button(center_x, start_y + btn_height + gap, btn_width, btn_height, ""),
            "exit": Button(center_x, start_y + 2 * (btn_height + gap), btn_width, btn_height, ""),
        }

        # Кнопка настроек (левый верхний угол)
        self.settings_button = Button(20, 20, 50, 50, "")

        # Кнопки настроек
        self.back_button = Button(center_x, 400, btn_width, btn_height, "")
        self.lang_ru_button = Button(center_x - 130, 250, 120, 50, "")
        self.lang_en_button = Button(center_x + 10, 250, 120, 50, "")

        # Кнопки статистики
        self.stats_back_button = Button(center_x, 450, btn_width, btn_height, "")

        # Кнопки паузы
        self.pause_continue_button = Button(center_x, 200, btn_width, btn_height, "")
        self.pause_menu_button = Button(center_x, 280, btn_width, btn_height, "")

        self.reset_game()
        self.update_texts()

    def t(self, key):
        lang = self.data_manager.get_language()
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def update_texts(self):
        self.menu_buttons["play"].text = self.t("play")
        self.menu_buttons["statistics"].text = self.t("statistics")
        self.menu_buttons["exit"].text = self.t("exit")
        self.settings_button.text = self.t("settings")
        self.back_button.text = self.t("back")
        self.lang_ru_button.text = self.t("russian")
        self.lang_en_button.text = self.t("english")
        self.stats_back_button.text = self.t("back")
        self.pause_continue_button.text = self.t("continue")
        self.pause_menu_button.text = self.t("exit")

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.apples_eaten = 0
        self.spawn_apple()
        self.game_speed = 8

    def spawn_apple(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                self.apple = pos
                break

    def get_direction_name(self):
        dx, dy = self.direction
        if dx == 1:
            return "right"
        elif dx == -1:
            return "left"
        elif dy == 1:
            return "down"
        else:
            return "up"

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            self.update(dt)
            self.draw()

        pygame.quit()

    def handle_event(self, event):
        if self.state == GameState.MENU:
            if self.menu_buttons["play"].handle_event(event):
                self.reset_game()
                self.state = GameState.PLAYING
            elif self.menu_buttons["statistics"].handle_event(event):
                self.state = GameState.STATISTICS
            elif self.menu_buttons["exit"].handle_event(event):
                self.running = False
            elif self.settings_button.handle_event(event):
                self.state = GameState.SETTINGS

        elif self.state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.direction != (0, 1):
                        self.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.direction != (0, -1):
                        self.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.direction != (1, 0):
                        self.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.direction != (-1, 0):
                        self.next_direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.PAUSED
                elif event.key == pygame.K_p:
                    self.state = GameState.PAUSED

        elif self.state == GameState.GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU

        elif self.state == GameState.STATISTICS:
            if self.stats_back_button.handle_event(event):
                self.state = GameState.MENU

        elif self.state == GameState.SETTINGS:
            if self.back_button.handle_event(event):
                self.state = GameState.MENU
            elif self.lang_ru_button.handle_event(event):
                self.data_manager.set_language("ru")
                self.update_texts()
            elif self.lang_en_button.handle_event(event):
                self.data_manager.set_language("en")
                self.update_texts()

        elif self.state == GameState.PAUSED:
            if self.pause_continue_button.handle_event(event):
                self.state = GameState.PLAYING
            elif self.pause_menu_button.handle_event(event):
                self.state = GameState.MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.PLAYING

    def update(self, dt):
        if self.state == GameState.PLAYING:
            self.move_timer = getattr(self, 'move_timer', 0) + dt
            move_interval = 1.0 / self.game_speed

            if self.move_timer >= move_interval:
                self.move_timer -= move_interval
                self.move_snake()

    def move_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Проверка столкновений со стенами
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            self.game_over()
            return

        # Проверка столкновений с собой
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Проверка съедания яблока
        if new_head == self.apple:
            self.apples_eaten += 1
            self.game_speed = min(8 + self.apples_eaten // 5, 20)
            self.spawn_apple()
        else:
            self.snake.pop()

    def game_over(self):
        self.data_manager.add_game_result(self.apples_eaten)
        self.state = GameState.GAME_OVER

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == GameState.STATISTICS:
            self.draw_statistics()
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause()

        pygame.display.flip()

    def draw_menu(self):
        # Заголовок
        title = self.font_large.render("SNAKE", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Кнопки
        for btn in self.menu_buttons.values():
            btn.draw(self.screen)

        # Кнопка настроек
        self.settings_button.draw(self.screen)

    def draw_game(self):
        # Рисуем сетку (тонкие линии)
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

        # Рисуем яблоко
        apple_rect = pygame.Rect(
            self.apple[0] * GRID_SIZE + 2,
            self.apple[1] * GRID_SIZE + 2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        pygame.draw.rect(self.screen, COLOR_APPLE, apple_rect, border_radius=4)

        # Рисуем змейку
        for i, segment in enumerate(self.snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
            seg_rect = pygame.Rect(
                segment[0] * GRID_SIZE + 1,
                segment[1] * GRID_SIZE + 1,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
            pygame.draw.rect(self.screen, color, seg_rect, border_radius=3)

        # Счёт
        score_text = self.font_small.render(f"{self.t('score')}: {self.apples_eaten}", True, COLOR_TEXT)
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        # Затемнение
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render(self.t("game_over"), True, COLOR_TEXT)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font_medium.render(f"{self.t('score')}: {self.apples_eaten}", True, COLOR_TEXT)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        self.screen.blit(score_text, score_rect)

        restart_text = self.font_small.render(self.t("restart"), True, COLOR_TEXT)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)

    def draw_statistics(self):
        title = self.font_large.render(self.t("statistics"), True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        stats = self.data_manager.get_stats()

        if stats["games_played"] == 0:
            no_data = self.font_medium.render(self.t("no_data"), True, COLOR_TEXT)
            no_data_rect = no_data.get_rect(center=(WINDOW_WIDTH // 2, 250))
            self.screen.blit(no_data, no_data_rect)
        else:
            lines = [
                f"{self.t('games_played')}: {stats['games_played']}",
                f"{self.t('avg_apples')}: {stats['avg_apples']:.1f}",
                f"{self.t('max_apples')}: {stats['max_apples']}",
            ]

            y = 200
            for line in lines:
                text = self.font_medium.render(line, True, COLOR_TEXT)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
                self.screen.blit(text, text_rect)
                y += 60

        self.stats_back_button.draw(self.screen)

    def draw_settings(self):
        title = self.font_large.render(self.t("settings"), True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        lang_label = self.font_medium.render(self.t("language") + ":", True, COLOR_TEXT)
        lang_rect = lang_label.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(lang_label, lang_rect)

        # Подсветка выбранного языка
        lang = self.data_manager.get_language()
        if lang == "ru":
            self.lang_ru_button.rect.inflate_ip(4, 4)
        else:
            self.lang_en_button.rect.inflate_ip(4, 4)

        self.lang_ru_button.draw(self.screen)
        self.lang_en_button.draw(self.screen)

        # Возвращаем размеры обратно
        if lang == "ru":
            self.lang_ru_button.rect.inflate_ip(-4, -4)
        else:
            self.lang_en_button.rect.inflate_ip(-4, -4)

        self.back_button.draw(self.screen)

    def draw_pause(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render(self.t("pause"), True, COLOR_TEXT)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(pause_text, pause_rect)

        self.pause_continue_button.draw(self.screen)
        self.pause_menu_button.draw(self.screen)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
