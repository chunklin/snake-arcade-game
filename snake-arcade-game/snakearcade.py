import sys,os,pygame,random,math,numpy,pygame.time
#Globals
speed = 15
size = 15
spacing = 2
KEY = {"UP":1,"DOWN":2,"LEFT":3,"RIGHT":4}

class Snake:
    def __init__(self,x,y,dx,dy):
        self.segments = []
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.isAlive = True
        self.startTime = 0
    
    def move(self): 
        #starting from the last segment, they replace the one in front
        for i in range(len(self.segments)-1, 0, -1):
            currentSeg = self.segments[i]
            prevSeg = self.segments[i-1]
            currentSeg.rect.x = prevSeg.rect.x 
            currentSeg.rect.y = prevSeg.rect.y 
            currentSeg.dx = prevSeg.dx
            currentSeg.dy = prevSeg.dy
        #last, moves the head
        self.segments[0].move()
          
    def changeDir(self,direction):
        #changes directional velocity based on key inputs
        if(len(self.segments)>1 and self.segments[0].rect.x - self.segments[0].dx == self.segments[1].rect.x):
            if(direction == "UP" and self.segments[0].dy != speed):
                self.segments[0].dx = 0
                self.segments[0].dy = -speed
            elif(direction == "DOWN" and self.segments[0].dy != -speed):
                self.segments[0].dx = 0
                self.segments[0].dy = speed
            elif(direction == "RIGHT" and self.segments[0].dx != -speed):
                self.segments[0].dx = speed
                self.segments[0].dy= 0
            elif(direction == "LEFT" and self.segments[0].dx != speed):
                self.segments[0].dx = -speed
                self.segments[0].dy = 0  
        elif(len(self.segments) == 1):
            if(direction == "UP"):
                self.segments[0].dx = 0
                self.segments[0].dy = -speed
            elif(direction == "DOWN"):
                self.segments[0].dx = 0
                self.segments[0].dy = speed
            elif(direction == "RIGHT"):
                self.segments[0].dx = speed
                self.segments[0].dy= 0
            elif(direction == "LEFT"):
                self.segments[0].dx = -speed
                self.segments[0].dy = 0              
            
    def addSeg(self, segment):
        #if there are no segments yet, add the head first
        if len(self.segments) == 0:
            self.segments.append(segment)
            self.segments[0].rect.x = self.x
            self.segments[0].rect.y = self.y
            self.segments[0].dx = self.dx
            self.segments[0].dy = self.dy
        #the new segment takes the place of the last segment
        else:
            segment.rect.x = self.segments[-1].rect.x
            segment.rect.y = self.segments[-1].rect.y
            self.segments.append(segment)
    def killSnake(self):
        for segment in self.segments:
            segment.kill()
        self.isAlive = False

class Segment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("greenblock.png")
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.rect.x = 0
        self.rect.y = 0
        self.dx = 0
        self.dy = 0
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy        
            
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("mouse.png")
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.rect.x = 0
        self.rect.y = 0 
    def spawnfood(self):
        self.rect.x = random.uniform(10,890)
        self.rect.y = random.uniform(10,890)


