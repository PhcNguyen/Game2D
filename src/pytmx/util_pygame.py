import logging
from typing import Optional, Union, List

import src.pytmx
from src.pytmx.pytmx import ColorLike
import src.pytmx.pytmx

logger = logging.getLogger(__name__)

try:
    from pygame.transform import flip, rotate
    import pygame
except ImportError:
    logger.error("cannot import pygame (is it installed?)")
    raise

__all__ = ["load_pygame", "pygame_image_loader", "simplify", "build_rects"]


def handle_transformation(
    tile: pygame.Surface,
    flags: src.pytmx.pytmx.TileFlags,
) -> pygame.Surface:
    if flags.flipped_diagonally:
        tile = flip(rotate(tile, 270), True, False)
    if flags.flipped_horizontally or flags.flipped_vertically:
        tile = flip(tile, flags.flipped_horizontally, flags.flipped_vertically)
    return tile


def smart_convert(
    original: pygame.Surface,
    colorkey: Optional[ColorLike],
    pixelalpha: bool,
) -> pygame.Surface:
    # tiled set a colorkey
    if colorkey:
        tile = original.convert()
        tile.set_colorkey(colorkey, pygame.RLEACCEL)
        # TODO: if there is a colorkey, count the colorkey pixels to determine if RLEACCEL should be used

    # no colorkey, so use a mask to determine if there are transparent pixels
    else:
        tile_size = original.get_size()
        threshold = 254  # the default

        try:
            # count the number of pixels in the tile that are not transparent
            px = pygame.mask.from_surface(original, threshold).count()
        except:
            # pygame_sdl2 will fail because the mask module is not included
            # in this case, just convert_alpha and return it
            return original.convert_alpha()

        # there are no transparent pixels in the image
        if px == tile_size[0] * tile_size[1]:
            tile = original.convert()

        # there are transparent pixels, and set for perpixel alpha
        elif pixelalpha:
            tile = original.convert_alpha()

        # there are transparent pixels, and we won't handle them
        else:
            tile = original.convert()

    return tile


def pygame_image_loader(filename: str, colorkey: Optional[ColorLike], **kwargs):
    if colorkey:
        colorkey = pygame.Color("#{0}".format(colorkey))

    pixelalpha = kwargs.get("pixelalpha", True)
    image = pygame.image.load(filename)

    def load_image(rect=None, flags=None):
        if rect:
            try:
                tile = image.subsurface(rect)
            except ValueError:
                logger.error("Tile bounds outside bounds of tileset image")
                raise
        else:
            tile = image.copy()

        if flags:
            tile = handle_transformation(tile, flags)

        tile = smart_convert(tile, colorkey, pixelalpha)
        return tile

    return load_image


def load_pygame(
    filename: str,
    *args,
    **kwargs,
) -> src.pytmx.pytmx.TiledMap:
    kwargs["image_loader"] = pygame_image_loader
    return src.pytmx.pytmx.TiledMap(filename, *args, **kwargs)