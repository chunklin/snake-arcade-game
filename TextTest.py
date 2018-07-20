import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

startTime = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 30)

score = font.render("Score: ", True, (0, 128, 0))

time = font.render("Time: ", True, (0, 128, 0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    gameTime = pygame.time.get_ticks() - startTime

    timeNum = font.render(str(gameTime/1000), True, (0, 128, 0))

    screen.fill((255, 255, 255))
    screen.blit(score, (500,10))
    screen.blit(time, (500,30))
    screen.blit(timeNum, (570,30))
    pygame.display.flip()
    #clock.tick(60)