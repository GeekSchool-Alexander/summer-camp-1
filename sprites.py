import pygame as pg
from VectorClass import Vec2d
from settings import *


class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface(PLAYER_SIZE)
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDHT/2, HEIGHT/2)
		self.pos = Vec2d(self.rect.center)
		
	def update(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.pos.x -= 5
		if keys[pg.K_RIGHT]:
			self.pos.x += 5
		
		self.rect.center = self.pos