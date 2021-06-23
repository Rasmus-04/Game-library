import pygame
import os
import random
#from Slutprojekt.flappy_birds.config import *

def reset():
    global run, death, FPS, HEIGHT, WIDTH, red, black, white, gray, aqua, green, orange, yellow, pipes, clouds, jump_timer, score
    run = True
    death = False
    FPS = 60
    HEIGHT, WIDTH = 650, 550

    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (192, 192, 192)
    aqua = (0, 128, 128)
    green = (0, 255, 0)
    orange = (255, 165, 0)
    yellow = (255, 255, 0)

    pipes = []
    clouds = []

    jump_timer = 0
    score = 0

def start_flappy_birds():
    global run, jump_timer, score
    reset()
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")

    path_to_assets_folder = "Flappy_birds\Assetes"

    bg_img = pygame.image.load(os.path.join(path_to_assets_folder, "bg.png"))
    bird_img = pygame.image.load(os.path.join(path_to_assets_folder, "bird.png"))
    bird_img_up = pygame.image.load(os.path.join(path_to_assets_folder, "bird_up.png"))
    bird_img_down = pygame.image.load(os.path.join(path_to_assets_folder, "bird_down.png"))
    pipe_img = pygame.image.load(os.path.join(path_to_assets_folder, "pipe.png"))
    cloud_img = pygame.image.load(os.path.join(path_to_assets_folder, "cloud.png"))

    class BIRD:
        def __init__(self, x, y, width, height, img):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.force = 50
            self.is_jump = False

        def draw(self):
            if self.is_jump and self.force > 0:
                self.img = bird_img_up
            elif self.is_jump and self.force < 0:
                self.img = bird_img_down
            else:
                self.img = bird_img
            win.blit(self.img, (self.x, self.y))

            #pygame.draw.rect(win, red, (self.x, self.y, self.width, self.height), 2)
            self.jump()

        def jump(self):
            if self.is_jump:
                self.y -= self.force
                self.force -= 0.5


    class PIPE:
        def __init__(self, x, y, width, height, img):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.vel = 2
            self.given_points = False

        def draw(self):
            win.blit(self.img, (self.x,self.y))
            self.move()
            #pygame.draw.rect(win, red, (self.x, self.y, self.width, self.height), 2)
            #pygame.draw.rect(win, red, (self.x, self.y + self.height + 180, self.width, self.height), 2)

        def move(self):
            if bird.is_jump:
                self.x -= self.vel

                if self.x + self.width <= 0:
                    self.given_points = False
                    self.x = WIDTH
                    self.y = random_y_value(-800, -480)


    class BACK_GROUND:
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img

        def draw(self):
            win.blit(self.img, (self.x, self.y))
            self.move()

        def move(self):
            if self.x <= -405:
                self.x = 0
            self.x -= 0.5



    class cloud:
        def __init__(self, x, y, width, height, img):
            self.x = x
            self.y = y
            self.img = img
            self.width = width
            self.height = height

        def draw(self):
            win.blit(self.img, (self.x, self.y))
            #pygame.draw.rect(win, red, (self.x, self.y, self.width, self.height), 2)
            self.move()

        def move(self):
            if self.x + 156 <= 0:
                self.x = WIDTH + 150
                self.y = random_y_value(5, 75)
            self.x -= 1.5


    def random_y_value(min, max):
        return random.randint(min, max)


    def death_screen():
        global run, death
        death = True

        bird.is_jump = True
        bird.force = 0
        for pipe in pipes:
            pipe.vel = 0


        while death:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    death = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r] and death:
                restart()

            if (bird.y + bird.height) >= (HEIGHT- 50):
                bird.is_jump = False

            re_draw()


    def write_text(txt, x=0, y=0, xmiddle=False, ymiddle=False, size=50, Bold=True, italic=False, txt_font="comicsans", color=white):
        fonts = pygame.font.SysFont(txt_font, size, Bold, False)
        text = font.render(txt, 1, color)

        if xmiddle:
            x = WIDTH//2 - text.get_width()//2

        if ymiddle:
            y = HEIGHT//2 - text.get_height()//2

        win.blit(text, (x,y))


    def write_high_score(score):
        with open("Flappy_birds\High_scores.txt", "w") as f:
            f.write(str(score))

    def get_high_score():
        with open("Flappy_birds\High_scores.txt", "r") as f:
            return int(f.read())


    def restart():
        global score, death

        #for pipe_index, pipe in enumerate(pipes):
        pipes[0].y = random_y_value(-800, -480)
        pipes[1].y = random_y_value(-800, -480)
        pipes[0].x = WIDTH
        pipes[1].x = WIDTH + WIDTH//2
        for pipe in pipes:
            pipe.given_points = False
        score = 0
        bird.is_jump = False
        bird.y = HEIGHT//2
        death = False
        for pipe in pipes:
            pipe.vel = 2



    def re_draw():
        BG.draw()

        for Cloud in clouds:
            Cloud.draw()

        bird.draw()

        for pipe in pipes:
            pipe.draw()

        if not death and bird.is_jump:
            write_text(f"Score: {score}", xmiddle=True, y=HEIGHT-32)

        if not bird.is_jump and not death:
            write_text("Press Space to start", xmiddle=True, y=HEIGHT//2 - 80)

        if death:
            write_text("Game Over", xmiddle=True, y=HEIGHT//2 - 100)
            write_text(f"Score: {score}", xmiddle=True, y=HEIGHT // 2 - 30)
            write_text("Press \"R\" to restart", xmiddle=True, y=HEIGHT//2 + 40)
            write_text(f"High Score: {get_high_score()}", xmiddle=True, y=HEIGHT-35)


        pygame.display.update()


    font = pygame.font.SysFont("comicsans", 50, True)


    BG = BACK_GROUND(0, -100, bg_img)
    bird = BIRD(100, HEIGHT//2, 45, 35, bird_img)

    # Set pipe y value between -480 at lowest and -800 at heighest
    pipes.append(PIPE(WIDTH, random_y_value(-800, -480), 82, 850, pipe_img))
    pipes.append(PIPE(WIDTH + WIDTH//2, random_y_value(-800, -480), 82, 850, pipe_img))


    for i in range(3):
        clouds.append(cloud(WIDTH + i*300, random_y_value(5, 75), 150, 100, cloud_img))

    restart()


    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        re_draw()

        if jump_timer > 0:
            jump_timer -= 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and jump_timer <= 0 and bird.y > 0:
            bird.is_jump = True
            bird.force = 8
            jump_timer = 10


        if bird.y > HEIGHT:
            death_screen()

        for pipe in pipes:
            if bird.x >= pipe.x + pipe.width and not pipe.given_points:
                pipe.given_points = True
                score += 1

            if (bird.x + bird.width) > pipe.x and (pipe.x + pipe.width) > bird.x:
                if bird.y < (pipe.y + pipe.height) or (pipe.y + pipe.height + 180) < (bird.y + bird.height):
                    bird.is_jump = False
                    death_screen()


        if score > get_high_score():
            write_high_score(score)


    pygame.font.quit()
    pygame.quit()
