import sys,os,pygame,random,math,numpy,pygame.time
#Globals
size = 15
KEY = {"UP":1,"DOWN":2,"LEFT":3,"RIGHT":4}
separation = 2
speed = 15
frames = 20
highscore = 0
class Snake:
    def __init__(self,x,y,dx,dy):
        self.segments = []
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.isAlive = True
        self.startTime = 0
        self.boosted = False
        self.slowed = False
        self.rockeater = False
        self.ghost = False
    
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
        #changes directional velocity based on key inputs, doesn't allow to move backwards
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
        #if the head is the only segment, allows for movement in any direction       
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
            
        #assigns correct image for each powerup
        if(self.rockeater):
            segment.image = pygame.image.load("rock2.png") 
        elif(self.boosted):
            segment.image = pygame.image.load("speed2.png") 
        elif(self.slowed):
            segment.image = pygame.image.load("slow.png")
        elif(self.ghost):
            segment.image = pygame.image.load("ghost.png")
    
    def killSnake(self):
        #systematically kills all segments in the snake
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
        #movement simply adds directional velocity to current location
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
        self.direction = ("x",2.5)
        self.dirs = [("x",2.5),("x",-2.5),("y",2.5),("y",-2.5)]
    
    def spawnfood(self):
        #spawns food in a randomly determined coordinate
        self.rect.x = random.uniform(10,890)
        self.rect.y = random.uniform(10,890)
        self.direction = random.choice(self.dirs)
    
    def move(self, xy, velocity):
        if xy == "x":
            self.rect.x += velocity
        elif xy == "y":
            self.rect.y += velocity

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("rock1.png")
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.rect.x = 0
        self.rect.y = 0         
    def spawnrock(self):
        onsnake = True
        xvar = 0
        yvar = 0
        while(onsnake):
            xvar = random.uniform(80,820)
            yvar = random.uniform(80,820)
            if((xvar >= 580 or xvar <= 420) and (yvar >= 580 or yvar <= 420)):
                onsnake = False
        self.rect.x = xvar
        self.rect.y = yvar

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("powerup.png")
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.rect.x = 0
        self.rect.y = 0
        self.powerups = ["slowmo","speedboost","shedskin", "rockeater", "ghost"]
        self.power = ""
        
    def spawnpowerup(self):
        self.rect.x = random.uniform(10,890)
        self.rect.y = random.uniform(10,890)        
    
    def powerused(self):
        self.power = random.choice(self.powerups)
        return self.power
            
        
        

