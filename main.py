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
COLOR_WHITE_BLOCK = (255, 255, 255)
COLOR_RED_BLOCK = (255, 50, 50)
COLOR_HOTBAR = (40, 40, 40)
COLOR_HOTBAR_SELECTED = (70, 70, 70)
COLOR_INPUT_BG = (35, 35, 35)
COLOR_INPUT_BORDER = (80, 80, 80)

# Файлы данных
DATA_FILE = "snake_data.json"

# Локализация
TRANSLATIONS = {
    "ru": {
        "play": "Играть",
        "statistics": "Статистика",
        "exit": "Выйти",
        "settings": "⚙",
        "settings_title": "Настройки",
        "back": "Назад",
        "language": "Язык",
        "russian": "Русский",
        "english": "English",
        "chinese": "中文",
        "german": "Немецкий",
        "games_played": "Игр сыграно",
        "avg_apples": "Среднее яблок за игру",
        "max_apples": "Максимум яблок",
        "score": "Счёт",
        "game_over": "Игра окончена!",
        "restart": "Нажмите R для рестарта или ESC для меню",
        "no_data": "Нет данных",
        "pause": "Пауза",
        "continue": "Продолжить",
        "create_world": "Создать мир",
        "my_worlds": "Мои миры",
        "world_size": "Размер мира",
        "apple_count": "Количество яблок",
        "snake_hp": "HP змеи",
        "create": "Создать",
        "world_name": "Название мира",
        "no_worlds": "Нет миров",
        "white_block": "Белый блок (смерть)",
        "red_block": "Красный блок (-1 HP)",
        "erase": "Ластик",
        "save": "Сохранить",
        "hp": "HP",
        "classic_stats": "Обычная игра",
        "custom_stats": "Кастомные миры",
        "edit": "Ред",
        "delete": "Удл",
        "name_exists": "Мир с таким именем уже существует!",
        "block_info_title": "Информация о блоках",
        "block_info_white": "Белый блок — при столкновении змея умирает",
        "block_info_red": "Красный блок — при столкновении отнимает 1 HP и блок исчезает",
        "block_info_erase": "Ластик — удаляет блоки с поля",
        "close": "Закрыть",
    },
    "en": {
        "play": "Play",
        "statistics": "Statistics",
        "exit": "Exit",
        "settings": "⚙",
        "settings_title": "Settings",
        "back": "Back",
        "language": "Language",
        "russian": "Russian",
        "english": "English",
        "chinese": "中文",
        "german": "German",
        "games_played": "Games played",
        "avg_apples": "Avg apples per game",
        "max_apples": "Max apples",
        "score": "Score",
        "game_over": "Game Over!",
        "restart": "Press R to restart or ESC for menu",
        "no_data": "No data",
        "pause": "Pause",
        "continue": "Continue",
        "create_world": "Create World",
        "my_worlds": "My Worlds",
        "world_size": "World size",
        "apple_count": "Apple count",
        "snake_hp": "Snake HP",
        "create": "Create",
        "world_name": "World name",
        "no_worlds": "No worlds",
        "white_block": "White block (death)",
        "red_block": "Red block (-1 HP)",
        "erase": "Eraser",
        "save": "Save",
        "hp": "HP",
        "classic_stats": "Classic game",
        "custom_stats": "Custom worlds",
        "edit": "Edit",
        "delete": "Del",
        "name_exists": "World with this name already exists!",
        "block_info_title": "Block Information",
        "block_info_white": "White block — snake dies on collision",
        "block_info_red": "Red block — removes 1 HP then disappears",
        "block_info_erase": "Eraser — removes blocks from the field",
        "close": "Close",
    },
    "zh": {
        "play": "开始游戏",
        "statistics": "统计",
        "exit": "退出",
        "settings": "⚙",
        "settings_title": "设置",
        "back": "返回",
        "language": "语言",
        "russian": "俄语",
        "english": "英语",
        "chinese": "中文",
        "german": "德语",
        "games_played": "游戏次数",
        "avg_apples": "平均每局苹果数",
        "max_apples": "最多苹果数",
        "score": "得分",
        "game_over": "游戏结束！",
        "restart": "按 R 重新开始 或按 ESC 返回菜单",
        "no_data": "暂无数据",
        "pause": "暂停",
        "continue": "继续",
        "create_world": "创建世界",
        "my_worlds": "我的世界",
        "world_size": "世界大小",
        "apple_count": "苹果数量",
        "snake_hp": "蛇的生命值",
        "create": "创建",
        "world_name": "世界名称",
        "no_worlds": "没有世界",
        "white_block": "白块 (死亡)",
        "red_block": "红块 (-1 HP)",
        "erase": "橡皮擦",
        "save": "保存",
        "hp": "HP",
        "classic_stats": "经典模式",
        "custom_stats": "自定义世界",
        "edit": "编辑",
        "delete": "删除",
        "name_exists": "该名称的世界已存在！",
        "block_info_title": "方块信息",
        "block_info_white": "白块 — 蛇碰到即死亡",
        "block_info_red": "红块 — 蛇碰到扣除1点生命值后消失",
        "block_info_erase": "橡皮擦 — 移除场上的方块",
        "close": "关闭",
    },
    "de": {
        "play": "Spielen",
        "statistics": "Statistik",
        "exit": "Beenden",
        "settings": "⚙",
        "settings_title": "Einstellungen",
        "back": "Zurück",
        "language": "Sprache",
        "russian": "Russisch",
        "english": "Englisch",
        "chinese": "Chinesisch",
        "german": "Deutsch",
        "games_played": "Gespielte Spiele",
        "avg_apples": "Ø Äpfel pro Spiel",
        "max_apples": "Max. Äpfel",
        "score": "Punkte",
        "game_over": "Spiel vorbei!",
        "restart": "Drücke R für Neustart oder ESC für Menü",
        "no_data": "Keine Daten",
        "pause": "Pause",
        "continue": "Fortsetzen",
        "create_world": "Welt erstellen",
        "my_worlds": "Meine Welten",
        "world_size": "Weltgröße",
        "apple_count": "Apfelanzahl",
        "snake_hp": "Schlangen-HP",
        "create": "Erstellen",
        "world_name": "Weltname",
        "no_worlds": "Keine Welten",
        "white_block": "Weißer Block (Tod)",
        "red_block": "Roter Block (-1 HP)",
        "erase": "Radiergummi",
        "save": "Speichern",
        "hp": "HP",
        "classic_stats": "Klassisches Spiel",
        "custom_stats": "Benutzerdefinierte Welten",
        "edit": "Bearb",
        "delete": "Lsch",
        "name_exists": "Eine Welt mit diesem Namen existiert bereits!",
        "block_info_title": "Block-Informationen",
        "block_info_white": "Weißer Block — Schlange stirbt bei Kollision",
        "block_info_red": "Roter Block — -1 HP bei Kollision, dann verschwindet er",
        "block_info_erase": "Radiergummi — entfernt Blöcke vom Feld",
        "close": "Schließen",
    }
}


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    STATISTICS = 4
    SETTINGS = 5
    PAUSED = 6
    CREATE_WORLD = 7
    WORLD_EDITOR = 8
    MY_WORLDS = 9
    PLAYING_CUSTOM = 10


