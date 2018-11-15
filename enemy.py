class Enemy:
    def __init__(self, pos_x, pos_y, health):
        self.x = pos_x
        self.y = pos_y
        self.x_vel = 1
        self.health = health
        self.max_health = health
        
    def tick(self):
        self.x += self.x_vel
        
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
        
    def set_vel(self, new_vel):
        self.x_vel = new_vel