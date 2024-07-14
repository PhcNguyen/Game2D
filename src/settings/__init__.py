import pygame

from os import walk
from os.path import join
from pathlib import Path
from pygame.math import Vector2 as vector

from src.pytmx.util_pygame import load_pygame
from src.system import System



BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = join(BASE_DIR, 'assets')
GRAPHICS_DIR = join(BASE_DIR, 'graphics')

LEVELS_DIR = join(ASSETS_DIR, 'levels')
TILESETS_DIR = join(ASSETS_DIR, 'tilesets')
OVERWORLD_DIR = join(ASSETS_DIR, 'overworld')
AUDIO_DIR = join(ASSETS_DIR, 'audio')


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6

#Players

Z_LAYERS = {
	'bg': 0,
	'clouds': 1,
	'bg tiles': 2,
	'path': 3,
	'bg details': 4,
	'main': 5,
	'water': 6,
	'fg': 7
}