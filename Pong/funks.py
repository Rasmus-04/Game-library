import random

# Bestämmer om bollen ska börja gå uppåt eller nedåt
def ball_vel_ud():
    if random.randint(1,2) == 1:
        return 3
    else:
        return -3

# Bestämmer om bollen ska börja gå Höger eller vänster
def ball_vel_rl():
    if random.randint(1,2) == 1:
        return 4
    else:
        return -4