class DataManager:
    def __init__(self):
        self.data = {
            "language": "ru",
            "games_played": 0,
            "total_apples": 0,
            "max_apples": 0,
            "custom_games_played": 0,
            "custom_total_apples": 0,
            "custom_max_apples": 0,
            "worlds": [],
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

    def add_custom_game_result(self, apples):
        self.data["custom_games_played"] += 1
        self.data["custom_total_apples"] += apples
        if apples > self.data["custom_max_apples"]:
            self.data["custom_max_apples"] = apples
        self.save()

    def get_stats(self):
        games = self.data["games_played"]
        total = self.data["total_apples"]
        max_a = self.data["max_apples"]
        avg = total / games if games > 0 else 0
        custom_games = self.data["custom_games_played"]
        custom_total = self.data["custom_total_apples"]
        custom_max = self.data["custom_max_apples"]
        custom_avg = custom_total / custom_games if custom_games > 0 else 0
        return {
            "games_played": games,
            "avg_apples": avg,
            "max_apples": max_a,
            "custom_games_played": custom_games,
            "custom_avg_apples": custom_avg,
            "custom_max_apples": custom_max,
        }

    def get_worlds(self):
        return self.data.get("worlds", [])

    def add_world(self, world):
        worlds = self.data.get("worlds", [])
        world["id"] = len(worlds) + 1
        worlds.append(world)
        self.data["worlds"] = worlds
        self.save()

    def delete_world(self, world_id):
        worlds = self.data.get("worlds", [])
        self.data["worlds"] = [w for w in worlds if w.get("id") != world_id]
        self.save()

    def update_world(self, world_id, world_data):
        worlds = self.data.get("worlds", [])
        for i, w in enumerate(worlds):
            if w.get("id") == world_id:
                worlds[i] = world_data
                break
        self.data["worlds"] = worlds
        self.save()


class Button:
    def __init__(self, x, y, width, height, text, font_size=32, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.hovered = False
        if font is not None:
            self.font = font
        else:
            font_path = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, font_size)
            else:
                self.font = pygame.font.Font(None, font_size)

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


class InputField:
    def __init__(self, x, y, width, height, initial_value="", font_size=24, min_value=None, max_value=None, numeric_only=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = str(initial_value)
        self.active = False
        self.min_value = min_value
        self.max_value = max_value
        self.numeric_only = numeric_only
        font_path = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)
        self.color = COLOR_INPUT_BG

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_INPUT_BORDER, self.rect, border_radius=4)
        pygame.draw.rect(screen, self.color, self.rect.inflate(-2, -2), border_radius=3)
        # Обрезаем текст если не влезает
        display_text = self.text
        text_surface = self.font.render(display_text, True, COLOR_TEXT)
        while text_surface.get_width() > self.rect.width - 20 and len(display_text) > 0:
            display_text = display_text[1:]
            text_surface = self.font.render(display_text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.rect.collidepoint(event.pos)
                self.color = (50, 50, 50) if self.active else COLOR_INPUT_BG
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = COLOR_INPUT_BG
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif self.numeric_only:
                if event.key == pygame.K_MINUS:
                    self.text += "-"
                elif event.unicode.isdigit() or event.unicode == "":
                    self.text += event.unicode
                # Валидация для числовых полей
                try:
                    val = int(self.text) if self.text else 0
                    if self.min_value is not None and val < self.min_value:
                        self.text = str(self.min_value)
                    if self.max_value is not None and val > self.max_value:
                        self.text = str(self.max_value)
                except ValueError:
                    if self.text and self.text != "-":
                        self.text = ""
            else:
                # Текстовый ввод для названия мира
                if event.unicode.isprintable():
                    self.text += event.unicode
        return False

    def get_value(self):
        try:
            return int(self.text) if self.text else 0
        except ValueError:
            return 0


class SliderInput:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val=None, font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val if initial_val is not None else min_val
        self.dragging = False
        font_path = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        # Фон слайдера
        pygame.draw.rect(screen, COLOR_BUTTON, self.rect, border_radius=4)
        # Ползунок
        ratio = (self.value - self.min_val) / max(1, self.max_val - self.min_val)
        thumb_x = self.rect.x + int(ratio * self.rect.width)
        thumb_rect = pygame.Rect(thumb_x - 8, self.rect.y - 5, 16, self.rect.height + 10)
        pygame.draw.rect(screen, COLOR_BUTTON_BORDER, thumb_rect, border_radius=4)
        # Значение
        text = self.font.render(str(self.value), True, COLOR_TEXT)
        screen.blit(text, (self.rect.right + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ratio = (self.value - self.min_val) / max(1, self.max_val - self.min_val)
                thumb_x = self.rect.x + int(ratio * self.rect.width)
                thumb_rect = pygame.Rect(thumb_x - 10, self.rect.y - 5, 20, self.rect.height + 10)
                if thumb_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
        return False

    def update_value(self, mouse_x):
        ratio = (mouse_x - self.rect.x) / self.rect.width
        ratio = max(0, min(1, ratio))
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.data_manager = DataManager()
        self.state = GameState.MENU
        self.running = True

        # Шрифты
        font_path = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
        font_to_use = font_path if os.path.exists(font_path) else None
        self.font_large = pygame.font.Font(font_to_use, 48)
        self.font_medium = pygame.font.Font(font_to_use, 32)
        self.font_small = pygame.font.Font(font_to_use, 24)

        # Кнопки меню
        btn_width, btn_height = 250, 50
        start_y = 150
        gap = 20
        center_x = WINDOW_WIDTH // 2 - btn_width // 2

        self.menu_buttons = {
            "play": Button(center_x, start_y, btn_width, btn_height, ""),
            "create_world": Button(center_x, start_y + btn_height + gap, btn_width, btn_height, ""),
            "my_worlds": Button(center_x, start_y + 2 * (btn_height + gap), btn_width, btn_height, ""),
            "statistics": Button(center_x, start_y + 3 * (btn_height + gap), btn_width, btn_height, ""),
            "exit": Button(center_x, start_y + 4 * (btn_height + gap), btn_width, btn_height, ""),
        }

        # Кнопка настроек (левый верхний угол) — отдельный шрифт для символа ⚙
        symbol_font_path = "/usr/share/fonts/TTF/DejaVuSansCondensed.ttf"
        if os.path.exists(symbol_font_path):
            symbol_font = pygame.font.Font(symbol_font_path, 36)
        else:
            symbol_font = None
        self.settings_button = Button(20, 20, 50, 50, "", font_size=36, font=symbol_font)

        # Кнопки настроек
        self.back_button = Button(center_x, 400, btn_width, btn_height, "")

        # Кнопки языков на всю ширину экрана
        lang_margin = 40
        lang_gap = 20
        lang_count = 4
        lang_btn_width = (WINDOW_WIDTH - 2 * lang_margin - (lang_count - 1) * lang_gap) // lang_count
        lang_btn_height = 50
        lang_y = 250
        lang_font_size = 24
        self.lang_ru_button = Button(lang_margin, lang_y, lang_btn_width, lang_btn_height, "", font_size=lang_font_size)
        self.lang_en_button = Button(lang_margin + lang_btn_width + lang_gap, lang_y, lang_btn_width, lang_btn_height, "", font_size=lang_font_size)
        self.lang_zh_button = Button(lang_margin + 2 * (lang_btn_width + lang_gap), lang_y, lang_btn_width, lang_btn_height, "", font_size=lang_font_size)
        self.lang_de_button = Button(lang_margin + 3 * (lang_btn_width + lang_gap), lang_y, lang_btn_width, lang_btn_height, "", font_size=lang_font_size)

        # Кнопки статистики
        self.stats_back_button = Button(center_x, 450, btn_width, btn_height, "")

        # Кнопки паузы
        self.pause_continue_button = Button(center_x, 200, btn_width, btn_height, "")
        self.pause_menu_button = Button(center_x, 280, btn_width, btn_height, "")

        # Кнопки создания мира
        self.create_world_inputs = {}
        self.setup_create_world_inputs(center_x)

        # Кнопки редактора мира
        self.editor_buttons = {}
        self.hotbar_slots = []
        self.selected_tool = "white"  # white, red, erase
        self.setup_editor_buttons()

        # Кнопки моих миров
        self.world_buttons = []
        self.setup_my_worlds_buttons()

        # Переменные для текущего мира
        self.current_world = None
        self.custom_grid_size = GRID_SIZE
        self.custom_grid_width = GRID_WIDTH
        self.custom_grid_height = GRID_HEIGHT
        self.white_blocks = set()
        self.red_blocks = set()
        self.snake_max_hp = 3
        self.snake_current_hp = 3

        self.reset_game()
        self.update_texts()

    def setup_create_world_inputs(self, center_x):
        # Поля для создания мира — располагаем в строку: метка | поле | подсказка
        input_y = 160
        gap = 60
        input_width = 100
        input_height = 36
        field_x = WINDOW_WIDTH // 2 + 20  # Поле ввода правее

        # Размер мира (5-128)
        self.world_size_input = InputField(field_x, input_y, input_width, input_height, "20", numeric_only=True, min_value=5, max_value=128)

        # Количество яблок (1-9999)
        self.apple_count_input = InputField(field_x, input_y + gap, input_width, input_height, "10", numeric_only=True, min_value=1, max_value=9999)

        # HP змеи (1-20)
        self.snake_hp_input = InputField(field_x, input_y + 2 * gap, input_width, input_height, "3", numeric_only=True, min_value=1, max_value=20)

        # Название мира
        self.world_name_input = InputField(field_x, input_y + 3 * gap, 200, input_height, "Новый мир")

        # Ошибка дубликата
        self.name_error = ""

        # Кнопки
        self.create_world_create_btn = Button(center_x - 100, input_y + 4 * gap + 30, 200, 50, "")
        self.create_world_back_btn = Button(center_x - 100, input_y + 4 * gap + 95, 200, 50, "")

    def setup_editor_buttons(self):
        # Хотбар внизу экрана
        hotbar_y = WINDOW_HEIGHT - 70
        slot_size = 50
        gap = 10
        total_width = 3 * slot_size + 2 * gap
        start_x = (WINDOW_WIDTH - total_width) // 2

        self.hotbar_slots = [
            {"rect": pygame.Rect(start_x, hotbar_y, slot_size, slot_size), "type": "white", "color": COLOR_WHITE_BLOCK},
            {"rect": pygame.Rect(start_x + slot_size + gap, hotbar_y, slot_size, slot_size), "type": "red", "color": COLOR_RED_BLOCK},
            {"rect": pygame.Rect(start_x + 2 * (slot_size + gap), hotbar_y, slot_size, slot_size), "type": "erase", "color": (100, 100, 100)},
        ]

        # Кнопки сохранения, назад и инфо
        self.editor_save_btn = Button(WINDOW_WIDTH - 190, 10, 180, 40, "")
        self.editor_back_btn = Button(10, 10, 100, 40, "")
        self.editor_info_btn = Button(120, 10, 40, 40, "?", font_size=28)
        self.show_block_info = False

    def setup_my_worlds_buttons(self):
        self.my_worlds_back_btn = Button(WINDOW_WIDTH // 2 - 100, 500, 200, 50, "")
        self.world_buttons = []

    def t(self, key):
        lang = self.data_manager.get_language()
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def update_texts(self):
        self.menu_buttons["play"].text = self.t("play")
        self.menu_buttons["create_world"].text = self.t("create_world")
        self.menu_buttons["my_worlds"].text = self.t("my_worlds")
        self.menu_buttons["statistics"].text = self.t("statistics")
        self.menu_buttons["exit"].text = self.t("exit")
        self.settings_button.text = self.t("settings")
        self.back_button.text = self.t("back")
        self.lang_ru_button.text = self.t("russian")
        self.lang_en_button.text = self.t("english")
        self.lang_zh_button.text = self.t("chinese")
        self.lang_de_button.text = self.t("german")
        self.stats_back_button.text = self.t("back")
        self.pause_continue_button.text = self.t("continue")
        self.pause_menu_button.text = self.t("exit")
        self.create_world_create_btn.text = self.t("create")
        self.create_world_back_btn.text = self.t("back")
        self.editor_save_btn.text = self.t("save")
        self.editor_back_btn.text = self.t("back")
        self.editor_info_btn.text = "?"
        self.my_worlds_back_btn.text = self.t("back")
        # Обновляем тексты кнопок миров
        for item in self.world_buttons:
            item["edit_btn"].text = self.t("edit")
            item["delete_btn"].text = self.t("delete")

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
            elif self.menu_buttons["create_world"].handle_event(event):
                self.state = GameState.CREATE_WORLD
            elif self.menu_buttons["my_worlds"].handle_event(event):
                self.state = GameState.MY_WORLDS
                self.update_world_buttons()
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

        elif self.state == GameState.PLAYING_CUSTOM:
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
                key_char = event.unicode.lower() if event.unicode else ""
                if (event.key == pygame.K_r or event.key == pygame.K_RETURN
                        or event.key == pygame.K_SPACE or key_char in ("r", "к")):
                    if self.current_world is None:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    else:
                        self.reset_custom_game()
                        self.state = GameState.PLAYING_CUSTOM
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    self.current_world = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.current_world is None:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    else:
                        self.reset_custom_game()
                        self.state = GameState.PLAYING_CUSTOM

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
            elif self.lang_zh_button.handle_event(event):
                self.data_manager.set_language("zh")
                self.update_texts()
            elif self.lang_de_button.handle_event(event):
                self.data_manager.set_language("de")
                self.update_texts()

        elif self.state == GameState.PAUSED:
            if self.pause_continue_button.handle_event(event):
                self.state = GameState.PLAYING if self.current_world is None else GameState.PLAYING_CUSTOM
            elif self.pause_menu_button.handle_event(event):
                self.state = GameState.MENU
                self.current_world = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.PLAYING if self.current_world is None else GameState.PLAYING_CUSTOM

        elif self.state == GameState.CREATE_WORLD:
            self.world_name_input.handle_event(event)
            self.world_size_input.handle_event(event)
            self.apple_count_input.handle_event(event)
            self.snake_hp_input.handle_event(event)
            if self.create_world_create_btn.handle_event(event):
                self.create_new_world()
            elif self.create_world_back_btn.handle_event(event):
                self.state = GameState.MENU

        elif self.state == GameState.WORLD_EDITOR:
            self.handle_editor_event(event)

        elif self.state == GameState.MY_WORLDS:
            if self.my_worlds_back_btn.handle_event(event):
                self.state = GameState.MENU
            for btn in self.world_buttons:
                if btn["edit_btn"].handle_event(event):
                    self.edit_world(btn["world"])
                    break
                elif btn["delete_btn"].handle_event(event):
                    self.delete_world(btn["world"])
                    break
                elif btn["btn"].handle_event(event):
                    self.load_world(btn["world"])
                    break

    def create_new_world(self):
        size = self.world_size_input.get_value()
        apples = self.apple_count_input.get_value()
        hp = self.snake_hp_input.get_value()
        name = self.world_name_input.text.strip() or "Новый мир"

        # Проверка на дубликат названия
        worlds = self.data_manager.get_worlds()
        for world in worlds:
            if world["name"] == name:
                self.name_error = self.t("name_exists")
                return

        self.current_world = {
            "id": -1,
            "name": name,
            "size": size,
            "apple_count": apples,
            "snake_hp": hp,
            "white_blocks": [],
            "red_blocks": [],
        }
        self.custom_grid_width = size
        self.custom_grid_height = size
        self.white_blocks = set()
        self.red_blocks = set()
        self.name_error = ""
        self.state = GameState.WORLD_EDITOR

    def handle_editor_event(self, event):
        if self.editor_back_btn.handle_event(event):
            self.state = GameState.MENU
            self.current_world = None
        elif self.editor_save_btn.handle_event(event):
            self.save_current_world()
            # Если редактировали существующий мир — возвращаемся в "Мои миры"
            if self.current_world and self.current_world.get("id", -1) > 0:
                self.state = GameState.MY_WORLDS
                self.update_world_buttons()
            else:
                self.state = GameState.MENU
            self.current_world = None
        elif self.editor_info_btn.handle_event(event):
            self.show_block_info = not self.show_block_info
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Выбор инструмента в хотбаре
                for slot in self.hotbar_slots:
                    if slot["rect"].collidepoint(event.pos):
                        self.selected_tool = slot["type"]
                        return
                # Размещение блока на поле
                self.place_block(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                # Рисование при зажатой ЛКМ
                self.place_block(event.pos)

    def place_block(self, pos):
        # Проверяем, что клик не в хотбар
        hotbar_rect = pygame.Rect(0, WINDOW_HEIGHT - 80, WINDOW_WIDTH, 80)
        if hotbar_rect.collidepoint(pos):
            return

        # Определяем координаты клетки
        # Поле центрируется на экране
        grid_pixel_width = self.custom_grid_width * GRID_SIZE
        grid_pixel_height = self.custom_grid_height * GRID_SIZE
        offset_x = (WINDOW_WIDTH - grid_pixel_width) // 2
        offset_y = (WINDOW_HEIGHT - grid_pixel_height - 100) // 2  # Отступ для хотбара

        cell_x = (pos[0] - offset_x) // GRID_SIZE
        cell_y = (pos[1] - offset_y) // GRID_SIZE

        if 0 <= cell_x < self.custom_grid_width and 0 <= cell_y < self.custom_grid_height:
            cell = (cell_x, cell_y)
            if self.selected_tool == "white":
                self.white_blocks.add(cell)
                self.red_blocks.discard(cell)
            elif self.selected_tool == "red":
                self.red_blocks.add(cell)
                self.white_blocks.discard(cell)
            elif self.selected_tool == "erase":
                self.white_blocks.discard(cell)
                self.red_blocks.discard(cell)

    def save_current_world(self):
        if self.current_world:
            self.current_world["white_blocks"] = list(self.white_blocks)
            self.current_world["red_blocks"] = list(self.red_blocks)
            world_id = self.current_world.get("id", -1)
            if world_id > 0:
                # Обновляем существующий мир
                self.data_manager.update_world(world_id, self.current_world)
            else:
                # Создаём новый мир
                self.data_manager.add_world(self.current_world)
            self.current_world = None

    def edit_world(self, world):
        # Загружаем мир для редактирования
        self.current_world = world.copy()
        self.custom_grid_width = world["size"]
        self.custom_grid_height = world["size"]
        self.white_blocks = set(tuple(b) for b in world.get("white_blocks", []))
        self.red_blocks = set(tuple(b) for b in world.get("red_blocks", []))
        # Предзаполняем поля ввода
        self.world_size_input.text = str(world["size"])
        self.apple_count_input.text = str(world.get("apple_count", 10))
        self.snake_hp_input.text = str(world.get("snake_hp", 3))
        self.world_name_input.text = world["name"]
        self.name_error = ""
        self.state = GameState.WORLD_EDITOR

    def delete_world(self, world):
        self.data_manager.delete_world(world["id"])
        self.update_world_buttons()

    def update_world_buttons(self):
        worlds = self.data_manager.get_worlds()
        self.world_buttons = []
        btn_width, btn_height = 280, 50
        start_y = 150
        gap = 15
        center_x = WINDOW_WIDTH // 2 - btn_width // 2 - 60
        icon_btn_w = 50
        icon_btn_h = 36
        icon_gap = 8
        for i, world in enumerate(worlds):
            y = start_y + i * (btn_height + gap)
            # Основная кнопка мира
            btn = Button(center_x, y, btn_width, btn_height,
                        f"{world['name']} ({world['size']}x{world['size']})")
            # Кнопка редактировать справа
            edit_btn = Button(center_x + btn_width + icon_gap, y + (btn_height - icon_btn_h) // 2, icon_btn_w, icon_btn_h, self.t("edit"), font_size=18)
            # Кнопка удалить
            delete_btn = Button(center_x + btn_width + icon_gap + icon_btn_w + icon_gap, y + (btn_height - icon_btn_h) // 2, icon_btn_w, icon_btn_h, self.t("delete"), font_size=18)
            self.world_buttons.append({"btn": btn, "edit_btn": edit_btn, "delete_btn": delete_btn, "world": world})

    def load_world(self, world):
        self.current_world = world.copy()
        self.custom_grid_width = world["size"]
        self.custom_grid_height = world["size"]
        self.white_blocks = set(tuple(b) for b in world.get("white_blocks", []))
        self.red_blocks = set(tuple(b) for b in world.get("red_blocks", []))
        self.snake_max_hp = world.get("snake_hp", 3)
        self.reset_custom_game()
        self.state = GameState.PLAYING_CUSTOM

    def reset_custom_game(self):
        self.snake = [(self.custom_grid_width // 2, self.custom_grid_height // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.apples_eaten = 0
        self.snake_current_hp = self.snake_max_hp
        self.game_speed = 8
        self.spawn_custom_apples()

    def spawn_custom_apples(self):
        total_cells = self.custom_grid_width * self.custom_grid_height
        apple_count = self.current_world.get("apple_count", 10)
        snake_pos = set(self.snake)

        if apple_count >= total_cells - len(snake_pos):
            # Яблоки везде кроме змеи
            self.apples = []
            for x in range(self.custom_grid_width):
                for y in range(self.custom_grid_height):
                    if (x, y) not in snake_pos and (x, y) not in self.white_blocks and (x, y) not in self.red_blocks:
                        self.apples.append((x, y))
        else:
            self.apples = []
            occupied = snake_pos | self.white_blocks | self.red_blocks
            attempts = 0
            while len(self.apples) < apple_count and attempts < 10000:
                pos = (random.randint(0, self.custom_grid_width - 1),
                       random.randint(0, self.custom_grid_height - 1))
                if pos not in occupied and pos not in self.apples:
                    self.apples.append(pos)
                attempts += 1

    def update(self, dt):
        if self.state == GameState.PLAYING:
            self.move_timer = getattr(self, 'move_timer', 0) + dt
            move_interval = 1.0 / self.game_speed

            if self.move_timer >= move_interval:
                self.move_timer -= move_interval
                self.move_snake()

        elif self.state == GameState.PLAYING_CUSTOM:
            self.move_timer = getattr(self, 'move_timer', 0) + dt
            move_interval = 1.0 / self.game_speed

            if self.move_timer >= move_interval:
                self.move_timer -= move_interval
                self.move_custom_snake()

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

    def move_custom_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Проверка столкновений со стенами
        if new_head[0] < 0 or new_head[0] >= self.custom_grid_width or new_head[1] < 0 or new_head[1] >= self.custom_grid_height:
            self.game_over()
            return

        # Проверка столкновений с собой
        if new_head in self.snake:
            self.game_over()
            return

        # Проверка белых блоков (смерть)
        if new_head in self.white_blocks:
            self.game_over()
            return

        # Проверка красных блоков (-1 HP)
        if new_head in self.red_blocks:
            self.snake_current_hp -= 1
            self.red_blocks.discard(new_head)  # Блок исчезает
            if self.snake_current_hp <= 0:
                self.game_over()
                return

        self.snake.insert(0, new_head)

        # Проверка съедания яблока
        if new_head in self.apples:
            self.apples_eaten += 1
            self.apples.remove(new_head)
            self.game_speed = min(8 + self.apples_eaten // 5, 20)
        else:
            self.snake.pop()

    def game_over(self):
        # Кастомные миры не влияют на общую статистику
        if self.current_world is None:
            self.data_manager.add_game_result(self.apples_eaten)
        else:
            self.data_manager.add_custom_game_result(self.apples_eaten)
        self.state = GameState.GAME_OVER

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.apples_eaten = 0
        self.spawn_apple()
        self.game_speed = 8
        self.current_world = None

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            if self.current_world is None:
                self.draw_game()
            else:
                self.draw_custom_game()
            self.draw_game_over()
        elif self.state == GameState.STATISTICS:
            self.draw_statistics()
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        elif self.state == GameState.PAUSED:
            if self.current_world is None:
                self.draw_game()
            else:
                self.draw_custom_game()
            self.draw_pause()
        elif self.state == GameState.CREATE_WORLD:
            self.draw_create_world()
        elif self.state == GameState.WORLD_EDITOR:
            self.draw_editor()
        elif self.state == GameState.MY_WORLDS:
            self.draw_my_worlds()
        elif self.state == GameState.PLAYING_CUSTOM:
            self.draw_custom_game()

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

        if self.current_world is not None:
            hp_text = self.font_small.render(f"{self.t('hp')}: {self.snake_current_hp}/{self.snake_max_hp}", True, COLOR_TEXT)
            hp_rect = hp_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(hp_text, hp_rect)

        restart_text = self.font_small.render(self.t("restart"), True, COLOR_TEXT)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
        self.screen.blit(restart_text, restart_rect)

    def draw_create_world(self):
        title = self.font_large.render(self.t("create_world"), True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)

        # Позиции для элементов в строку
        label_x = WINDOW_WIDTH // 2 - 210  # Метка слева
        hint_x = WINDOW_WIDTH // 2 + 130   # Подсказка справа
        base_y = 160
        gap = 60

        # Поля ввода с метками и подсказками
        fields = [
            (self.t("world_size"), self.world_size_input, "5-128"),
            (self.t("apple_count"), self.apple_count_input, "1-9999"),
            (self.t("snake_hp"), self.snake_hp_input, "1-20"),
        ]

        for i, (label, field, hint) in enumerate(fields):
            y = base_y + i * gap
            # Метка слева
            text = self.font_small.render(label + ":", True, COLOR_TEXT)
            self.screen.blit(text, (label_x, y + 5))
            # Поле ввода (уже задано в setup)
            field.draw(self.screen)
            # Подсказка справа
            hint_text = self.font_small.render(hint, True, (120, 120, 120))
            self.screen.blit(hint_text, (hint_x, y + 5))

        # Название мира
        y = base_y + 3 * gap
        text = self.font_small.render(self.t("world_name") + ":", True, COLOR_TEXT)
        self.screen.blit(text, (label_x, y + 5))
        self.world_name_input.draw(self.screen)

        # Ошибка дубликата
        if self.name_error:
            error_text = self.font_small.render(self.name_error, True, (255, 80, 80))
            self.screen.blit(error_text, (self.world_name_input.rect.x, self.world_name_input.rect.bottom + 5))

        self.create_world_create_btn.draw(self.screen)
        self.create_world_back_btn.draw(self.screen)

    def draw_editor(self):
        # Рисуем сетку мира
        grid_pixel_width = self.custom_grid_width * GRID_SIZE
        grid_pixel_height = self.custom_grid_height * GRID_SIZE
        offset_x = (WINDOW_WIDTH - grid_pixel_width) // 2
        offset_y = (WINDOW_HEIGHT - grid_pixel_height - 100) // 2

        # Фон поля
        field_rect = pygame.Rect(offset_x, offset_y, grid_pixel_width, grid_pixel_height)
        pygame.draw.rect(self.screen, (30, 30, 30), field_rect)

        # Сетка
        for x in range(self.custom_grid_width + 1):
            pygame.draw.line(self.screen, (60, 60, 60),
                           (offset_x + x * GRID_SIZE, offset_y),
                           (offset_x + x * GRID_SIZE, offset_y + grid_pixel_height))
        for y in range(self.custom_grid_height + 1):
            pygame.draw.line(self.screen, (60, 60, 60),
                           (offset_x, offset_y + y * GRID_SIZE),
                           (offset_x + grid_pixel_width, offset_y + y * GRID_SIZE))

        # Белые блоки
        for block in self.white_blocks:
            bx = offset_x + block[0] * GRID_SIZE + 1
            by = offset_y + block[1] * GRID_SIZE + 1
            pygame.draw.rect(self.screen, COLOR_WHITE_BLOCK, (bx, by, GRID_SIZE - 2, GRID_SIZE - 2))

        # Красные блоки
        for block in self.red_blocks:
            bx = offset_x + block[0] * GRID_SIZE + 1
            by = offset_y + block[1] * GRID_SIZE + 1
            pygame.draw.rect(self.screen, COLOR_RED_BLOCK, (bx, by, GRID_SIZE - 2, GRID_SIZE - 2))

        # Хотбар
        self.draw_hotbar()

        # Кнопки
        self.editor_save_btn.draw(self.screen)
        self.editor_back_btn.draw(self.screen)
        self.editor_info_btn.draw(self.screen)

        # Информационная панель
        if self.show_block_info:
            self.draw_block_info()

    def draw_block_info(self):
        # Полупрозрачный фон
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Окно информации
        info_width, info_height = 560, 250
        info_x = (WINDOW_WIDTH - info_width) // 2
        info_y = (WINDOW_HEIGHT - info_height) // 2
        info_rect = pygame.Rect(info_x, info_y, info_width, info_height)
        pygame.draw.rect(self.screen, COLOR_SETTINGS_BG, info_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BUTTON_BORDER, info_rect, 2, border_radius=10)

        # Заголовок
        title = self.font_medium.render(self.t("block_info_title"), True, COLOR_TEXT)
        self.screen.blit(title, (info_x + 20, info_y + 15))

        # Информация о блоках
        y = info_y + 65
        blocks_info = [
            (COLOR_WHITE_BLOCK, self.t("block_info_white")),
            (COLOR_RED_BLOCK, self.t("block_info_red")),
            ((100, 100, 100), self.t("block_info_erase")),
        ]

        info_font = pygame.font.Font(None, 22)
        for color, text in blocks_info:
            # Цветной квадрат
            pygame.draw.rect(self.screen, color, (info_x + 20, y, 20, 20))
            # Текст с переносом если не влезает
            max_width = info_width - 60
            words = text.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test = current_line + word + " "
                if info_font.size(test)[0] <= max_width:
                    current_line = test
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())

            line_y = y
            for line in lines:
                label = info_font.render(line, True, COLOR_TEXT)
                self.screen.blit(label, (info_x + 50, line_y))
                line_y += 22
            y = line_y + 10

        # Кнопка закрытия
        close_btn = Button(info_x + info_width - 110, info_y + info_height - 45, 90, 35, self.t("close"), font_size=20)
        close_btn.draw(self.screen)
        # Обработка клика по кнопке закрытия
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if close_btn.rect.collidepoint(mouse_pos):
                self.show_block_info = False
                pygame.time.delay(150)

    def draw_hotbar(self):
        # Фон хотбара
        hotbar_rect = pygame.Rect(0, WINDOW_HEIGHT - 80, WINDOW_WIDTH, 80)
        pygame.draw.rect(self.screen, COLOR_HOTBAR, hotbar_rect)

        for slot in self.hotbar_slots:
            rect = slot["rect"]
            if self.selected_tool == slot["type"]:
                pygame.draw.rect(self.screen, COLOR_HOTBAR_SELECTED, rect.inflate(4, 4), border_radius=6)
            pygame.draw.rect(self.screen, slot["color"], rect, border_radius=4)
            pygame.draw.rect(self.screen, COLOR_BUTTON_BORDER, rect, 2, border_radius=4)

    def draw_my_worlds(self):
        title = self.font_large.render(self.t("my_worlds"), True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        worlds = self.data_manager.get_worlds()
        if not worlds:
            no_data = self.font_medium.render(self.t("no_worlds"), True, COLOR_TEXT)
            no_data_rect = no_data.get_rect(center=(WINDOW_WIDTH // 2, 250))
            self.screen.blit(no_data, no_data_rect)
        else:
            for item in self.world_buttons:
                item["btn"].draw(self.screen)
                item["edit_btn"].draw(self.screen)
                item["delete_btn"].draw(self.screen)

        self.my_worlds_back_btn.draw(self.screen)

    def draw_custom_game(self):
        # Рисуем кастомный мир
        grid_pixel_width = self.custom_grid_width * GRID_SIZE
        grid_pixel_height = self.custom_grid_height * GRID_SIZE
        offset_x = (WINDOW_WIDTH - grid_pixel_width) // 2
        offset_y = (WINDOW_HEIGHT - grid_pixel_height - 50) // 2

        # Фон поля
        field_rect = pygame.Rect(offset_x, offset_y, grid_pixel_width, grid_pixel_height)
        pygame.draw.rect(self.screen, (30, 30, 30), field_rect)

        # Сетка
        for x in range(self.custom_grid_width + 1):
            pygame.draw.line(self.screen, (60, 60, 60),
                           (offset_x + x * GRID_SIZE, offset_y),
                           (offset_x + x * GRID_SIZE, offset_y + grid_pixel_height))
        for y in range(self.custom_grid_height + 1):
            pygame.draw.line(self.screen, (60, 60, 60),
                           (offset_x, offset_y + y * GRID_SIZE),
                           (offset_x + grid_pixel_width, offset_y + y * GRID_SIZE))

        # Белые блоки
        for block in self.white_blocks:
            bx = offset_x + block[0] * GRID_SIZE + 1
            by = offset_y + block[1] * GRID_SIZE + 1
            pygame.draw.rect(self.screen, COLOR_WHITE_BLOCK, (bx, by, GRID_SIZE - 2, GRID_SIZE - 2))

        # Красные блоки
        for block in self.red_blocks:
            bx = offset_x + block[0] * GRID_SIZE + 1
            by = offset_y + block[1] * GRID_SIZE + 1
            pygame.draw.rect(self.screen, COLOR_RED_BLOCK, (bx, by, GRID_SIZE - 2, GRID_SIZE - 2))

        # Яблоки
        for apple in getattr(self, "apples", []):
            ax = offset_x + apple[0] * GRID_SIZE + 2
            ay = offset_y + apple[1] * GRID_SIZE + 2
            pygame.draw.rect(self.screen, COLOR_APPLE, (ax, ay, GRID_SIZE - 4, GRID_SIZE - 4), border_radius=4)

        # Змейка
        for i, segment in enumerate(self.snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
            sx = offset_x + segment[0] * GRID_SIZE + 1
            sy = offset_y + segment[1] * GRID_SIZE + 1
            pygame.draw.rect(self.screen, color, (sx, sy, GRID_SIZE - 2, GRID_SIZE - 2), border_radius=3)

        # Счёт и HP
        score_text = self.font_small.render(f"{self.t('score')}: {self.apples_eaten}", True, COLOR_TEXT)
        self.screen.blit(score_text, (10, 10))

        hp_text = self.font_small.render(f"{self.t('hp')}: {self.snake_current_hp}/{self.snake_max_hp}", True, COLOR_TEXT)
        self.screen.blit(hp_text, (WINDOW_WIDTH - 150, 10))

    def draw_statistics(self):
        title = self.font_large.render(self.t("statistics"), True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)

        stats = self.data_manager.get_stats()

        # Обычная игра
        y = 120
        classic_title = self.font_medium.render(self.t("classic_stats"), True, COLOR_TEXT)
        self.screen.blit(classic_title, (WINDOW_WIDTH // 2 - 150, y))
        y += 40

        if stats["games_played"] == 0:
            no_data = self.font_small.render(self.t("no_data"), True, COLOR_TEXT)
            self.screen.blit(no_data, (WINDOW_WIDTH // 2 - 150, y))
            y += 50
        else:
            lines = [
                f"{self.t('games_played')}: {stats['games_played']}",
                f"{self.t('avg_apples')}: {stats['avg_apples']:.1f}",
                f"{self.t('max_apples')}: {stats['max_apples']}",
            ]
            for line in lines:
                text = self.font_small.render(line, True, COLOR_TEXT)
                self.screen.blit(text, (WINDOW_WIDTH // 2 - 150, y))
                y += 30

        # Кастомные миры
        y += 20
        custom_title = self.font_medium.render(self.t("custom_stats"), True, COLOR_TEXT)
        self.screen.blit(custom_title, (WINDOW_WIDTH // 2 - 150, y))
        y += 40

        if stats["custom_games_played"] == 0:
            no_data = self.font_small.render(self.t("no_data"), True, COLOR_TEXT)
            self.screen.blit(no_data, (WINDOW_WIDTH // 2 - 150, y))
        else:
            lines = [
                f"{self.t('games_played')}: {stats['custom_games_played']}",
                f"{self.t('avg_apples')}: {stats['custom_avg_apples']:.1f}",
                f"{self.t('max_apples')}: {stats['custom_max_apples']}",
            ]
            for line in lines:
                text = self.font_small.render(line, True, COLOR_TEXT)
                self.screen.blit(text, (WINDOW_WIDTH // 2 - 150, y))
                y += 30

        self.stats_back_button.draw(self.screen)

    def draw_settings(self):
        title = self.font_large.render(self.t("settings_title"), True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        lang_label = self.font_medium.render(self.t("language") + ":", True, COLOR_TEXT)
        lang_rect = lang_label.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(lang_label, lang_rect)

        # Подсветка выбранного языка
        lang = self.data_manager.get_language()
        active_btn = None
        if lang == "ru":
            active_btn = self.lang_ru_button
        elif lang == "en":
            active_btn = self.lang_en_button
        elif lang == "zh":
            active_btn = self.lang_zh_button
        elif lang == "de":
            active_btn = self.lang_de_button

        if active_btn:
            active_btn.rect.inflate_ip(4, 4)

        self.lang_ru_button.draw(self.screen)
        self.lang_en_button.draw(self.screen)
        self.lang_zh_button.draw(self.screen)
        self.lang_de_button.draw(self.screen)

        # Возвращаем размеры обратно
        if active_btn:
            active_btn.rect.inflate_ip(-4, -4)

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
