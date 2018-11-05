import pygame
import math
from random import randint
from game import Game

screen_width = 800
screen_height = 600

def draw_game():
    def cnvtY(n): #Convert from cartesian form to python form
        return n * -1 + screen_height
    if game.state == 0:
        #Menu
        pygame.draw.rect(screen, (30,30,30), pygame.Rect(380, cnvtY(280), 80, 50))
        screen.blit(myfont.render("MENU", 1, (255,255,255)), (400, cnvtY(300)))
    elif game.state == 1:
        def loadXTranslate(x):
            return x + game.x * (-1) + screen_width/2.0
        #Game
        screen.fill((0,10,20))
        #Player
        pygame.draw.rect(screen, (10,123,50), pygame.Rect(loadXTranslate(game.x), cnvtY(game.y), 50, 50))
        #Catapult and balls
        for i in range(len(game.catapult)):
            pygame.draw.rect(screen, (123,50,10), pygame.Rect(loadXTranslate(game.catapult[i][0]), cnvtY(game.catapult[i][1]), 50, 50))
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(loadXTranslate(game.catapult[i][0]), cnvtY(game.catapult[i][1]), game.catapultProgress[i], 50))
        for ball in game.balls:
            pygame.draw.ellipse(screen, (10,123,50), pygame.Rect(loadXTranslate(ball.getX()), cnvtY(ball.getY()), 10, 10))
        for enemy in game.enemies:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(loadXTranslate(enemy.getX()), cnvtY(enemy.getY()), 50, 50))
        #text
        screen.blit(myfont.render("Points: {}".format(game.points), 1, (255,255,0)), (50, cnvtY(550)))
        screen.blit(myfont.render("Enemies: {}".format(game.get_enemies_amount()), 1, (255,255,0)), (50, cnvtY(525)))
        
        #Background
        pygame.draw.line(screen, (255), (0, cnvtY(50)), (screen_width, cnvtY(50)))
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

