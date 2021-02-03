import pygame as pg
from os import path
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


def wall_collide(sprite, group, direc):
    """ Sets up collisions for sprites and walls
    """
    if direc == 'x':
        hits = pg.sprite.spritecollide(
            sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if direc == 'y':
        hits = pg.sprite.spritecollide(
            sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Spritesheet:
    """ Utility class for loading and parsing spritesheets
    """
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale2x(image)
        # image = pg.transform.scale(image, (TILESIZE, TILESIZE))
        return image


class Player(pg.sprite.Sprite):
    """ Defines player class - sets up player movement and attack animations
        with corresponding keys
        """
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.attacking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_move()
        self.load_atk()
        self.image = self.standing[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)

    # noinspection PyAttributeOutsideInit
    def load_move(self):
        """ Loads movement frames for animation from 'char_anim.png'
        """
        self.stand_fr = self.game.spritesheet.get_image(0, 40, 15, 20)
        self.stand_bk = self.game.spritesheet.get_image(66, 20, 15, 20)
        self.stand_lt = self.game.spritesheet.get_image(60, 40, 13, 20)
        self.stand_rt = self.game.spritesheet.get_image(112, 40, 13, 20)
        self.standing = [
            self.stand_fr, self.stand_bk, self.stand_lt, self.stand_rt]
        for frame in self.standing:
            frame.set_colorkey(BLACK)

        self.walk_fr = [
            self.game.spritesheet.get_image(0, 40, 15, 20),
            self.game.spritesheet.get_image(15, 40, 15, 20),
            self.game.spritesheet.get_image(30, 40, 15, 20),
            self.game.spritesheet.get_image(45, 40, 15, 20)]
        for frame in self.walk_fr:
            frame.set_colorkey(BLACK)

        self.walk_bk = [
            self.game.spritesheet.get_image(66, 20, 15, 20),
            self.game.spritesheet.get_image(81, 20, 15, 20),
            self.game.spritesheet.get_image(96, 20, 15, 20),
            self.game.spritesheet.get_image(111, 20, 15, 20)]
        for frame in self.walk_bk:
            frame.set_colorkey(BLACK)

        self.walk_lt = [
            self.game.spritesheet.get_image(60, 40, 13, 20),
            self.game.spritesheet.get_image(73, 40, 13, 20),
            self.game.spritesheet.get_image(86, 40, 13, 20),
            self.game.spritesheet.get_image(99, 40, 13, 20)]
        for frame in self.walk_lt:
            frame.set_colorkey(BLACK)

        self.walk_rt = [
            self.game.spritesheet.get_image(112, 40, 13, 20),
            self.game.spritesheet.get_image(0, 60, 13, 20),
            self.game.spritesheet.get_image(13, 60, 13, 20),
            self.game.spritesheet.get_image(26, 60, 13, 20)]
        for frame in self.walk_rt:
            frame.set_colorkey(BLACK)

    # noinspection PyAttributeOutsideInit
    def load_atk(self):
        """Loads attack frames for animation from 'char_anim.png'
        """
        self.atk_fr = [
            self.game.spritesheet.get_image(64, 0, 16, 20),
            self.game.spritesheet.get_image(59, 60, 16, 22),
            self.game.spritesheet.get_image(88, 60, 16, 24),
            self.game.spritesheet.get_image(104, 60, 16, 24)]
        for frame in self.atk_fr:
            frame.set_colorkey(BLACK)

        self.atk_bk = [
            self.game.spritesheet.get_image(17, 0, 17, 20),
            self.game.spritesheet.get_image(0, 0, 17, 19),
            self.game.spritesheet.get_image(34, 0, 15, 20),
            self.game.spritesheet.get_image(49, 0, 15, 20)]
        for frame in self.atk_bk:
            frame.set_colorkey(BLACK)

        self.atk_lt = [
            self.game.spritesheet.get_image(75, 60, 13, 22),
            self.game.spritesheet.get_image(39, 60, 20, 21),
            self.game.spritesheet.get_image(80, 0, 18, 20),
            self.game.spritesheet.get_image(98, 0, 18, 20)]
        for frame in self.atk_lt:
            frame.set_colorkey(BLACK)

        self.atk_rt = [
            self.game.spritesheet.get_image(0, 20, 16, 20),
            self.game.spritesheet.get_image(16, 20, 20, 20),
            self.game.spritesheet.get_image(36, 20, 15, 20),
            self.game.spritesheet.get_image(51, 20, 15, 20)]
        for frame in self.atk_rt:
            frame.set_colorkey(BLACK)

    def get_keys(self):
        """Sets keys for movement and attack"""
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        # Attack keys
        # if pg.KEYDOWN == pg.K_RSHIFT or pg.KEYDOWN == pg.K_LSHIFT:
        if keys[pg.K_SPACE]:
            self.attacking = True
        else:
            self.attacking = False

        # Move keys
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # if self.vel.x != 0 and self.vel.y != 0:
            # self.vel *= 0.7071            # For diagonal movement

    def update(self):
        # self.atk_anim()
        self.get_keys()
        self.move_anim()
        # self.atk_anim()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        wall_collide(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        wall_collide(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def move_anim(self):
        """Performs movement and attack animations
        """
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()
        pg.key.set_repeat(500, 100)

        if self.vel.x != 0 or self.vel.y != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.walk_fr)
                if self.vel.x > 0:
                    self.image = self.walk_rt[self.current_frame]
                    if keys[pg.K_SPACE]:
                        self.image = self.atk_rt[self.current_frame]
                elif self.vel.x < 0:
                    self.image = self.walk_lt[self.current_frame]
                    if keys[pg.K_SPACE]:
                        self.image = self.atk_lt[self.current_frame]
                elif self.vel.y > 0:
                    self.image = self.walk_fr[self.current_frame]
                    if keys[pg.K_SPACE]:
                        self.image = self.atk_fr[self.current_frame]
                elif self.vel.y < 0:
                    self.image = self.walk_bk[self.current_frame]
                    if keys[pg.K_SPACE]:
                        self.image = self.atk_bk[self.current_frame]

        if not self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.standing)
                if self.image == self.stand_fr or self.image in self.walk_fr:
                    if self.attacking:
                        self.image = self.atk_fr[self.current_frame]
                elif self.image == self.stand_bk or self.image in self.walk_bk:
                    if self.attacking:
                        self.image = self.atk_bk[self.current_frame]
                elif self.image == self.stand_lt or self.image in self.walk_lt:
                    if self.attacking:
                        self.image = self.atk_lt[self.current_frame]
                elif self.image == self.stand_rt or self.image in self.walk_rt:
                    if self.attacking:
                        self.image = self.atk_rt[self.current_frame]


class Wall(pg.sprite.Sprite):
    """Class to create wall objects - Currently repleced by 'Obstacle' class
    """
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    """Class to create impassable objects
    """
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
