import pygame
import os 

#adds the bird img as a variable and makes it 2x as big
#bird imgs is an array of different pictures of the bird in different movement stages 
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

class Bird:
    #Array of jpgs
    IMGS = BIRD_IMG
    
    #tilt
    MAX_ROTATION = 25
    
    # how much rotation per frame
    ROTATION_VELOCITY = 20
    
    #Time in milliseconds each frame is shown 
    ANIMATION_DURATION = 5
    
    def __init__(self,x,y):
        #x and y pos of bird
        self.x = x
        self.y = y
        #base bird tilt
        self.tilt = 0
        #used for gravity and jump cool down
        self.seconds_count = 0
        #velocity/speed of bird
        self.vel = 0
        #current height of bird
        self.height = self.y
        #current animation state of bird
        self.img_count = 0
        self.img = self.IMGS[0]
    
    #flap method makes the bird fly 
    def flap(self):
        #in order to go up number must be a negative
        self.vel = -10.5
        #set current time between "flaps" to 0 
        self.seconds_count = 0
        #gets the origin point of the bird 
        self.height = self.y
    
    #called every frame because its flappy bird 
    def move(self):
        self.seconds_count += 1
        #this equation tells us how much our bird is moving up or down
        #displacement = self.vel * (self.seconds_count) + 0.5(3) * (self.seconds_count)**2
        displacement = self.vel*(self.seconds_count) + 0.5*(3)*(self.seconds_count)**2  # calculate displacement
        #velocity caps 
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        if  displacement < 0:
            displacement -= 2
        #change the y position of the bird based off the displacement
        self.y = self.y + displacement
        #used for arching the bird aka momentum
        if displacement < 0 or self.y < 0 < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        #if we are not moving upwards move the bird down        
        else:
            #rotate 90 degrees
            if self.tilt > -90:
                self.tilt = self.ROTATION_VELOCITY
    #show it
    def draw(self,win):
        self.img_count += 1
        #changes the animation after a certain amount of time 
        if self.img_count < self.ANIMATION_DURATION:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_DURATION *2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_DURATION *3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_DURATION *4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_DURATION *4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_DURATION*2
        #rotate the image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        #moves the rotator to the center of the image 
        new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)
        
      #collision detection
    def get_mask(self):
        return pygame.mask.from_surface(self.img)