import math
import pygame
from random import randint
from ball import Ball

class Game:
    def __init__(self):
        self.state = 0
        #State 0: Menu
        #State 1: Game
        #State 2: Pause
        self.x = 600
        self.y = 500
        
        self.y_vel = 0
        self.x_vel = 0
        self.max_x_vel = 3
        
        self.points = 0
        self.y_ground = 100
        self.catapult = [600, self.y_ground]

        self.balls = []
        
        self.grav_acc = 9.82
            

    def tick(self, pg, pressed):
        def fire_catapult(strength, x, y):
            self.balls.append(Ball(strength, x, y))
            
        def collision(x0, y0, x1, y1):
            if abs(x0 - x1) > 50:
                return False
            else:
                return True
            
        if self.state == 1:
            #Movement
            if self.y > self.y_ground:
                self.y_vel -= self.grav_acc / 50
            elif self.y_vel < 0:
                self.y_vel = 0
                self.y = self.y_ground
                
            if pressed[pg.K_UP] and self.y <= self.y_ground:
                self.y_vel += 6
            if pressed[pg.K_LEFT]: 
                self.x_vel -= 0.5
            if pressed[pg.K_RIGHT]: 
                self.x_vel += 0.5
            if (not pressed[pg.K_UP] and not pressed[pg.K_LEFT] and not pressed[pg.K_RIGHT]):
                self.x_vel = 0
                
            if self.x_vel > self.max_x_vel:
                self.x_vel = self.max_x_vel
            if self.x_vel < -self.max_x_vel:
                self.x_vel = -self.max_x_vel
            self.x += self.x_vel
            self.y += self.y_vel
            
            #Catapult and balls
            if (self.y == self.y_ground and pressed[pg.K_DOWN] and collision(self.x, self.y, self.catapult[0], self.catapult[1])):
                fire_catapult(50, self.x, self.y)
            for ball in self.balls:
                ball.tick()

            #if math.sqrt((self.target[0] - self.x)**2 + (self.target[1] - self.y)**2) < 40:
            #    self.points += 1
            #    self.catapult = [randint(0,800), randint(0,600)]

    def start_game(self):
        if self.state == 0:
            self.state = 1     
            self.points = 0

    def end_game(self):
        if self.state > 0:
            self.state = 0

    def toggle_pause(self):
        if self.state == 1:
            self.state = 2
        else:
            self.state = 1

    def started(self):
        if self.state > 0:
            return True
        else:
            return False