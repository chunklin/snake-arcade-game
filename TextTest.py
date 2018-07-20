import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
#clock = pygame.time.Clock()
done = False

font = pygame.font.SysFont(None, 30)

score = font.render("Score: ", True, (0, 128, 0))

time = font.render("Time: ", True, (0, 128, 0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True


    screen.fill((255, 255, 255))
    screen.blit(score, (500,10))
    screen.blit(time, (500,30))
    pygame.display.flip()
    #clock.tick(60)