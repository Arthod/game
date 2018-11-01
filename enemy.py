class Enemy:
    def __init__(self, pos_x, pos_y, health):
        self.x = pos_x
        self.y = pos_y
        self.x_vel = 1
        self.health = health
        
    def tick(self):
        self.x += self.x_vel
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y