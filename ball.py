class Ball:
    def __init__(self, strength, pos_x, pos_y, xdir):
        self.x = pos_x
        self.y = pos_y
        self.y_vel = strength/10.0
        self.strength = strength/8.0 * (-xdir)
        
    def tick(self):
        self.x -= self.strength
        self.y_vel -= 9.82/50.0
        self.y += self.y_vel
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y