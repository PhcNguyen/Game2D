import pygame
from pygame.time import get_ticks
from pygame.math import Vector2 as vector

from random import (
    uniform, choice,
    randint
)

from os import walk
from os.path import join
from pathlib import Path
from math import sin, cos, radians

from src.pytmx.util_pygame import load_pygame
from src.system import System

# Xác định thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Xác định các thư mục con chứa tài nguyên (assets), đồ họa (graphics)
ASSETS_DIR = join(BASE_DIR, 'assets')
GRAPHICS_DIR = join(BASE_DIR, 'graphics')

# Xác định các thư mục con chứa cấp độ (levels), bộ gạch (tilesets), bản đồ tổng thể (overworld), âm thanh (audio)
LEVELS_DIR = join(ASSETS_DIR, 'levels')
TILESETS_DIR = join(ASSETS_DIR, 'tilesets')
OVERWORLD_DIR = join(ASSETS_DIR, 'overworld')
AUDIO_DIR = join(ASSETS_DIR, 'audio')

# Thiết lập kích thước cửa sổ trò chơi và kích thước ô gạch
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6  # Tốc độ hoạt ảnh

# Xác định các lớp Z để sắp xếp thứ tự hiển thị các đối tượng trong trò chơi
Z_LAYERS = {
    'bg': 0,           # Lớp nền
    'clouds': 1,       # Lớp mây
    'bg tiles': 2,     # Lớp gạch nền
    'path': 3,         # Lớp đường đi
    'bg details': 4,   # Lớp chi tiết nền
    'main': 5,         # Lớp chính (nhân vật, đối tượng chính)
    'water': 6,        # Lớp nước
    'fg': 7            # Lớp trước (foreground)
}
