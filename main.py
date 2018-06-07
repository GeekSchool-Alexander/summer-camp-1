import pygame as pg
from settings import *
from sprites import *


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
		for plat in PLATFORM_LIST:
			p = Platform(*plat)
			self.all_sprites.add(p)
			self.platforms.add(p)
		self.player = Player(self)
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