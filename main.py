from src.settings import *

from src.core.level import Level
from src.core.overworld import Overworld
from src.core.data import Data
from src.core.ui import UI
from src.core.support import (
    import_image, 
    import_folder,
    import_folder_dict,
    import_sub_folders,
)


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        pygame.display.set_caption('Game2D')
        
        # Set the display mode first
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Load the TMX map after setting the display mode
        self.tmx_maps = {
            0: load_pygame(join(LEVELS_DIR, 'omni.tmx')),
            1: load_pygame(join(LEVELS_DIR, '1.tmx')),
			2: load_pygame(join(LEVELS_DIR, '2.tmx')),
			3: load_pygame(join(LEVELS_DIR, '3.tmx')),
			4: load_pygame(join(LEVELS_DIR, '4.tmx')),
			5: load_pygame(join(LEVELS_DIR, '5.tmx')),
            6: load_pygame(join(LEVELS_DIR, '6.tmx')),
        }

        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)

        self.tmx_overworld = load_pygame(join(OVERWORLD_DIR, 'overworld.tmx'))

        self.current_stage = Level(
            self.tmx_maps[self.data.current_level],
            self.level_frames, self.audio_files, 
            self.data, self.switch_stage
        )
        self.bg_music.play(-1)
    
    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.current_stage = Level(
                self.tmx_maps[self.data.current_level], 
                self.level_frames, self.audio_files, 
                self.data, self.switch_stage
            )

        else: # overworld 
            if unlock > 0:
                self.data.unlocked_level = 6
            else:
                self.data.health -= 1
                self.current_stage = Overworld(
                    self.tmx_overworld, self.data, 
                    self.overworld_frames, self.switch_stage
                )
                  
    def import_assets(self):
        self.level_frames = {
			'flag': import_folder(GRAPHICS_DIR, 'level', 'flag'),
			'saw': import_folder(GRAPHICS_DIR, 'enemies', 'saw', 'animation'),
			'floor_spike': import_folder(GRAPHICS_DIR,'enemies', 'floor_spikes'),
			'palms': import_sub_folders(GRAPHICS_DIR, 'level', 'palms'),
			'candle': import_folder(GRAPHICS_DIR, 'level', 'candle'),
			'window': import_folder(GRAPHICS_DIR, 'level', 'window'),
			'big_chain': import_folder(GRAPHICS_DIR, 'level', 'big_chains'),
			'small_chain': import_folder(GRAPHICS_DIR, 'level', 'small_chains'),
			'candle_light': import_folder(GRAPHICS_DIR, 'level', 'candle light'),
			'player': import_sub_folders(GRAPHICS_DIR,'player'),
			'saw': import_folder(GRAPHICS_DIR, 'enemies', 'saw', 'animation'),
			'saw_chain': import_image(GRAPHICS_DIR, 'enemies', 'saw', 'saw_chain'),
			'helicopter': import_folder(GRAPHICS_DIR, 'level', 'helicopter'),
			'boat': import_folder(GRAPHICS_DIR, 'objects', 'boat'),
			'spike': import_image(GRAPHICS_DIR, 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image(GRAPHICS_DIR, 'enemies', 'spike_ball', 'spiked_chain'),
			'tooth': import_folder(GRAPHICS_DIR,'enemies', 'tooth', 'run'),
			'shell': import_sub_folders(GRAPHICS_DIR,'enemies', 'shell'),
			'pearl': import_image(GRAPHICS_DIR, 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders(GRAPHICS_DIR, 'items'),
			'particle': import_folder(GRAPHICS_DIR, 'effects', 'particle'),
			'water_top': import_folder(GRAPHICS_DIR, 'level', 'water', 'top'),
			'water_body': import_image(GRAPHICS_DIR, 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict(GRAPHICS_DIR, 'level', 'bg', 'tiles'),
			'cloud_small': import_folder(GRAPHICS_DIR,'level', 'clouds', 'small'),
			'cloud_large': import_image(GRAPHICS_DIR,'level', 'clouds', 'large_cloud'),
		}
        self.font = pygame.font.Font(join(GRAPHICS_DIR, 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
			'heart': import_folder(GRAPHICS_DIR, 'ui', 'heart'), 
			'coin':import_image(GRAPHICS_DIR, 'ui', 'coin')
		}
        self.overworld_frames = {
			'palms': import_folder(GRAPHICS_DIR, 'overworld', 'palm'),
			'water': import_folder(GRAPHICS_DIR, 'overworld', 'water'),
			'path': import_folder_dict(GRAPHICS_DIR, 'overworld', 'path'),
			'icon': import_sub_folders(GRAPHICS_DIR, 'overworld', 'icon'),
		}
        self.audio_files = {
			'coin': pygame.mixer.Sound(join(AUDIO_DIR, 'coin.wav')),
			'attack': pygame.mixer.Sound(join(AUDIO_DIR, 'attack.wav')),
			'jump': pygame.mixer.Sound(join(AUDIO_DIR, 'jump.wav')), 
			'damage': pygame.mixer.Sound(join(AUDIO_DIR, 'damage.wav')),
			'pearl': pygame.mixer.Sound(join(AUDIO_DIR, 'pearl.wav')),
		}
        self.bg_music = pygame.mixer.Sound(join(AUDIO_DIR, 'starlight_city.mp3'))
        self.bg_music.set_volume(0.5)

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            System.exit()
    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    System.exit()
            
            self.check_game_over()
            self.current_stage.run(dt)
            self.ui.update(dt)
            
            pygame.display.update()


if __name__ == '__main__':
    Game().run()