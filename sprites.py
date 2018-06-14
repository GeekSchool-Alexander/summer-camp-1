import pygame as pg

from VectorClass import Vec2d
from settings import *


class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		pg.sprite.Sprite.__init__(self)
		self.frames = (pg.image.load("./images/ball.png"),
		            pg.image.load("./images/ball2.png"),
		            pg.image.load("./images/ball3.png"),
		            pg.image.load("./images/ball4.png"),
		            pg.image.load("./images/ball5.png"),
		            pg.image.load("./images/ball6.png"),
		            pg.image.load("./images/ball7.png") )
		self.current_frame = 0
		self.image = self.frames[self.current_frame]
		self.last_update = pg.time.get_ticks()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.pos = Vec2d(self.rect.center)
		self.vel = Vec2d(0, 0)
		self.acc = Vec2d(0, 0)
		self.game = game
		self.on_ground = False
	
	def update(self):
		
		self.acc.x = 0
		self.acc.y = GRAVITY
		
		keys = pg.key.get_pressed()
		self.moving = ""
		if keys[pg.K_LEFT]:
			self.acc.x = -PLAYER_ACC
			self.moving = "left"
		if keys[pg.K_RIGHT]:
			self.acc.x = PLAYER_ACC
			self.moving = "right"
		if keys[pg.K_UP]:
			self.jump()
		
		#
		self.acc.x += PLAYER_FRICTION * self.vel.x
		self.vel += self.acc
		self.pos += self.vel + self.acc / 2
		self.rect.midbottom = self.pos
		
		# processing with
		if self.pos.x + PLAYER_WIDTH / 2 > WIDHT:
			self.pos.x = WIDHT - PLAYER_WIDTH / 2
		if self.pos.x - PLAYER_WIDTH / 2 < 0:
			self.pos.x = PLAYER_WIDTH / 2
		if self.pos.y - PLAYER_HEIGHT < 0:
			self.pos.y = PLAYER_HEIGHT
			self.vel.y = 0
		
		# animation
		self.animate()
		
		# collide processing
		self.on_ground = False
		empty_spaces = 1
		for platform in self.game.platforms:
			sides = {
				"top": pg.Rect(platform.rect.left + empty_spaces, platform.rect.top, PLATFORM_WIDTH - empty_spaces * 2,
				               1), "bottom": pg.Rect(platform.rect.left + empty_spaces, platform.rect.bottom,
				                                     PLATFORM_WIDTH - empty_spaces * 2, 1),
				"left": pg.Rect(platform.rect.left, platform.rect.top + empty_spaces, 1,
				                PLATFORM_HEIGHT - empty_spaces * 2),
				"right": pg.Rect(platform.rect.right, platform.rect.top + empty_spaces, 1,
				                 PLATFORM_HEIGHT - empty_spaces * 2)}
			collisions = set()
			for side, plat_rect in sides.items():
				if self.rect.colliderect(plat_rect):
					collisions.add(side)
			
			if platform.rect.top < self.rect.centery < platform.rect.bottom:
				if "left" in collisions:
					self.vel.x = 0
					self.pos.x = sides["left"].left - PLAYER_WIDTH / 2
				if "right" in collisions:
					self.vel.x = 0
					self.pos.x = sides["right"].right + PLAYER_WIDTH / 2
			else:
				if "top" in collisions:
					self.vel.y = 0
					self.pos.y = sides["top"].top
					self.on_ground = True
				elif "bottom" in collisions:
					self.vel.y = 0
					self.pos.y = sides["bottom"].bottom + PLAYER_HEIGHT
	
	def jump(self):
		if self.on_ground:
			self.vel.y = -5

	def animate(self):
		now = pg.time.get_ticks()
		if self.moving:
			if now - self.last_update >= 100:
				self.last_update = now
				if self.moving == "left":
					self.current_frame -= 1
					if self.current_frame < 0:
						self.current_frame = len(self.frames)-1
				elif self.moving == "right":
					self.current_frame += 1
					if self.current_frame >= len(self.frames):
						self.current_frame = 0
				self.image = self.frames[self.current_frame]
				
				
class Platform(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load("./images/platform.png")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
class Saw(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.frames = (pg.image.load("./images/saw1.png"),
		               pg.image.load("./images/saw2.png"),
		               pg.image.load("./images/saw3.png"),
		               pg.image.load("./images/saw4.png"))
		self.current_frame = 0
		self.image = self.frames[self.current_frame]
		self.last_update = pg.time.get_ticks()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def update(self):
		self.animate()
		
	def animate(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 30:
			self.last_update = now
			self.current_frame += 1
			if self.current_frame == len(self.frames):
				self.current_frame = 0
			self.image = self.frames[self.current_frame]
