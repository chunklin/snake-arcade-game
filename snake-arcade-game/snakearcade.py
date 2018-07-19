import sys,os,pygame,random,math
#Globals
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
    
    def move(self): 
        for i in range(len(self.segments)-1, 0, -1):
            currentSeg = self.segments[i]
            prevSeg = self.segments[i-1]
            currentSeg.rect.x = prevSeg.rect.x
            currentSeg.rect.y = prevSeg.rect.y
            currentSeg.dx = prevSeg.dx
            currentSeg.dy = prevSeg.dy
        self.segments[0].move()
          
    def changeDir(self,direction):
        if(direction == "UP"):
            self.segments[0].dx = 0
            self.segments[0].dy = -10
        elif(direction == "DOWN"):
            self.segments[0].dx = 0
            self.segments[0].dy = 10
        elif(direction == "RIGHT"):
            self.segments[0].dx = 10
            self.segments[0].dy= 0
        else:
            self.segments[0].dx = -10
            self.segments[0].dy = 0  
            
    def addSeg(self, segment):
        
        if len(self.segments) == 0:
            self.segments.append(segment)
            self.segments[0].rect.x = self.x
            self.segments[0].rect.y = self.y
            self.segments[0].dx = self.dx
            self.segments[0].dy = self.dy
        else:
            self.segments.append(segment)
            
        
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
            
        


class App:
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = self.width, self.height = 600, 600


    def on_init(self):
        # The following lines are needed for any pygame.
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True

        # A surface is a solid colored box. In this case it is green.
        self.bgImg = pygame.Surface((600,600))
        self.bgImg.fill((128,128,128))
        # blit displays it on the screen (actually in the buffer).
        self.screen.blit(self.bgImg,(0,0))

        pygame.display.set_caption("Snake Arcade")

        # self.sprites is a RenderUpdates group. A group is a group of sprites. Groups
        # provide the ability to draw sprites on the screen and other management of
        # sprites.
        self.sprites = pygame.sprite.RenderUpdates()

        # The ball is one of the sprites. The self.balls list is the list of balls
        # bouncing on the screen.
        self.snake = Snake(300,300,0,0)
        segment = Segment()
        self.snake.addSeg(segment)
        self.sprites.add(segment)
        
        return True
    
    def on_loop(self):
        # The on_loop is called below in the on_execute. This handles the changes
        # to the model of this program. It does not do any drawing.
        self.snake.move()
            
    
    def on_render(self):
        # The on_render is responsible for rendering or drawing the
        # frame.
        # These next lines clear each sprite from the screen by redrawing
        # the background behind that sprite.
        self.sprites.clear(self.screen,self.bgImg)

        # These next lines call blit to draw each sprite on the screen
        self.sprites.draw(self.screen)

        # Since double buffering is used, the flip method
        # switches the displayed buffer and the drawing buffer.
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while(self.running):
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
                elif event.key == pygame.K_SPACE:
                    segment = Segment()
                    self.snake.addSeg(segment)
                    self.sprites.add(segment)
                    


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()    