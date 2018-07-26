import sys,os,pygame,random,math

pygame.init()
pygame.font.init()

pygame.display.set_caption("Testing for Snake Game")
font = pygame.font.SysFont(None, 30) # Text
screen_w = 640
screen_h = 480
screen = pygame.display.set_mode([screen_w, screen_h])
clock = pygame.time.Clock() # Time
done = False
screen.fill((255, 255, 255))

number = random.randrange(1, 8)

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                        sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        done = True
                        sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        scoreNum += 10 # score
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                        endGame()   


                randNum = font.render(str(number), True, (0, 0, 0))

                screen.fill((255, 255, 255))
                screen.blit(randNum, (200, 200))
                pygame.display.flip()
                pygame.display.update()



#def main():
        
        #done = False
        
        #startMes = font.render("Snake Arcade", True, (0, 128, 0))
        #playMes = font.render("Play? Y/N", True, (0, 128, 0))
                
        
        #screen.blit(startMes,(320,240))
        #screen.blit(playMes,(320+12,240+40))
        #pygame.display.flip()
        #pygame.display.update()
                
        #while not done:
                #for event in pygame.event.get():
                        #if event.type == pygame.QUIT:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                                #start()
                                
                             
                                
#def start():
        
        #done = False

        #startTime = pygame.time.get_ticks() # Time

        #scoreNum = 0 # score

        #score = font.render("Score: ", True, (0, 128, 0)) # Text and score
        #time = font.render("Time: ", True, (0, 128, 0)) # Text and time

        #while not done:
                #for event in pygame.event.get():
                        #if event.type == pygame.QUIT:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                #scoreNum += 10 # score
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                                #endGame()                       

                #gameTime = pygame.time.get_ticks() - startTime # Time

                #timeNum = font.render(str(gameTime/1000), True, (0, 128, 0)) # Text and time

                #scoreTotal = font.render(str(scoreNum), True, (0, 128, 0)) # Text and score

                #screen.fill((255, 255, 255))
                #screen.blit(score, (500,10)) # Text and score
                #screen.blit(time, (500,30)) # Text and time
                #screen.blit(timeNum, (570,30)) # Text and time
                #screen.blit(scoreTotal, (570, 10)) # Text and score
                #pygame.display.flip()
                #pygame.display.update()
                ##clock.tick(60)
            
#def endGame():
        
        #done = False
        
        #endMes = font.render("Game Over", True, (0, 128, 0))
        #conMes = font.render("Play again? Y/N", True, (0, 128, 0))
                
                
        #screen.blit(endMes,(320,240))
        #screen.blit(conMes,(320+12,240+40))
        #pygame.display.flip()
        #pygame.display.update()
                
        #while not done:
                #for event in pygame.event.get():
                        #if event.type == pygame.QUIT:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                                #done = True
                                #sys.exit()
                        #if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                                #start()
                                            
#main()           