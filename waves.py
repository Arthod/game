class Waves:
    def __init__(self):
        self.wave_number = 0
        
    def next_wave(self):
        self.wave_number += 1
        
        spawn_enemy(-400, 100, 50)
        
    def get_wave_number(self):
        return self.wave_number