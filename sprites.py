import pygame as pg
from VectorClass import Vec2d
from settings import *


class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load("./images/ball.png")
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.pos = Vec2d(self.rect.center)
		self.vel = Vec2d(0, 0)
		self.acc = Vec2d(0, 0)
		self.game = game
		
	def update(self):
		self.acc.x = 0
		self.acc.y = GRAVITY
		
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_RIGHT]:
			self.acc.x = PLAYER_ACC
		if keys[pg.K_UP]:
			self.jump()
	
		self.acc.x += PLAYER_FRICTION * self.vel.x
		self.vel += self.acc
		self.pos += self.vel + self.acc / 2

		if self.pos.x + PLAYER_WIDTH / 2 > WIDHT:
			self.pos.x = WIDHT - PLAYER_WIDTH / 2
		if self.pos.x - PLAYER_WIDTH / 2 < 0:
			self.pos.x = PLAYER_WIDTH / 2
		if self.pos.y - PLAYER_HEIGHT < 0:
			self.pos.y = PLAYER_HEIGHT
			self.vel.y = 0
		
		self.rect.midbottom = self.pos

	def jump(self):
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:
			self.vel.y = -5
		
		
class Platform(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load("./images/platform.png")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y