import pygame
import neat 
import os
import Bird
import Floor 
import Pipe 

pygame.font.init()
#Constant variables are in all caps 
#screen config 
WIN_WIDTH = 530#pixels
WIN_HIGHT = 800#pixels 
GEN_NUM  = 0


#background image variable deceleration and initialization
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("arial",50)
 

#Just creates the screen         
def draw_window(win,birds,pipes,floor,score,gen):
    win.blit(BG_IMG,(0,0))
    
    for pipe in pipes:
        pipe.draw(win)
    score = STAT_FONT.render("Score:" + str(score),1,(255,255,255))
    win.blit(score,(WIN_WIDTH-10 - score.get_width(),10))
    gen_text = STAT_FONT.render("Gen:" + str(gen),1,(255,255,255))
    win.blit(gen_text,(10,10))
    floor.draw(win)
    
    for bird in birds:
        bird.draw(win)
        
    pygame.display.update()

#main game method and also the neat fitness function
#NOTE: all neat fitness functions need gnomes and config as parameters
def main(genomes, config):
    currentGen = 1
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HIGHT))
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird.Bird(230,350))
        ge.append(genome)

    floor = Floor.Floor(730)
    pipes = [Pipe.Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)#Frames per sec change this to make simulation faster or slower 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_index = 1                                                                 # pipe on the screen for neural network input

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.flap()

        floor.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe.Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= 730 or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(win,birds, pipes,floor, score, currentGen)

# Artificial intel part 
def run(config_path):
    
    # looks in the config file for settings 
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet
                                ,neat.DefaultStagnation, config_path)
    
    #sets the population size to whatever the size is in the config file
    population = neat.Population(config)
    #adds a report to the terminal for more information
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    # 50 = how many generates are we going to run 
    #calls the main function 50 times 
    winner = population.run(main,100)
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
#neat config file import and sets the fiction function which is out main method

if __name__ == "__main__":
    #sets the local dir to the dir we are in
    local_dir = os.path.dirname(__file__)
    config = os.path.join(local_dir, "config-flappy.txt")
    run(config)
