import math
import pygame
from random import randint
from enemy import Enemy
from catapult import Catapult
#from waves import Waves
from wall import Wall

class Game:
    def __init__(self):
        self.state = 0
        #State 0: Menu
        #State 1: Game
        #State 2: Pause
        self.x = 0
        self.y = 250
        
        self.y_vel = 0
        self.x_vel = 0
        self.max_x_vel = 3
        
        self.points = 0
        self.y_ground = 100
        
        self.catapult = [Catapult(-300, self.y_ground, 0, 1), Catapult(300, self.y_ground, 0, -1)]
        self.enemies = []
        self.walls = []
        
        self.grav_acc = 9.82
        self.wave_number = 0
            

    def tick(self, pg, pressed):
        def spawn_enemy(x, y, health):
            self.enemies.append(Enemy(x, y, health))
        def build_wall(x, y, health):
            self.walls.append(Wall(x, y, health))
            
        def collision(x0, y0, w0, h0, x1, y1, w1, h1):
            if abs((x0 + w0/2.0) - (x1 + w1/2.0)) > (w0+w1) / 2.0:
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
                if self.x_vel != 0:
                    self.x_vel -= self.x_vel * 0.2
                
            if self.x_vel > self.max_x_vel:
                self.x_vel = self.max_x_vel
            if self.x_vel < -self.max_x_vel:
                self.x_vel = -self.max_x_vel
            self.x += self.x_vel
            self.y += self.y_vel
            
            #Catapult and balls
            for i in range(len(self.catapult)):
                cata = self.catapult[i]
                self.catapult[i].tick()
                if (self.y == cata.getY() and pressed[pg.K_DOWN] and collision(self.x, self.y, 50, 50, cata.getX(), cata.getY(), 50, 50) and cata.get_progress() < 50):
                    cata.progress += 1
                if (cata.get_progress() > 0) and (not pressed[pg.K_DOWN] or not collision(self.x, self.y, 50, 50, cata.getX(), cata.getY(), 50, 50)):
                    cata.fire_catapult(cata.get_progress(), cata.getX(), cata.getY(), cata.get_xdir())
                    cata.progress = 0
                    
            #Walls
            if (pressed[pg.K_b] and self.y == self.y_ground):
                build_wall(self.x, self.y, 50)
                
            ii = 0
            for i in range(len(self.enemies)):
                self.enemies[ii].tick()
                if self.enemies[ii].get_health() <= 0:
                    self.enemies.pop(ii)
                    ii -= 1
                ii += 1
            ii = 0
            for i in range(len(self.enemies)):
                for j in range(len(self.catapult)):
                    kk = 0
                    for k in range(len(self.catapult[j].balls)):
                        if (collision(self.enemies[ii].getX(), self.enemies[ii].getY(), 50, 50, self.catapult[j].balls[kk].getX(), self.catapult[j].balls[kk].getY(), 10, 10)):
                            self.catapult[j].balls.pop(kk)
                            kk -= 1
                            self.enemies[ii].update_health(-25)
                        kk += 1
                ii += 1
        
        #Waves
        def next_wave():
            self.wave_number += 1
            for i in range(self.wave_number):
                spawn_enemy(-700 + randint(-50, 50), 100, 50)
        if (len(self.enemies)) == 0:
            next_wave()
        
                
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
    
    def get_wave_number(self):
        return self.wave_number