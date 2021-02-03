import pygame as pg
import pytmx
from settings import *


def collide_hit_rect(one, two):
    """ Collision function used by 'wall_collide' function in sprites.py
    """
    return one.hit_rect.colliderect(two.rect)


class TiledMap:
    """Class for creating 'Tiled' app map objects
    """
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        """Renders map to screen
        """
        ti = self.tmxdata.get_tile_image_by_gid
        t_wid = self.tmxdata.tilewidth
        t_hgt = self.tmxdata.tileheight
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * t_wid, y * t_hgt))
                        # surface.blit(
                        # pg.transform.scale2x(tile), (x * 32, y * 32))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        # return pg.transform.scale2x(temp_surface)
        return temp_surface


class Camera:
    """Class to create a 'camera' object that centers on the player as he
        moves around the map
        """
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """ Sets the entity to follow - (Player)
        """
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """ Centers camera over map screen
        """
        return rect.move(self.camera.topleft)

    def update(self, target):
        # Calculates camera offset
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)   # left
        y = min(0, y)   # top
        x = max(-(self.width - WIDTH), x)   # right
        y = max(-(self.height - HEIGHT), y)   # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

