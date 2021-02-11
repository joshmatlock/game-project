import pygame as pg
from os import path
from settings import *
from random import choice, random
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

        """self.walk_bk = [
            self.game.spidersheet.get_image(0, 167, 42, 42),
            self.game.spidersheet.get_image(0, 209, 41, 40),
            self.game.spidersheet.get_image(0, 249, 42, 42),
            self.game.spidersheet.get_image(0, 291, 42, 42),
            self.game.spidersheet.get_image(0, 333, 41, 40),
            self.game.spidersheet.get_image(0, 373, 42, 42)]
        for frame in self.walk_bk:
            frame.set_colorkey(BLACK)"""

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
        # for event in pg.KEYDOWN == pg.K_RSHIFT or pg.KEYDOWN == pg.K_LSHIFT:
        if keys[pg.K_SPACE]:
            snd = self.game.atk_snds
            if snd.get_num_channels() > 2:
                now = pg.time.get_ticks()
                if now - self.last_update > 180:
                    self.last_update = now
                    snd.stop()
                    snd.play()
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
        self.anim()
        # self.atk_anim()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        wall_collide(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        wall_collide(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def anim(self):
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
            if now - self.last_update > 100:
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
                        self.game.atk_snds.play()
                        self.image = self.atk_fr[self.current_frame]
                elif self.vel.y < 0:
                    self.image = self.walk_bk[self.current_frame]
                    if keys[pg.K_SPACE]:
                        self.image = self.atk_bk[self.current_frame]

        if not self.walking and self.attacking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.standing)
                if self.image == self.stand_fr or self.image in self.walk_fr:
                    self.image = self.atk_fr[self.current_frame]
                elif self.image == self.stand_bk or self.image in self.walk_bk:
                    self.image = self.atk_bk[self.current_frame]
                elif self.image == self.stand_lt or self.image in self.walk_lt:
                    self.image = self.atk_lt[self.current_frame]
                elif self.image == self.stand_rt or self.image in self.walk_rt:
                    self.image = self.atk_rt[self.current_frame]


# noinspection PyAttributeOutsideInit
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

    def load_move(self):
        """ Loads movement frames for animation from 'spidersheet.png':
        Frame 1: Standing
        Frames 1-4: Attacking
        Frames 5-10: Walking
        """
        self.stand_fr = self.game.spidersheet.get_image(125, 150, 42, 41)
        self.stand_bk = self.game.spidersheet.get_image(0, 191, 42, 42)
        self.stand_lt = self.game.spidersheet.get_image(68, 0, 36, 36)
        self.stand_rt = self.game.spidersheet.get_image(35, 36, 35, 36)
        self.standing = [
            self.stand_fr, self.stand_bk, self.stand_lt, self.stand_rt
        ]
        for frame in self.standing:
            frame.set_colorkey(BLACK)

        self.walk_fr = [
            self.game.spidersheet.get_image(162, 110, 41, 40),
            self.game.spidersheet.get_image(126, 233, 41, 42),
            self.game.spidersheet.get_image(203, 110, 41, 40),
            self.game.spidersheet.get_image(0, 150, 41, 40),
            self.game.spidersheet.get_image(167, 233, 41, 42),
            self.game.spidersheet.get_image(121, 110, 41, 40)
        ]
        for frame in self.walk_fr:
            frame.set_colorkey(BLACK)

        self.walk_bk = [
            self.game.spidersheet.get_image(168, 191, 42, 42),
            self.game.spidersheet.get_image(39, 110, 41, 40),
            self.game.spidersheet.get_image(210, 191, 42, 42),
            self.game.spidersheet.get_image(0, 233, 42, 42),
            self.game.spidersheet.get_image(80, 110, 41, 40),
            self.game.spidersheet.get_image(42, 191, 42, 42)
        ]
        for frame in self.walk_bk:
            frame.set_colorkey(BLACK)

        self.walk_lt = [
            self.game.spidersheet.get_image(176, 0, 35, 36),
            self.game.spidersheet.get_image(0, 72, 38, 37),
            self.game.spidersheet.get_image(211, 0, 35, 36),
            self.game.spidersheet.get_image(0, 36, 35, 36),
            self.game.spidersheet.get_image(153, 72, 39, 38),
            self.game.spidersheet.get_image(104, 0, 36, 36)
        ]
        for frame in self.walk_lt:
            frame.set_colorkey(BLACK)

        self.walk_rt = [
            self.game.spidersheet.get_image(141, 36, 36, 36),
            self.game.spidersheet.get_image(0, 110, 39, 38),
            self.game.spidersheet.get_image(177, 36, 35, 36),
            self.game.spidersheet.get_image(212, 36, 35, 36),
            self.game.spidersheet.get_image(38, 72, 38, 37),
            self.game.spidersheet.get_image(70, 36, 35, 36)
        ]
        for frame in self.walk_rt:
            frame.set_colorkey(BLACK)

        self.dead = [
            self.game.spidersheet.get_image(83, 150, 42, 41),
            self.game.spidersheet.get_image(76, 72, 38, 38),
            self.game.spidersheet.get_image(34, 0, 34, 34),
            self.game.spidersheet.get_image(0, 0, 34, 33)
        ]

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS ** 2:
            if random() < 0.002:
                choice(self.game.mob_snds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += (
                    self.vel * self.game.dt + 0.5 * self.acc * self.game.dt**2)
            self.hit_rect.centerx = self.pos.x
            wall_collide(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            wall_collide(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.mob_hit_snds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class FallsBtm(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load()
        self.image = self.game.watersheet_b.get_image(0, 0, 32, 32)
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.hit_rect = WATER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.current_frame = 0
        self.last_update = 0
        self.flowing = True

    # noinspection PyAttributeOutsideInit
    def load(self):
        self.falls_b = [
            self.game.watersheet_b.get_image(0, 0, 32, 32),
            self.game.watersheet_b.get_image(32, 0, 32, 32),
            self.game.watersheet_b.get_image(64, 0, 32, 32),
            self.game.watersheet_b.get_image(96, 0, 32, 32)]
        for frame in self.falls_b:
            # frame = pg.transform.scale(frame, (TILESIZE, TILESIZE))
            frame.set_colorkey(BLACK)

    def anim(self):
        now = pg.time.get_ticks()
        if self.flowing:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.falls_b)
                self.image = self.falls_b[self.current_frame]
                self.image = pg.transform.scale(self.image, (32, 32))

    def update(self):
        self.anim()


class FallsTop(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load()
        self.image = self.game.watersheet_t.get_image(0, 0, 32, 32)
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.hit_rect = WATER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.current_frame = 0
        self.last_update = 0
        self.flowing = True

    def load(self):
        self.falls_t = [
            self.game.watersheet_t.get_image(0, 0, 32, 32),
            self.game.watersheet_t.get_image(32, 0, 32, 32),
            self.game.watersheet_t.get_image(64, 0, 32, 32),
            self.game.watersheet_t.get_image(96, 0, 32, 32)]
        for frame in self.falls_t:
            # frame = pg.transform.scale(frame, (TILESIZE, TILESIZE))
            frame.set_colorkey(BLACK)

    def anim(self):
        now = pg.time.get_ticks()
        if self.flowing:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.falls_t)
                self.image = self.falls_t[self.current_frame]
                self.image = pg.transform.scale(self.image, (32, 32))

    def update(self):
        self.anim()


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