class App:
    def __init__(self):
        
        self.running = True
        self.screen = None
        self.size = self.width, self.height = 900,900
        self.scoreNum = 0
        self.font = None
        self.FPS = 15 
        self.startTime = 0
        self.foodcounter = 0
        self.powerupcd = 0
        self.powerupexists = False

    def on_init(self):
        # The following lines are needed for any pygame.
        
        pygame.init()
        #calls init to initialize the game
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        #initializes the screen
        self.running = True
        #sets the state of the game to running
        self.font = pygame.font.SysFont(None, 30) 
        #initializes font
        self.startTime = pygame.time.get_ticks()
        # A surface is a solid colored box. In this case it is green.
        self.bgImg = pygame.Surface((900,900))
        #sets the size of the game surface
        self.bgImg.fill((184, 151, 118))
        #ssets the background color to brown
        self.screen.blit(self.bgImg,(0,0)) 
        # blit displays it on the screen (actually in the buffer).
        pygame.display.set_caption("Snake Arcade") 
        #sets caption
        
        #start screen
        startMes = self.font.render("Snake Arcade", True, (0, 128, 0))
        playMes = self.font.render("Play? Y/N", True, (0, 128, 0))
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
        self.powerups = pygame.sprite.RenderUpdates()
        self.head = pygame.sprite.RenderUpdates()
        self.food = pygame.sprite.RenderUpdates()
        self.rock = pygame.sprite.RenderUpdates()
        
        # The snake is one of the sprites. The self.snake list is the list of snakes
        #creates the snake object and creates the first segment, the head
        self.snake = Snake(500,500,.1,.1)
        segment = Segment()
        segment.image = pygame.image.load("redblock.png")
        self.snake.addSeg(segment)
        self.head.add(segment)
        
        #creates food object and spawns a food sprite on the screen
        food = Food()
        food.spawnfood()
        self.food.add(food)        
            
        #creates or spawns rocks
        for i in range(8):
            rock = Rock()
            rock.spawnrock()
            self.rock.add(rock)
        return True
    
    def endGame(self):     
        #plays deathsound and pauses music
        deathsound = pygame.mixer.Sound("death.wav")
        deathsound.play()
        pygame.mixer.music.stop()          
        
        #defines endgame text
        endMes = self.font.render("Game Over", True, (0, 128, 0))
        conMes = self.font.render("Play again? Y/N", True, (0, 128, 0))
                
        #displays the text upon game over        
        self.screen.blit(endMes,(320,240))
        self.screen.blit(conMes,(320+12,240+40))
        pygame.display.flip()
        pygame.display.update()
    
        #asks the user whether they want to continue or end the game
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
            #moves the snake
            self.snake.move()
            
            #moves the food
            for food in self.food:
                if self.foodcounter%20 == 0:
                    food.direction = random.choice(food.dirs)
                self.foodcounter+= 1
                food.move(food.direction[0], food.direction[1])
            
            #kills snake if out of bounds or colliding with another segment
            if self.snake.segments[0].rect.x>900 or self.snake.segments[0].rect.x <0 or self.snake.segments[0].rect.y >900 or self.snake.segments[0].rect.y < 0:
                self.snake.killSnake()
                self.endGame()
            colliding = pygame.sprite.spritecollideany(self.snake.segments[0], self.sprites)
            if colliding != self.snake.segments[0] and colliding != None and self.snake.ghost == False:
                self.snake.killSnake()             
                self.endGame()
            
            #kills food if it goes out of bounds
            for food in self.food:
                if food.rect.x>900 or food.rect.x<0 or food.rect.y>900 or food.rect.y<0:
                    eatsound = pygame.mixer.Sound("squeak.wav")
                    eatsound.play()                      
                    food.kill()
                    newfood = Food()
                    newfood.spawnfood()
                    self.food.add(newfood)
            
            #checking for collisions with rocks
            colliding = pygame.sprite.spritecollideany(self.snake.segments[0], self.rock)
            if not colliding == None:
                if(self.snake.rockeater == True):
                    eatsound = pygame.mixer.Sound("hitnoise.wav")
                    eatsound.play()                     
                    colliding.kill()
                else:
                    self.snake.killSnake()                 
                    self.endGame()
            
            #checks if player is colliding with food and awards food/segments
            colliding = pygame.sprite.spritecollideany(self.snake.segments[0], self.food)
            if colliding != None:
                eatsound = pygame.mixer.Sound("squeak.wav")
                eatsound.play()                
                colliding.kill()
                for i in range(5):
                    segment = Segment()
                    self.snake.addSeg(segment)
                    self.sprites.add(segment)
                food = Food()
                food.spawnfood()
                self.food.add(food)
                self.scoreNum += 5
                if(self.powerupexists == False):
                    self.powerupcd +=1
            #checks if player collides with a powerup and powers the snake up   
            colliding = pygame.sprite.spritecollideany(self.snake.segments[0], self.powerups)
            if colliding != None:
                eatsound = pygame.mixer.Sound("hitnoise.wav")
                eatsound.play()   
                power = colliding.powerused()
                if(power == "slowmo"):
                    self.FPS = 7.5
                    for segment in self.snake.segments:
                        if segment != self.snake.segments[0]:
                            segment.image = pygame.image.load("slow.png")
                    pygame.time.set_timer(pygame.USEREVENT+1, 5000)
                    self.snake.slowed = True
                elif(power == "speedboost"):
                    self.FPS = 30
                    for segment in self.snake.segments:
                        if segment != self.snake.segments[0]:
                            segment.image = pygame.image.load("speed2.png")
                    pygame.time.set_timer(pygame.USEREVENT+1, 5000) 
                    self.snake.boosted = True
                elif(power == "shedskin"):
                    removelist = []
                    for i in range(len(self.snake.segments)-1, len(self.snake.segments)-21, -1):
                        if(i == 0):
                            break
                        else:
                            self.snake.segments[i].kill()
                            removelist.append(self.snake.segments[i])
                    for segment in removelist:
                        self.snake.segments.remove(segment)
                elif(power == "rockeater"):
                    self.snake.rockeater = True
                    for segment in self.snake.segments:
                        if segment != self.snake.segments[0]:
                            segment.image = pygame.image.load("rock2.png")
                    pygame.time.set_timer(pygame.USEREVENT+1, 5000)
                elif(power == "ghost"):
                    self.snake.ghost = True
                    for segment in self.snake.segments:
                        if segment != self.snake.segments[0]:
                            segment.image = pygame.image.load("ghost.png")
                    pygame.time.set_timer(pygame.USEREVENT+1, 5000)
                #adds score and kills the powerup
                self.scoreNum += 10
                colliding.kill()
                self.powerupexists = False
                                  
            if (self.powerupexists != True) and (self.powerupcd >= 2):
                self.powerupcd = 0
                self.powerupexists = True
                powerup = Powerup()
                powerup.spawnpowerup()
                self.powerups.add(powerup)
                colliding = pygame.sprite.spritecollideany(powerup, self.rock)
                spawned = False
                while(spawned == False):
                    if colliding != None:
                        powerup.kill()
                        powerup = Powerup()
                        powerup.spawnpowerup()
                        self.powerups.add(powerup) 
                        colliding = pygame.sprite.spritecollideany(powerup, self.rock)
                    else:
                        spawned = True     
                        
            #updates highscore
            global highscore
            if self.scoreNum > highscore:
                highscore = self.scoreNum             
    
    def on_render(self):
        # The on_render is responsible for rendering or drawing the
        # frame
        # These next lines clear each sprite from the screen by redrawing
        # the background behind that sprite.
        self.sprites.clear(self.screen,self.bgImg)
        self.powerups.clear
        self.food.clear(self.screen,self.bgImg)
        self.head.clear(self.screen, self.bgImg)
        self.rock.clear(self.screen, self.bgImg)
        self.screen.fill((184, 151, 118))

        # These next lines call blit to draw each sprite on the screen
        
        
        self.rock.draw(self.screen)
        self.head.draw(self.screen)
        self.sprites.draw(self.screen)
        self.powerups.draw(self.screen)
        self.food.draw(self.screen)
        
        score = self.font.render("Score: ", True, (0, 128, 0)) 
        time = self.font.render("Time: ", True, (0, 128, 0)) # Text and time          
        hiscore = self.font.render("High Score: ", True, (0,128,0))
        # Since double buffering is used, the flip method
        # switches the displayed buffer and the drawing buffer.
        
        gameTime = pygame.time.get_ticks() - self.startTime
               
        timeNum = self.font.render(str(gameTime/1000), True, (0, 128, 0)) # Text and time
    
        scoreTotal = self.font.render(str(self.scoreNum), True, (0, 128, 0)) # Text and score
        
        hiscorenum = self.font.render(str(highscore), True, (0,128,0))
    
        
        self.screen.blit(score, (700,10)) # Text and score
        self.screen.blit(time, (700,30)) # Text and time
        self.screen.blit(timeNum, (770,30)) # Text and time
        self.screen.blit(scoreTotal, (770, 10)) # Text and score
        self.screen.blit(hiscore,(700,50))
        self.screen.blit(hiscorenum,(820,50))
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
            clock.tick(self.FPS)
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
            elif event.type == pygame.USEREVENT+1:
                self.FPS = 15
                self.snake.rockeater = False
                self.snake.slowed = False
                self.snake.boosted = False
                self.snake.ghost = False
                for segment in self.snake.segments:
                    if segment != self.snake.segments[0]:
                        segment.image = pygame.image.load("greenblock.png")
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