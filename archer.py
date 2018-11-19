class Archer:
    def __init__(self, x, y):
        self.health = 50
        self.x = x
        self.y = y
        
        self.enemy_found = 0
        self.speed = 1
        self.go_to_x = -1
        self.manning = 0
        self.manned_the_catapult = -1
        
    def tick(self, unmanned):
        self.unmanned = unmanned
        
        if self.manning == 0:
            if self.go_to_x > self.x:
                self.x += self.speed
            else:
                self.x -= self.speed
                
            if len(self.unmanned) > 0:
                new_pos = self.unmanned[0][0]
                if new_pos > 0:
                    self.go_to_x = self.unmanned[0][0] - 25
                else:
                    self.go_to_x = self.unmanned[0][0] + 25
                if abs(self.go_to_x - self.x) < 1:
                    self.go_to_x = -1
                    self.manned_the_catapult = self.unmanned[0][1]
                    self.manning = 1
        
    def manning_catapult(self):
        return self.manning
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
    def get_health(self):
        return self.health