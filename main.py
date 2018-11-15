import pygame
import math
from random import randint
from game import Game

screen_width = 800
screen_height = 600

def draw_game():
    def cnvtY(n): #Convert from cartesian form to python form
        return -n + screen_height
    
    
    if game.state == 0:
        #Menu
        pygame.draw.rect(screen, (30,30,30), pygame.Rect(380, cnvtY(280), 80, 50))
        screen.blit(myfont.render("MENU", 1, (255,255,255)), (400, cnvtY(300)))
    elif game.state == 1:
        def loadXTranslate(x):
            return x + game.x * (-1) + screen_width/2.0
        def draw_rect(color, x, y, w, h):
            pygame.draw.rect(screen, color, pygame.Rect(loadXTranslate(x) - w/2.0, cnvtY(y), w, h))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(loadXTranslate(x), cnvtY(y), 5, 5))
        def draw_gui_rect(color, x, y, w, h):
            pygame.draw.rect(screen, color, pygame.Rect(loadXTranslate(x - 25), cnvtY(y), w, h))
        def draw_ellipse(color, x, y, w, h):
            pygame.draw.ellipse(screen, color, pygame.Rect(loadXTranslate(x) - w/2.0, cnvtY(y), w, h))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(loadXTranslate(x), cnvtY(y), 5, 5))

            
        #Background
        screen.fill((135,206,235))
        #Capital
        draw_rect((52,37, 26), 0, 200, 200, screen_height-600+150)
        #Catapults and balls
        for i in range(len(game.catapult)):
            draw_rect((123,50,10), game.catapult[i].getX(), game.catapult[i].getY(), 50, 50)
            draw_rect((255, 0, 0), game.catapult[i].getX(), game.catapult[i].getY(), game.catapult[i].get_progress(), 50)
            for ball in game.catapult[i].balls:
                draw_ellipse((10,123,50), ball.getX(), ball.getY(), 10, 10)
        #Enemies
        for enemy in game.enemies:
            draw_rect((255, 0, 0), enemy.getX(), enemy.getY(), 50, 50) #50, 50
            draw_gui_rect((60, 180, 0), enemy.getX(), enemy.getY() + 30, (enemy.get_health()/enemy.get_start_health())*50, 15) #*50, 15
            
        #Wall
        for wall in game.walls:
            draw_rect((255, 0, 0), wall.getX(), wall.getY() - 20, 16, 30)
            
        #text
        screen.blit(myfont.render("Points: {}".format(game.points), 1, (255,255,0)), (50, cnvtY(550)))
        screen.blit(myfont.render("Enemies: {}".format(game.get_enemies_amount()), 1, (255,255,0)), (50, cnvtY(525)))
        screen.blit(myfont.render("Wave: {}".format(game.get_wave_number()), 1, (255, 255,0)), (50, cnvtY(500)))
        
        #Ground
        #pygame.draw.line(screen, (255), (0, cnvtY(50)), (screen_width, cnvtY(50)))
        draw_gui_rect((0, 255, 60), -5000, 50, 10000, 50)
        #Player
        draw_rect((10,123,50), game.x, game.y, 50, 50)
    elif game.state == 2:
        #Pause
        pygame.draw.rect(screen, (30,30,30), pygame.Rect(380, cnvtY(280), 80, 50))
        screen.blit(myfont.render("PAUSE", 1, (255,255,255)), (400, cnvtY(300)))

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

done = False

game = Game()

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            game.toggle_pause()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game.started():
                game.end_game()
            else:
                game.start_game()
    
    pressed = pygame.key.get_pressed()
    
    game.tick(pygame, pressed)
    draw_game()
    
    pygame.display.flip()
    clock.tick(60)

