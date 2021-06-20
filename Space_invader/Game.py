import os.path
import time
import pygame
import random
from Slutprojekt.Space_invader.config import *


def space_invader_game():
    global run, score, status, enemy_list, bullets, timer, enemy_vel, player_vel, boss_state, boss_start_health
    global enemy_count, get_high_score, points_until_new_enemy, bullet_count, wave

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.Channel(1).set_volume(0.1)


    # Skapar fönstret
    win = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Space Invaders")
    win.fill(WHITE)

    CLOCK = pygame.time.Clock()

    # Laddar in alla bilder
    if __name__ == "__main__":
        path_to_folder = "Assets"
        high_score_file_path = "high_scores.txt"
    else:
        path_to_folder = "Space_invader\Assets"
        high_score_file_path = "Space_invader\high_scores.txt"

    bg_img = pygame.image.load(os.path.join(path_to_folder, "space_invaders_background.gif"))
    player_img = pygame.image.load(os.path.join(path_to_folder, "player.gif"))
    audio_on_img = pygame.image.load(os.path.join(path_to_folder, "audio_on.png"))
    audio_off_img = pygame.image.load(os.path.join(path_to_folder, "audio_off.png"))
    menu_img = pygame.image.load(os.path.join(path_to_folder, "menu.png"))

    for i in range(3):
        invader_img.append(pygame.image.load(os.path.join(path_to_folder, f"invader{i}.gif")))
        boss_img.append(pygame.image.load(os.path.join(path_to_folder, f"Boss_{i}.png")))



    # Klasser
    class PLAYER:
        def __init__(self, x, y, height, width):
            self.x = x
            self.y = y
            self.height = height
            self.width = width

        def draw(self):
            # Ritar spelaren
            win.blit(player_img, (self.x, self.y, self.width, self.height))
            self.move()

        def move(self):
            # Flyttar spelaren
            self.x += player_vel


    class ENEMY:
        def __init__(self, x, y, height, width, vel, img):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.vel = vel
            self.img = img

        def draw(self):
            # Ritar Spelaren
            win.blit(self.img, (self.x, self.y))
            self.move()

        def move(self):
            # Flyttar Spelaren
            self.y += self.vel


    class BOSS:
        def __init__(self, x, y, height, width, health=boss_start_health):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.vel = 2
            self.timers = 0
            self.health = health

        def draw(self):
            if boss_state:
                # Ändrar färg på bossen beronde på hur mycket hp den har kvar
                if self.health > boss_start_health * 0.6:
                    self.img = boss_img[0]
                elif self.health > boss_start_health * 0.3:
                    self.img = boss_img[1]
                else:
                    self.img = boss_img[2]

                # Ritar bossen
                win.blit(self.img, (self.x, self.y))
                pygame.draw.rect(win, RED, (self.x, self.y - 20, self.width, 10))
                pygame.draw.rect(win, GREEN, (self.x, self.y - 20, self.width * (self.health/boss_start_health), 10))

                # Hitbox
                self.move()

        def move(self):
            # Flytar på bossen
            if self.y <= 300:
                self.y += 2
            else:
                if self.x < 100:
                    self.vel = 2
                elif self.x > (700 - self.width):
                    self.vel = -2
                self.x += self.vel

                self.fire()

        def fire(self):
            # Sjuter
            if len(boss_bullets) < 5:
                if self.timers <= 0:
                    boss_bullets.append(BULLET(boss.x + boss.width//2 - 5, boss.y + boss.height, 10, 10, 3))
                    self.timers = 50
                self.timers -= 1


    class BULLET:
        def __init__(self, x, y, height, width, vel):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.vel = vel

        def draw(self):
            # Ritar skotten
            pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))
            self.move()

        def move(self):
            # Flyttar skotten
            self.y += self.vel


    class buttons:
        def __init__(self, img, x, y, width, height, func):
            self.x = x
            self.y = y
            self.img = img
            self.width = width
            self.height = height
            self.func = func
            self.pressed_state = False

        def draw(self):
            if not self.pressed_state:
                win.blit(self.img, (self.x, self.y))
            else:
                win.blit(self.img, (self.x, self.y))

            # Audio button hitbox
            pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height), 2)

            self.check_klick()

        def check_klick(self):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if mouseX > self.x and (mouseX < self.x + self.width):
                        if mouseY > self.y and (mouseY < self.y + self.height):
                            self.func()



    def draw_bullet():
        for index, bullet in enumerate(bullets):
            # Om skottet är högst upp på skärmen så försvinner skottet
            if bullet.y < 100:
                bullets.pop(index)
            # Ritar skotten
            bullet.draw()


    def start_meny():
        global run
        start = False

        while not start:
            # kollar om användaren vill stänga av
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    start = True

                # kollar om användaren klickar på en mus knapp
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    start = True
                    redraw_window()

            # skriver text på skärmen
            win.fill(BLACK)
            draw_text("press any mouse button to start", 0, 0, 60, "comicsans", True, False, True, True)
            pygame.display.update()




    # Spelar upp ljud
    def play_sound(sound_file):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(path_to_folder, f"{sound_file}.wav")))
        #pygame.mixer.Channel(1).set_volume(0.1)


    # Skriver text på skärmen
    def draw_text(txt, x=0, y=0, size=30, font="comicsans", Bold=True, Italic=True, middle_x=False, middle_y=False):
        font = pygame.font.SysFont(font, size, Bold, Italic)
        text = font.render(txt, 1, WHITE)
        if middle_x:
            x = WIDTH // 2 - text.get_width() // 2
        if middle_y:
            y = HEIGHT // 2 - text.get_height() // 2
        win.blit(text, (x, y))


    def game_over():
        player.y = -1000
        bullets.clear()
        draw_text(f"Current High Score: {get_high_score()}", 0, 130, 50, "comicsans", True, False, True)
        draw_text(f"Your Score: {score:02d}", 0, BORDER // 2, 70, "comicsans", True, False, True)
        draw_text("GAME OVER", 0, 0, 100, "comicsans", True, False, True, True)
        draw_text('Press "R" To Play Agin', 0, HEIGHT//2.4 + BORDER //5, 50, "comicsans", True, False, True)


    # Skapar invadersna
    def create_enemys():
        if status == "on":
            for enemy in range(enemy_count):
                enemy_list.append(ENEMY(enemy_randomx(), enemy_randomy(), 25, 25, enemy_vel, enemy_color()))


    def reset_boss():
        boss_bullets.clear()
        boss.health = boss_start_health
        boss.y = 100
        boss.x = 357.5


    # sätter alla värden till start värderna
    def reset():
        global run, score, status, enemy_count, timer, bullet_count, points_to_enemy, boss_bullets
        global player_vel, points_until_new_enemy, enemy_vel, wave, boss_state, boss_start_health
        run = True
        boss_state = False
        player.x = WIDTH//2 - 12.5
        player.y = BORDER + 50
        status = "on"
        player_vel = 0
        enemy_list.clear()
        bullets.clear()
        boss_bullets.clear()
        enemy_count = 5
        score = 0
        timer = 0
        wave = 1
        enemy_vel = 0.5
        points_to_enemy = 100
        boss_start_health = 100
        points_until_new_enemy = points_to_enemy
        bullet_count = 5
        reset_boss()
        create_enemys()
        redraw_window()


    def pause():
        global run

        # Skriver paused på skärmen
        draw_text("PAUSED", 0, 0, 150, "comicsans", True, False, True, True),
        draw_text('Press "P" to un pause', 0, HEIGHT//2 + 75, 50,"comicsans", True, False, True, False)
        pygame.display.update()
        time.sleep(0.2)
        paused = True

        # kollar om användaren vill stänga av
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    paused = False

            # Kollar om spelaren vill sluta pausea
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:
                paused = False


    # Updaterar High score filen
    def update_high_score(score):
        with open(high_score_file_path, "w") as f:
            f.write(score)

    # Returnar ditt high score
    def get_high_score():
        with open(high_score_file_path, "r") as f:
            return int(f.read())

    # Ger random x värde för invaders
    def enemy_randomx():
        return random.randint(120, WIDTH - 140,)

    # Ger random y värde för invaders
    def enemy_randomy():
        return random.randint(110, 210)

    # Ger invaders deras färg
    def enemy_color():
        x = random.randint(1, 10)
        if x == 10:
            return invader_img[2]
        elif x > 6:
            return invader_img[1]
        else:
            return invader_img[0]

    def switch_audio():
        if audio_button.pressed_state:
            audio_button.pressed_state = False
            audio_button.img = audio_on_img
            pygame.mixer.Channel(1).set_volume(0.1)
        else:
            audio_button.pressed_state = True
            audio_button.img = audio_off_img
            pygame.mixer.Channel(1).set_volume(0)


    # Updaterar skärmen
    def redraw_window():
        # ritar bakgrunden
        win.blit(bg_img, (0, 0))

        # ritar spelaren
        player.draw()

        # Ritar invadersna
        for enemy in enemy_list:
            enemy.draw()
        draw_bullet()

        # om spelet pågår ritar den detta
        if status == "on":
            draw_text(f"Current High Score: {get_high_score()}", 0, 30, 30, "comicsans", True, False, True)
            draw_text(f"Score: {score:02d}", 120, 80)
            draw_text(f"Bullets {bullet_count}/{bullet_count-len(bullets)}", 550, 80)
            draw_text(f"Wave: {wave}", y=700, Italic=False, middle_x=True)

            # om man möter en boss så vissas detta
            if boss_state:
                draw_text("Boss", y=720, Italic=False, middle_x=True)

        if status == "over":
            game_over()

        audio_button.draw()
        meny_button.draw()

        # Om man möter en boss så ritas bossen och bossen skott
        if boss_state:
            boss.draw()
            for bullet in boss_bullets:
                bullet.draw()

        pygame.display.update()


    # Skapar Spelarna
    player = PLAYER(WIDTH//2 - 12.5, BORDER + 50, 25, 25)
    boss = BOSS(357.5, 100, 85, 85)
    audio_button = buttons(audio_on_img, audio_pos_x, audio_pos_y, audio_icon_width, audio_icon_height, switch_audio)
    meny_button = buttons(menu_img, WIDTH - 55, audio_pos_y, 50, 50, pause)


    reset()
    start_meny()

    while run:
        CLOCK.tick(FPS)
        redraw_window()

        # Kollar om användaren vill stänga av
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if timer != 0:
            timer -= 1

        # Updaterar high scoren om spelarens poäng är högre än det nuvarand high scoret
        if score > get_high_score():
            update_high_score(str(score))


        # Kollar efter kollision mellan invaders och spelarens skott
        for enemy_index, enemy in enumerate(enemy_list):
            for bullet_index, bullet in enumerate(bullets):
                if bullet.y > enemy.y and (bullet.y + bullet.height) < (enemy.y + enemy.height * 1.2):
                    if (bullet.x + bullet.width) > enemy.x and (bullet.x) < (enemy.x + enemy.width):
                        play_sound("explosion")
                        bullets.pop(bullet_index)

                        if enemy.img == invader_img[0]:
                            score += 10
                        elif enemy.img == invader_img[1]:
                            score += 20
                        else:
                            score += 30

                        enemy_list.pop(enemy_index)


        # Kollar om invaders är längs ner på fönstret
        for enemy_index, enemy in enumerate(enemy_list):
            if enemy.y > (BORDER + 100 - enemy.height):
                enemy_list.pop(enemy_index)
                if status == "on":
                    play_sound("explosion")
                status = "over"

            # Kollar om invader träffar spelaren
            elif player.x < (enemy.x + enemy.width) and (player.x + player.width) > enemy.x and status == "on":
                if (enemy.y + enemy.height - 10) > player.y:
                    enemy_list.pop(enemy_index)
                    if status == "on":
                        play_sound("explosion")
                    status = "over"


        # Key binds
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x > 103:
            player_vel = -start_player_vel

        if player.x < 100 and player_vel < 0:
            player_vel = 0


        if keys[pygame.K_RIGHT] and player.x < BORDER + 97 - player.width:
            player_vel = +start_player_vel

        if player.x > (BORDER + 100 - player.width) and player_vel > 0:
            player_vel = 0


        if keys[pygame.K_SPACE] and len(bullets) < bullet_count and timer == 0 and status == "on":
            bullets.append(BULLET(player.x + player.width//2 - 5, player.y, 10, 10, -3))
            play_sound("laser")
            timer = 5

        if keys[pygame.K_p] and status == "on":
            pause()
            time.sleep(0.2)

        if keys[pygame.K_r] and status == "over":
            reset()

        # Varje 100 poäng så får spelaren en till bullet
        if score >= points_until_new_enemy:
            points_until_new_enemy += points_to_enemy
            bullet_count += 1

        # var femte wave så möter spelaren en boss
        if wave % 5 == 0 and status == "on" and not boss_state:
            boss_state = True
            enemy_list.clear()
            bullets.clear()

        # Om man inte möter en boss och har dödat alla invaders så skapas 2 mer invaders och deras speed ökar med 10%
        if not boss_state:
            if len(enemy_list) == 0:
                enemy_count += 2
                enemy_vel += 0.05
                wave += 1
                bullets.clear()
                create_enemys()

        # om man möter en boss
        if boss_state:
            # Kollar om bossens skott är längs ner på fönsteret
            for bullet_index, bullet in enumerate(boss_bullets):
                if bullet.y > (700 - bullet.height):
                    boss_bullets.pop(bullet_index)

                # Kollar im bossen skott har träffat spelaren
                if player.x < (bullet.x + bullet.width) and (player.x + player.width) > bullet.x:
                    if (bullet.y + bullet.height - 10) > player.y:
                        game_over()
                        status = "over"
                        boss_state = False

            # Kollar om spelarens skott träffar bossen
            for bullet_index, bullet in enumerate(bullets):
                if bullet.x > boss.x and (bullet.x + bullet.width) < (boss.x + boss.width):
                    if bullet.y < (boss.y + boss.height) and (bullet.y + bullet.height) > boss.y:
                        bullets.pop(bullet_index)
                        play_sound("explosion")
                        score += 20
                        boss.health -= 10

                    if boss.health == 0:
                        wave += 1
                        boss_start_health += 100
                        boss_state = False
                        boss_bullets.clear()
                        bullets.clear()
                        create_enemys()
                        reset_boss()
                        break
    reset()
    pygame.quit()


if __name__ == "__main__":
    space_invader_game()