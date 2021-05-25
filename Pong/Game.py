import pygame
from Slutprojekt.Pong.config import *
from Slutprojekt.Pong.funks import *


# Start fönsteret
def Start_pong():
    global win

    # Skapar spel fönstret
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.font.init()
    Font = pygame.font.SysFont("comicsans", 40, True, True)

    # Start skärmen
    def redrawStart():
        # Fyller skärmen svart
        win.fill(BLACK)
        
        # Texten som visas i mitten av skärmen
        Starttext = Font.render("Press any mouse button to start!", 1, WHITE)
        win.blit(Starttext, (WIDTH // 2 - Starttext.get_width() // 2, HEIGHT // 2 - Starttext.get_height()//2))
        
        # Updaterar skärmen
        pygame.display.update()

    
    def start_window():
        Start = True
        redrawStart()
        while Start:
            # Kollar om användaren vill stänga ner spelet
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Start = False

            # Kolla om användaren klickade på musen
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                Start = False
                pong()

    start_window()
    pygame.quit()


# Spelet
def pong():
    p1score, p2score = 0,0
    run = True
    CLOCK = pygame.time.Clock()


    # Classes
    class PLAYER:
        def __init__(self, x, y, Width, Height, vel):
            self.x = x
            self.y = y
            self.Width = Width
            self.Height = Height
            self.vel = vel

        def draw(self):
            # Ritar spelaren
            self.hitbox = (self.x - 2, self.y, 12, 40)
            pygame.draw.rect(win, WHITE, (self.x, self.y, self.Width, self.Height))


    class BALL:
        def __init__(self, x, y, radius, xvel, yvel):
            self.x = x
            self.y = y
            self.radius = radius
            self.xvel = xvel
            self.yvel = yvel

        def draw(self):
            # Ritar bollen
            self.hitbox = (self.x - 10, self.y - 10, 20, 20)
            pygame.draw.circle(win, WHITE, (self.x, self.y, ), self.radius)

        def move(self):
            # Flyttar bollen
            self.x += self.xvel
            self.y += self.yvel


    def reset():
        # Flyttar spelarna och bollen där dom började
        ball.x = WIDTH//2
        ball.y = HEIGHT//2
        p1.y = HEIGHT//2 - 20
        p2.y = HEIGHT//2 - 20
        redraw_window()
        pygame.time.delay(500)


    def redraw_window():
        # Fyller skärmen med svart
        win.fill(BLACK)

        # Spelarnas poäng
        p1Scores = font.render(f"P1 Score {p1score}", 1, WHITE)
        p2Scores = font.render(f"P2 Score {p2score}", 1, WHITE)
        win.blit(p1Scores, (30, 10))
        win.blit(p2Scores, (WIDTH - p1Scores.get_width() - 30, 10))

        # Ritar spelarna och bollen
        p1.draw()
        p2.draw()
        ball.draw()

        # Updaterar skärmen
        pygame.display.update()


    # Font
    font = pygame.font.SysFont("comicsans", 20, True, True)


    # Player
    p1 = PLAYER(10, HEIGHT//2 - 20, 10, 40, 5)
    p2 = PLAYER(WIDTH - 20, HEIGHT//2 - 20, 10, 40, 5)
    ball = BALL(WIDTH//2, HEIGHT//2, 8, ball_vel_rl(), ball_vel_ud())

    redraw_window()
    pygame.time.delay(500)

    # main Loop
    while run:
        CLOCK.tick(FPS)
        redraw_window()

        # Kollar om användaren vill stänga av
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        ball.move()
        keys = pygame.key.get_pressed()

        #       Player 1 colistion
        # Kollar om bollen och player 1 har samma x värde
        if p1.hitbox[0] + p1.Width*2 > ball.hitbox[0]:
            # Kollar om bollen och spelaren har samma y värde
            if p1.hitbox[1] < ball.hitbox[1] + p1.Height//2 and p1.hitbox[1] + p1.Height > ball.hitbox[1]:
                # Byter håll på bollen
                ball.xvel = abs(ball.xvel)

        #       Player 2 colistion
        # Kollar om bollen och player 2 har samma x värde
        if p2.hitbox[0] - p2.Width*2 < ball.hitbox[0]:
            # Kollar om bollen och spelaren har samma y värde
            if p2.hitbox[1] < ball.hitbox[1] + p2.Height//2 and p2.hitbox[1] + p2.Height > ball.hitbox[1]:
                # Byter håll på bollen
                if ball.xvel > 0:
                    ball.xvel = -ball.xvel


        # Kollar om bollen är i mål
        if ball.hitbox[0] < 0:
            # Byter håll på bollen
            ball.xvel = abs(ball.xvel)
            ball.yvel = ball_vel_ud()
            # Ger poäng till spelaren
            p2score += 1
            # Sätter bollen i mitten
            reset()

        # Kollar om bollen är i mål
        if ball.hitbox[0] + ball.radius*2 > WIDTH:
            # Byter håll på bollen
            ball.xvel = -ball.xvel
            ball.yvel = ball_vel_ud()
            # Ger poäng till spelaren
            p1score += 1
            # Sätter bollen i mitten
            reset()


        # collar om bollen är högst upp eller längst ner på skärmen
        if ball.hitbox[1] < 0:
            # Bytter håll på bollen
            ball.yvel= abs(ball.yvel)

        if (ball.hitbox[1] + ball.radius*3) > HEIGHT:
            # Byter håll på bollen
            if ball.yvel > 0:
                ball.yvel = -ball.yvel


        # Keybinds
        if keys[pygame.K_w] and p1.y > 0:
            p1.y -= p1.vel
        if keys[pygame.K_s] and p1.y < HEIGHT - p1.Height:
            p1.y += p1.vel

        if keys[pygame.K_UP] and p2.y > 0:
            p2.y -= p2.vel

        if keys[pygame.K_DOWN] and p2.y < HEIGHT - p2.Height:
            p2.y += p2.vel

    pygame.quit()


if __name__ == "__main__":
    Start_pong()
