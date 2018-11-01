class Ball:
    def __init__(self, strength, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.strength = strength
        
        self.time = -100
        
    def tick(self):
        self.time += (1/10.0) * self.strength/10
        self.y = 0.5 * self.time * self.time
        self.x = -self.time
        
    def getX(self):
        return self.x + 600
    
    def getY(self):
        return self.y + 50