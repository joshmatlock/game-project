""" Tilemap game """

import sys
from sprites import *
from tilemap import *


class Game:
    """ initialize pygame and create game window
    """
    def __init__(self):
        pg.init()
        # pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        # self.running = True
        # self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    # noinspection PyShadowingNames,PyAttributeOutsideInit
    def load_data(self):
        """ Load game images and sounds
        """
        game_dir = path.dirname(__file__)
        img_dir = path.join(game_dir, 'img')
        music_dir = path.join(game_dir, 'music')
        map_dir = path.join(game_dir, 'maps')

        self.map = TiledMap(path.join(map_dir, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(
            path.join(img_dir, PLAYER_IMG)).convert_alpha()

        # Load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.watersheet_b = Spritesheet(path.join(img_dir, WATERSHEET_B))
        self.watersheet_t = Spritesheet(path.join(img_dir, WATERSHEET_T))

        # Load sound
        pg.mixer.music.load(path.join(music_dir, BG_MUSIC))

    # noinspection PyAttributeOutsideInit
    def new(self):
        """ Initialize all variables and do all setup for a new game
        """
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.water = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            t_obj = tile_object
            obj_list = ['wall', 'cliff', 'border',
                        'tree', 'falls_b', 'falls_t']

            if t_obj.name == 'Player':
                self.player = Player(self, t_obj.x, t_obj.y)

            if t_obj.name == 'falls_b':
                FallsBtm(self, t_obj.x, t_obj.y, t_obj.width, t_obj.height)

            if t_obj.name == 'falls_t':
                FallsTop(self, t_obj.x, t_obj.y, t_obj.width, t_obj.height)

            for i in obj_list:
                if t_obj.name == i in obj_list:
                    Obstacle(
                        self, t_obj.x, t_obj.y, t_obj.width, t_obj.height)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    # noinspection PyAttributeOutsideInit
    def run(self):
        """ Game loop - set self.playing = False to end the game
        """
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        """ Update portion of the game loop
        """
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        """ Draws background grid
        """
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        """ Draws images to the screen
        """
        # Framerate display
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR) # Older code

        # Apply camera
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid() # Older code

        # Draws sprites to screen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(
                    self.screen, CYAN, self.camera.apply_rect(
                        sprite.hit_rect), 1)

        # Display for hit rect debug - 'h' key to toggle in game
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(
                    self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)
        pg.display.flip()

    def events(self):
        """ Catch all events here
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# Create game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()

# pg.quit()
