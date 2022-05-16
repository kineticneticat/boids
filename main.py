import math
import sys
import time

import pygame

pygame.init()

size = width, height = 500, 500
speed = [2, 2]
blue = 0, 0, 255

screen = pygame.display.set_mode(size)


class board:
	class boid:
		def __init__(self, x, y, v, goal):
			self.x = x
			self.y = y
			self.v = v
			self.theta = math.atan2(self.x - (self.v[0] + self.x), self.y - (self.v[1] + self.y)) * (180 / math.pi)
			# self.theta = -90 #target angle
			self.angle = 0  # current angle
			self.images = [pygame.image.load(f"images/boid{i}.png") for i in range(90)]
			self.image = None
			self.rotate()
			self.rect = self.image.get_rect()
			self.goal = goal

		def blit(self):
			self.rect.center = (self.x, self.y)
			screen.blit(self.images[self.angle], self.rect)

		def move(self):
			self.x += self.v[0]
			self.y += self.v[1]
			if self.x > 500:
				self.x = 0
			if self.y > 500:
				self.y = 0
			if self.x < 0:
				self.x = 500
			if self.y < 0:
				self.y = 500
			self.rotate()

		def rotate(self):
			self.theta = math.atan2(self.x - (self.v[0] + self.x), self.y - (self.v[1] + self.y)) * (180 / math.pi)
			self.angle = math.floor(self.theta)

		# if self.angle != self.theta:
		# 	# 	self.image = pygame.transform.rotate(self.image, self.theta)
		# 	# 	self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.x, self.y)).center)
			if self.theta>=0 and self.theta<90: self.image = self.images[self.theta]
			elif self.theta>=90 and self.theta<180: self.image = (self.images[self.theta-90])
			elif self.theta>=180 and self.theta<270: self.image = self.images[self.theta-180]
			elif self.theta>=270 and self.theta<360: self.image = self.images[self.theta-270]
			self.angle = self.theta

		def adjust(self):
			distance = math.sqrt((self.x - self.goal.x) ** 2 + (self.y - self.goal.y) ** 2)
			if distance < 100:
				self.v[0] += ((self.goal.x - self.x) / distance) * 0.1
				self.v[1] += ((self.goal.y - self.y) / distance) * 0.1

	class goal:
		def __init__(self, x, y):
			self.x = x
			self.y = y
			self.image = pygame.image.load("images/goal.png")
			self.rect = self.image.get_rect()

		def blit(self):
			self.rect.center = (self.x, self.y)
			screen.blit(self.image, self.rect)

		def line(self):
			pygame.draw.line(screen, (0, 0, 0), (boids[0].x, boids[0].y), (self.x, self.y), 1)


Board = board()

boids = [Board.boid(250, 250, [2, 1], Board.goal(300, 300))]


def main():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		screen.fill(blue)
		for i in boids:
			i.move()
			i.adjust()
			i.blit()
			i.goal.blit()
			i.goal.line()
		time.sleep(1 / 25)
		pygame.display.flip()


main()
