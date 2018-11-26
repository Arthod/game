import math
import pygame
from random import randint
from enemy import Enemy
from catapult import Catapult
#from waves import Waves
from wall import Wall
from archer import Archer

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
        
        self.catapult = [Catapult(-300, self.y_ground, 0, -1), Catapult(300, self.y_ground, 0, 1)]
        self.enemies = []
        self.walls = [Wall(-360, self.y_ground, 100), Wall(360, self.y_ground, 100)]
        self.archers = []#Archer(-50, self.y_ground), Archer(50, self.y_ground)]
        
        self.grav_acc = 9.82
        self.wave_number = 0
            

    def tick(self, pg, pressed):
        def spawn_enemy(x, y, health):
            self.enemies.append(Enemy(x, y, health))
        def build_wall(x, y, health):
            self.walls.append(Wall(x, y, health))
            
        def collision(x0, y0, w0, h0, x1, y1, w1, h1):
            if (math.sqrt((x0 - x1)**2 + ((y0 + h0/2.0) - (y1 + h1/2.0))**2) < w0/2.0 + w1/2.0):
                return True
            else:
                return False
        def ball_collision(ballx, bally, x, y, w, h):
            if x + w/2.0 > ballx > x - w/2.0 and bally < y:
                return True
            else:
                return False
            
        def dist_to_enemy(x, y, dir):
            closest_dist = 5000
            for enemy in self.enemies:
                if dir == -1:
                    if enemy.getX() < x:
                        if closest_dist > x - enemy.getX():
                            closest_dist = x - enemy.getX()
                    
                else:
                    if enemy.getX() > x:
                        if closest_dist > enemy.getX() - x:
                            closest_dist = enemy.getX() - x
                            
            if closest_dist == 5000:
                return -1
            else:
                return closest_dist
        
        def get_new_xdir(x):
            if x > 0:
                new_xdir = -1
            else:
                new_xdir = 1
            return new_xdir
            
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
            self.unmanned_catapults = []
            for i in range(len(self.catapult)):
                if self.catapult[i].get_manned() == 0:
                    self.unmanned_catapults.append((self.catapult[i].getX(), i))

                self.catapult[i].tick()
                if (self.catapult[i].ready_to_fire()):
                    if (self.catapult[i].get_manned() != 1):
                        if (self.y == self.catapult[i].getY() and pressed[pg.K_SPACE] and collision(self.x, self.y, 50, 50, self.catapult[i].getX(), self.catapult[i].getY(), 50, 50) and self.catapult[i].get_progress() < 50):
                            self.catapult[i].progress += 1
                        if (self.catapult[i].get_progress() > 0) and (not pressed[pg.K_SPACE] or not collision(self.x, self.y, 50, 50, self.catapult[i].getX(), self.catapult[i].getY(), 50, 50)):
                            self.catapult[i].fire_catapult(self.catapult[i].get_progress(), self.catapult[i].getX(), self.catapult[i].getY(), self.catapult[i].get_xdir())
                            self.catapult[i].progress = 0
                            self.catapult[i].timer = 60
                    else:
                        if (self.catapult[i].get_progress() > 0):
                            self.catapult[i].fire_catapult(self.catapult[i].get_progress(), self.catapult[i].getX(), self.catapult[i].getY(), self.catapult[i].get_xdir())
                            self.catapult[i].progress = 0
                            self.catapult[i].timer = 60
                else:
                    self.catapult[i].progress = 0
                    
            #Enemies
            ii = 0
            for i in range(len(self.enemies)):
                self.enemies[ii].tick()
                self.enemies[ii].set_xdir(get_new_xdir(self.enemies[ii].getX()))
                
                if self.enemies[ii].get_health() <= 0:
                    self.enemies.pop(ii)
                    ii -= 1
                ii += 1
            ii = 0
            for i in range(len(self.enemies)):
                for j in range(len(self.catapult)):
                    kk = 0
                    for k in range(len(self.catapult[j].balls)):
                        if (ball_collision(self.catapult[j].balls[kk].getX(), self.catapult[j].balls[kk].getY(), self.enemies[ii].getX(), self.enemies[ii].getY(), 50, 50)):
                            self.catapult[j].balls.pop(kk)
                            kk -= 1
                            self.enemies[ii].update_health(-25)
                        kk += 1
                ii += 1
            
            for i in range(len(self.enemies)):
                for j in range(len(self.walls)):
                    if collision(self.enemies[i].getX(), self.enemies[i].getY(), 50, 50, self.walls[j].getX(), self.walls[j].getY(), 16, 30):
                        self.enemies[i].x -= self.enemies[i].x_vel * 20 * self.enemies[i].get_xdir()
                        self.enemies[i].y += 10
                        self.enemies[i].set_vel(1)
                        self.walls[j].add_health(-5)
                        break
                    else:
                        self.enemies[i].set_vel(0)
        
        
            #Waves
            def next_wave():
                self.wave_number += 1
                for i in range(self.wave_number):
                    spawn_enemy(-600 + randint(-50, 50), 100, 50)
            if (len(self.enemies)) == 0:
                next_wave()
                
            #Archers
            for i in range(len(self.archers)):
                closest_enemy_dist = dist_to_enemy(self.archers[i].getX(), self.archers[i].getY(), self.catapult[self.archers[i].manned_the_catapult].get_xdir())
                self.archers[i].tick(self.unmanned_catapults)
                if self.archers[i].manning_catapult() == 1:
                    self.catapult[self.unmanned_catapults[0][1]].set_manned(1)
                    self.archers[i].manning = 2
                if self.archers[i].manning == 2:
                    if closest_enemy_dist == -1:
                        continue
                    self.catapult[self.archers[i].manned_the_catapult].progress += closest_enemy_dist/6
                    
            #Walls
            ii = 0
            for i in range(len(self.walls)):
                if self.walls[ii].get_health() <= 0:
                    self.walls.pop(ii)
                    ii -= 1
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
    
    def get_wave_number(self):
        return self.wave_number