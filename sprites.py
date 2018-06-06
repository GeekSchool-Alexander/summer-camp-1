import pygame as pg
from VectorClass import Vec2d
from settings import *


class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface(PLAYER_SIZE)
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDHT/2, 0)
		self.pos = Vec2d(self.rect.center)
		self.vel = Vec2d(0, 0)
		self.acc = Vec2d(0, 0)
		
	def update(self):
		self.acc.x = 0
		self.acc.y = 0.1
		
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_RIGHT]:
			self.acc.x = PLAYER_ACC
	
		self.acc.x += PLAYER_FRICTION * self.vel.x
		self.vel += self.acc
		self.pos += self.vel + self.acc / 2

		if self.pos.x + PLAYER_WIDTH / 2 > WIDHT:
			self.pos.x = WIDHT - PLAYER_WIDTH / 2
		if self.pos.x - PLAYER_WIDTH / 2 < 0:
			self.pos.x = PLAYER_WIDTH / 2
		self.rect.center = self.pos

class Platform(pg.sprite.Sprite):
	def __init__(self, x, y, w, h):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((w, h))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y