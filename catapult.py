from ball import Ball

class Catapult:
    def __init__(self, x, y, progress, xdir):
        self.x = x
        self.y = y
        self.progress = progress
        self.xdir = xdir
        self.balls = []
        self.manned = 0
        self.timer = 20
        
    def tick(self):
        ii = 0
        for i in range(len(self.balls)):
            self.balls[ii].tick()
            if(self.balls[ii].y < 50):
                self.balls.pop(ii)
                ii -= 1
            ii += 1
        if self.timer > 0:
            self.timer -= 1
        
        
    def fire_catapult(self, strength, x, y, xdir):
        self.balls.append(Ball(strength, x, y, xdir))
        
    def getY(self):
        return self.y
    
    def getX(self):
        return self.x
    
    def get_progress(self):
        return self.progress
    
    def get_xdir(self):
        return self.xdir
    
    def get_manned(self):
        return self.manned
    
    def set_manned(self, new_value):
        self.manned = new_value
        
    def ready_to_fire(self):
        if (self.timer <= 0):
            return True
        else:
            return False