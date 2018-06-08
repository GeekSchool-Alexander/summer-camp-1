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
		self.running = True
	
	def new(self):
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		plt_conf, plr_conf = self.create_level(level1)
		for plt in plt_conf:
			p = Platform(*plt)
			self.all_sprites.add(p)
			self.platforms.add(p)
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
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
				self.player.pos.y = hits[0].rect.top
				self.player.vel.y = 0
			
		self.all_sprites.update()

	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		pg.display.flip()

	def create_level(self, lvl):
		x = y = 0
		config = []
		start = Vec2d(0, 0) ###
		for row in lvl:
			for cell in row:
				if cell == "o": ###
					start = Vec2d(x, y) ###
				if cell == "-":
					config.append((x, y))
				x += PLATFORM_WIDTH
			y += PLATFORM_HEIGHT
			x = 0
		return tuple(config), Vec2d(start) ###

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