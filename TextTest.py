import pygame

pygame.init()

pygame.display.set_caption("Testing for Snake Game")
font = pygame.font.SysFont(None, 30) # Text
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock() # Time
done = False
#screen.fill((255, 255, 255))


#def start():
        
        #startMes = font.render("Snake Arcade", True, (0, 128, 0))
        #playMes = font.render("Play? Y/N", True, (0, 128, 0))
        #screen.blit(startMes,(320,240))
        #screen.blit(playMes,(320+12,240+40))
        
        #pygame.display.flip()
        #pygame.display.update()
        
        #while not done:
                #for event in pygame.event.get():
                #if event.type == pygame.KEYDOWN:
                        #if event.key == pygame.K_Y:
                                #main()
                        #elif event.key == pygame.K_N:
                                #done = True
        
#def main():
    
done = False

startTime = pygame.time.get_ticks() # Time

scoreNum = 0 # score

score = font.render("Score: ", True, (0, 128, 0)) # Text and score
time = font.render("Time: ", True, (0, 128, 0)) # Text and time
while not done:
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            scoreNum += 10 # score

    gameTime = pygame.time.get_ticks() - startTime # Time

    timeNum = font.render(str(gameTime/1000), True, (0, 128, 0)) # Text and time

    scoreTotal = font.render(str(scoreNum), True, (0, 128, 0)) # Text and score

    screen.fill((255, 255, 255))
    screen.blit(score, (500,10)) # Text and score
    screen.blit(time, (500,30)) # Text and time
    screen.blit(timeNum, (570,30)) # Text and time
    screen.blit(scoreTotal, (570, 10)) # Text and score
    pygame.display.flip()
    pygame.display.update()
    #clock.tick(60)
            
#main()           