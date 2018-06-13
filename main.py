import pygame as pg
from settings import *
from sprites import *
from levels import *


class Game:
	def __init__(self):
		pg.init()
		pg.display.set_caption("GeekSchool Platformer")
		self.screen = pg.display.set_mode(WINDOW_SIZE)
		self.clock = pg.time.Clock()
		self.background = pg.image.load("./images/background.jpg")
		self.running = True
	
	def new(self):
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.saws = pg.sprite.Group()
		plt_conf, plr_conf, saw_conf = self.create_level(level1)
		for plt in plt_conf:
			p = Platform(*plt)
			self.all_sprites.add(p)
			self.platforms.add(p)
		for saw  in saw_conf:
			if len(saw) == 2:
				s = Saw(*saw)
			else:
				s = FlyingSaw(self, *saw)
			self.all_sprites.add(s)
			self.saws.add(s)
		self.player = Player(self, plr_conf.x, plr_conf.y)
		self.all_sprites.add(self.player)
		self.run()
	
	def run(self):
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.event()
			self.update()
			self.draw()
	
	def event(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.running = False
				self.playing = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.running = False
					self.playing = False
	
	def update(self):
		self.all_sprites.update()
	
	def draw(self):
		self.screen.blit(self.background, (0, 0))
		self.all_sprites.draw(self.screen)
		pg.display.flip()
	
	def create_level(self, lvl):
		x = y = 0
		platforms_config = []
		player_start = Vec2d(0, 0)
		saws_config = []
		for row in lvl:
			for cell in row:
				if cell == "o":
					player_start = Vec2d(x, y)
				elif cell == "-":
					platforms_config.append((x, y))
				elif cell == "*":
					saws_config.append((x, y))
				elif cell == ">":
					saws_config.append((x, y, "right"))
				elif cell == "<":
					saws_config.append((x, y, "left"))
				elif cell == "^":
					saws_config.append((x, y, "top"))
				elif cell == "|":
					saws_config.append((x, y, "bottom"))
				
				x += PLATFORM_WIDTH
			y += PLATFORM_HEIGHT
			x = 0
		return tuple(platforms_config), player_start, tuple(saws_config)
	
	def __del__(self):
		pg.quit()
	
	def show_start_screen(self):
		pass
	
	def show_go_screen(self):
		pass


g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()