class Wall:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y