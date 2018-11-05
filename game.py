import math
import pygame
from random import randint
from ball import Ball
from enemy import Enemy

class Game:
    def __init__(self):
        self.state = 0
        #State 0: Menu
        #State 1: Game
        #State 2: Pause
        self.x = 400
        self.y = 250
        
        self.y_vel = 0
        self.x_vel = 0
        self.max_x_vel = 3
        
        self.points = 0
        self.y_ground = 100
        self.catapult = [[100, self.y_ground], [700, self.y_ground]]
        self.catapultProgress = [0, 0]

        self.balls = []
        self.enemies = []
        
        self.grav_acc = 9.82
            

    def tick(self, pg, pressed):
        def fire_catapult(strength, x, y, xdir):
            self.balls.append(Ball(strength, x, y, xdir))
        def spawn_enemy(x, y, health):
            self.enemies.append(Enemy(x, y, health))
            
        def collision(x0, y0, x1, y1):
            if abs((x0 + 25) - (x1 + 25)) > 50 or y0 > y1:
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
            
            if pressed[pg.K_UP]:
                spawn_enemy(-200, 100, 50)
                
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
            for i in range(len(self.catapult)):
                if (self.y == self.y_ground and pressed[pg.K_DOWN] and collision(self.x, self.y, self.catapult[i][0], self.catapult[i][1]) and self.catapultProgress[i] < 50):
                    self.catapultProgress[i] += 1
                if (self.catapultProgress[i] > 0) and (not pressed[pg.K_DOWN] or not collision(self.x, self.y, self.catapult[i][0], self.catapult[i][1])):
                    if i == 0:
                        fire_catapult(self.catapultProgress[i], self.catapult[i][0], self.catapult[i][1], 1)
                    else:
                        fire_catapult(self.catapultProgress[i], self.catapult[i][0], self.catapult[i][1], -1)
                    self.catapultProgress[i] = 0
            
            ii = 0
            for i in range(len(self.balls)):
                self.balls[ii].tick()
                if(self.balls[ii].y < 50):
                    self.balls.pop(ii)
                    ii -= 1
                ii += 1
                
            ii = 0
            for i in range(len(self.enemies)):
                self.enemies[ii].tick()
                jj = 0
                for j in range(len(self.balls)):
                    if (collision(self.enemies[ii].getX(), self.enemies[ii].getY(), self.balls[jj].getX(), self.balls[jj].getY())):
                        self.balls.pop(jj)
                        self.enemies.pop(ii)
                        ii -= 1
                        jj -= 1
                    jj += 1
                ii += 1
                
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
        
    def get_enemies_amount(self):
        return len(self.enemies)