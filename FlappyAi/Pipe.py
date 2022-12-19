import pygame
import random 
import os 

#Pipe img variable deceleration and initialization
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png"))) 

class Pipe:
    #Space between pipes 
    GAP = 200
    #pipes move not the bird 
    VEL = 2
    
    def __init__(self,x):
        self.x = x
        self.height = 0
        
        self.top =0
        self.bottom =0
        # flipped pipe image
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        #normal pipe image 
        self.PIPE_BOTTOM = PIPE_IMG
        #for collision and ai 
        self.passed = False
        self.set_height()
    #randomizes the pipe pos   
    def set_height(self):
        #random height 
        self.height = random.randrange(50,450)
        #
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    #moves the pipe 
    def move(self):
        self.x -= self.VEL
        
    #creates the pipes 
    def draw(self,win):
        win.blit(self.PIPE_TOP, (self.x,self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    #uses mask for hit boxes
    def collide(self,bird):
        
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        #tells us the first point of collision 
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        return False