class App:
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = self.width, self.height = 900,900
        self.scoreNum = 0
        self.font = None
        self.startTime = 0
    
                 

    def on_init(self):
        # The following lines are needed for any pygame.
        self.startTime = pygame.time.get_ticks()
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True
        self.font = pygame.font.SysFont(None, 30) # Text
        # A surface is a solid colored box. In this case it is green.
        self.bgImg = pygame.Surface((900,900))
        self.bgImg.fill((184, 151, 118))
        # blit displays it on the screen (actually in the buffer).
        self.screen.blit(self.bgImg,(0,0))
        pygame.display.set_caption("Snake Arcade") 
        startMes = self.font.render("Snake Arcade", True, (0, 128, 0))
        playMes = self.font.render("Play? Y/N", True, (0, 128, 0))
        
        self.screen.fill((184, 151, 118))
        self.screen.blit(startMes,(380,340))
        self.screen.blit(playMes,(380+12,340+40))
        pygame.display.flip()
        pygame.display.update()
        menu = True
        while(menu):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                        self.running = False
                        menu = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                        menu = False
                        
        
        # self.sprites is a RenderUpdates group. A group is a group of sprites. Groups
        # provide the ability to draw sprites on the screen and other management of
        # sprites.
        self.sprites = pygame.sprite.RenderUpdates()
        self.head = pygame.sprite.RenderUpdates()
        self.food = pygame.sprite.RenderUpdates()
        # The ball is one of the sprites. The self.balls list is the list of balls
        # bouncing on the screen.
        self.snake = Snake(500,500,.1,.1)
        segment = Segment()
        segment.image = pygame.image.load("redblock.png")
        self.snake.addSeg(segment)
        self.head.add(segment)
        food = Food()
        food.spawnfood()
        self.food.add(food)        
        
        return True
    def endGame(self):       
        endMes = self.font.render("Game Over", True, (0, 128, 0))
        conMes = self.font.render("Play again? Y/N", True, (0, 128, 0))
                
                
        self.screen.blit(endMes,(320,240))
        self.screen.blit(conMes,(320+12,240+40))
        pygame.display.flip()
        pygame.display.update()
        endgame = True
        while(endgame):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                        sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                        theApp = App()
                        theApp.on_execute()
                        sys.exit()
                        
    def on_loop(self):
        # The on_loop is called below in the on_execute. This handles the changes
        # to the model of this program. It does not do any drawing.
        if(self.snake.isAlive):
            self.snake.move()
            if self.snake.segments[0].rect.x>900 or self.snake.segments[0].rect.x <0 or self.snake.segments[0].rect.y >900 or self.snake.segments[0].rect.y < 0:
                self.snake.killSnake()
                self.endGame()
            colliding = pygame.sprite.spritecollideany(self.snake.segments[0], self.sprites)
            
            if colliding != self.snake.segments[0] and colliding != None:
                self.snake.killSnake()
                self.endGame()
            colliding = pygame.sprite.spritecollideany(self.snake.segments[0], self.food)
            if colliding != None:
                colliding.kill()
                for i in range(3):
                    segment = Segment()
                    self.snake.addSeg(segment)
                    self.sprites.add(segment)
                food = Food()
                food.spawnfood()
                self.food.add(food)
                self.scoreNum += 10     
            
            
    
    def on_render(self):
        # The on_render is responsible for rendering or drawing the
        # frame.
        # These next lines clear each sprite from the screen by redrawing
        # the background behind that sprite.
        self.sprites.clear(self.screen,self.bgImg)
        self.food.clear(self.screen,self.bgImg)
        self.head.clear(self.screen, self.bgImg)
        self.screen.fill((184, 151, 118))

        # These next lines call blit to draw each sprite on the screen
        self.sprites.draw(self.screen)
        self.food.draw(self.screen)
        self.head.draw(self.screen)
        
        score = self.font.render("Score: ", True, (0, 128, 0)) 
        time = self.font.render("Time: ", True, (0, 128, 0)) # Text and time          
        # Since double buffering is used, the flip method
        # switches the displayed buffer and the drawing buffer.
        
        gameTime = pygame.time.get_ticks() - self.startTime
               
        timeNum = self.font.render(str(gameTime/1000), True, (0, 128, 0)) # Text and time
    
        scoreTotal = self.font.render(str(self.scoreNum), True, (0, 128, 0)) # Text and score
    
        
        self.screen.blit(score, (700,10)) # Text and score
        self.screen.blit(time, (700,30)) # Text and time
        self.screen.blit(timeNum, (770,30)) # Text and time
        self.screen.blit(scoreTotal, (770, 10)) # Text and score
        pygame.display.flip()
        pygame.display.update()           
        

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False
        clock = pygame.time.Clock()   
        pygame.mixer.init()
        pygame.mixer.music.load("backgroundmusic.mp3")
        pygame.mixer.music.play(-1,0.0)
        while(self.running):
            clock.tick(20)
            # The following get method call is a non-blocking
            # call that gets an event if one is ready. Otherwise
            # it drops through the for loop.
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()    

    def on_event(self, event):
            # This is an event processing function that is called with an event when it occurs.
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_UP:
                    self.snake.changeDir("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.changeDir("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.changeDir("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.changeDir("RIGHT")  
                    
    
                    
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()    