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
		# setting the initial values of acceleration
		self.acc.x = 0
		self.acc.y = GRAVITY
		
		# processing of control keys
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
		
		# calculation of acceleration, speed, position
		self.acc.x += PLAYER_FRICTION * self.vel.x
		self.vel += self.acc
		self.pos += self.vel + self.acc / 2
		self.rect.midbottom = self.pos
		
		# processing of screen edges
		if self.pos.x + PLAYER_WIDTH / 2 > WIDHT:
			self.pos.x = WIDHT - PLAYER_WIDTH / 2
		if self.pos.x - PLAYER_WIDTH / 2 < 0:
			self.pos.x = PLAYER_WIDTH / 2
		if self.pos.y - PLAYER_HEIGHT < 0:
			self.pos.y = PLAYER_HEIGHT
			self.vel.y = 0
		
		# call animation function
		self.animate()
		
		# processing collisions
		self.collides()
	
	def jump(self):
		if self.on_ground:
			self.vel.y = -5

	def animate(self):
		now = pg.time.get_ticks()
		if self.moving:
			if now - self.last_update >= 75:
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
				
	def collides(self):
		self.on_ground = False
		empty_spaces = 4
		for platform in self.game.platforms:
			sides = {"top": pg.Rect(platform.rect.left + empty_spaces, platform.rect.top, PLATFORM_WIDTH - empty_spaces, 1),
				"bottom": pg.Rect(platform.rect.left + empty_spaces, platform.rect.bottom, PLATFORM_WIDTH - empty_spaces, 1),
				"right": pg.Rect(platform.rect.right, platform.rect.top + empty_spaces, 1, PLATFORM_HEIGHT - empty_spaces),
				"left": pg.Rect(platform.rect.left, platform.rect.top + empty_spaces, 1, PLATFORM_HEIGHT - empty_spaces)}
			collisions = set()
			for side, plat_rect in sides.items():
				if self.rect.colliderect(plat_rect):
					collisions.add(side)
			# collide processing
			if "top" in collisions:
				self.vel.y = 0
				self.pos.y = sides["top"].top
				self.on_ground = True
			if "bottom" in collisions:
				self.vel.y = 0
				self.pos.y = sides["bottom"].bottom + PLAYER_HEIGHT
			if "left" in collisions:
				self.vel.x = 0
				self.pos.x = sides["left"].left - PLAYER_WIDTH / 2
			if "right" in collisions:
				self.vel.x = 0
				self.pos.x = sides["right"].right + PLAYER_WIDTH / 2


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
		if now - self.last_update > 50:
			self.last_update = now
			self.current_frame += 1
			if self.current_frame == len(self.frames):
				self.current_frame = 0
			self.image = self.frames[self.current_frame]


class FlyingSaw(Saw):
	def __init__(self, game, x, y, direction):
		Saw.__init__(self, x, y)
		self.game = game
		if direction == "left":
			self.vel = Vec2d(-3, 0)
		elif direction == "right":
			self.vel = Vec2d(3, 0)
		elif direction == "top":
			self.vel = Vec2d(0, -3)
		elif direction == "bottom":
			self.vel = Vec2d(0, 3)
	
	def update(self):
		self.animate()
		
		# processing of screen edges
		if self.rect.right > WIDHT:
			self.vel = -self.vel
		elif self.rect.left < 0:
			self.vel = -self.vel
		elif self.rect.top < 0:
			self.vel = -self.vel
		elif self.rect.bottom > HEIGHT:
			self.vel = -self.vel
		
		self.collides()
		self.rect.x += self.vel.x
		self.rect.y += self.vel.y
		
	def collides(self):
		for platform in self.game.platforms:
			if self.rect.colliderect(platform.rect):
				self.vel = -self.vel


class Platform(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load("./images/platform.png")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
