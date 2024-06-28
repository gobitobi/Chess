import pygame
import chess
import os
from Game import Game

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            game.handle_user_interaction(event)
            
        
        
        game.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()


