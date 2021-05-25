# Fönstrets mått
HEIGHT, WIDTH = 800, 800
BORDER = 600

# Färger
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (4, 51, 255)
GREEN = (0, 255, 0)

# Spel state
run = True
boss_state = False
status = "on"

# Listor
enemy_list = []
bullets = []
invader_img = []
boss_img = []
boss_bullets = []

# Variabler
enemy_count = 5
boss_start_health = 100
enemy_vel = 0.5
points_to_enemy = 100
points_until_new_enemy = points_to_enemy
bullet_count = 5
player_vel = 0
start_player_vel = 5
FPS = 60
score = 0
timer = 0
wave = 1
