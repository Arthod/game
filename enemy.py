class Enemy:
    def __init__(self, pos_x, pos_y, health):
        self.x = pos_x
        self.y = pos_y
        self.x_vel = 1
        self.xdir = 0
        self.health = health
        self.max_health = health
        
        self.y_ground = 100 #y position of ground.
        self.gravity = 9.82 / 50.0
        self.y_vel = 0
        
    def tick(self):
        self.x += self.x_vel * self.xdir
        if self.y > self.y_ground:
            self.y_vel -= self.gravity
        self.y += self.y_vel
        if self.y <= self.y_ground:
            self.y = self.y_ground
            self.y_vel = 0
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def get_health(self):
        return self.health
    
    def get_start_health(self):
        return self.max_health
    
    def update_health(self, diff_health):
        self.health += diff_health
        
    def set_xdir(self, new_value):
        self.xdir = new_value
        
    def set_vel(self, new_value):
        self.vel = new_value
        
    def get_xdir(self):
        return self.xdir
        
    