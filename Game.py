import pygame
import random
import sys
import neat
pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800






BIRD_IMG = pygame.image.load("assets/bird1.png")
BIRD_WIDTH = 45  # Desired width of the bird sprite
BIRD_HEIGHT = 45  # Desired height of the bird sprite
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (BIRD_WIDTH, BIRD_HEIGHT))

PIPE_IMG = pygame.image.load("assets/pipe.png")
PIPE_WIDTH = 70  # Desired width of the pipe sprite
PIPE_HEIGHT = 600  # Desired height of the pipe sprite
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (PIPE_WIDTH, PIPE_HEIGHT))


BASE_IMG = pygame.image.load("assets/base.png")
new_width = 800  # Desired new width
BASE_IMG = pygame.transform.scale(BASE_IMG, (new_width, BASE_IMG.get_height()))

GEN=int(0)

BG_IMG = pygame.image.load("assets/bg.png")

STAT_FONT =pygame.font.SysFont("comicsans",50)



WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


class Bird:
    IMG = BIRD_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = y
        self.vel = 0
        self.img = BIRD_IMG
        self.tick_count = 0

    def jump(self):
        self.vel =-10
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if(d < 0):
            d -= 2

        self.y = self.y + d

    def draw(self, win):
        new_rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.img, (new_rect.topleft))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP=500
    VEL=5
    
    def __init__(self,x):
        self.x=x
        self.height=WIN_HEIGHT
        self.gap=180

        self.top=0
        self.bottom=0
        self.PIPE_TOP=pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM=PIPE_IMG

        self.passed=False
        self.set_height()

    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.bottom=self.height+self.gap


    def move(self):
        self.x -= self.VEL


    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask=bird.get_mask()
        top_mask= pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask= pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset=(self.x-bird.x,self.top-round(bird.y))
        bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))

        b_point=bird_mask.overlap(bottom_mask,bottom_offset)
        t_point=top_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True

        return False



class Base:
    VEL=5
    WIDTH=BASE_IMG.get_width()
    IMG=BASE_IMG

    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1+ self.WIDTH <0:
            self.x1=self.x2+self.WIDTH

        if self.x2+ self.WIDTH <0:
            self.x2=self.x1+self.WIDTH    

           
    def draw(self,win):
       win.blit(self.IMG,(self.x1,self.y))
       win.blit(self.IMG,(self.x2,self.y))







def draw_window(win, birds, pipes, base, score):
    scaled_bg = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))
    win.blit(scaled_bg, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text=STAT_FONT.render("Score: "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
    base.draw(win)

    for bird in birds:
      bird.draw(win)

    pygame.display.update()





def main(genomes,config):


    

    nets=[]
    ge=[]
    birds = []

    best_genome = None  # Variable to store the best genome
    best_fitness = 0 



    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness=0
        ge.append(g)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock= pygame.time.Clock()
    run = True
    score=0
    base=Base(730)
    pipes=[Pipe(700)]

    


    while run and len(birds) >0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                if best_genome is not None:
                 with open("best_genome.txt", "w") as file:
                   file.write(str(best_genome))
                print(str(best_genome))
                pygame.quit()
                quit()
                break


        pipe_ind=0
        if len(birds)>0:
           if len(pipes)>1 and birds[0].x > pipes[0].x +pipes[0].PIPE_TOP.get_width():
             pipe_ind=1

      

        for x,bird in enumerate(birds):
          ge[x].fitness+=0.1
          bird.move()


          output=nets[birds.index(bird)].activate((bird.y,abs(bird.y-pipes[pipe_ind].height),abs(bird.y-pipes[pipe_ind].bottom)))

          if output[0] >0.5:
            bird.jump()



        for x, g in enumerate(ge):
            if g.fitness > best_fitness:
                best_genome = g
                best_fitness = g.fitness

        base.move()


        add_pipe=False
        rem=[]
        for pipe in pipes:
            pipe.move()

            for x,bird in enumerate(birds):
             if pipe.collide(bird):
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

            if not pipe.passed and pipe.x<bird.x :
                pipe.passed=True 
                add_pipe=True  

            if pipe.x+pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)

        

        if add_pipe:
            for g in ge:
                g.fitness += 5 
            score+=1
            pipes.append(Pipe(600))


        for r in rem:
          pipes.remove(r)

        for x,bird in enumerate(birds):
         if bird.y+bird.img.get_height()>=730 or bird.y<0:
            ge[x].fitness -= 1
            birds.pop(x)
            nets.pop(x)
            ge.pop(x)


        draw_window(win, birds, pipes, base,score)

   

    


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                               neat.DefaultSpeciesSet, neat.DefaultStagnation,
                               config_path)
    p=neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    winner=p.run(main,50)





if __name__ == "__main__":
    config_path="config.txt"
    run(config_path)