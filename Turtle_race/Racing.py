import turtle
import random
import time


def game_turle_race(players):
    turtle.TurtleScreen._RUNNING = True

    # Skapar Fönstret
    WIDTH, HEIGHT = 500, 500
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing!")
    screen.clear()

    # Färger
    COLORS = ["red", "green", "blue", "orange", "yellow", "black", "purple", "pink", "brown", "cyan"]
    random.shuffle(COLORS)
    colors = COLORS[:players]


    def race(colors):
        # Skapar spelarna
        turtles = create_turtle(colors)

        while True:
            # Flyttar fram spelaren
            for racer in turtles:
                distance = random.randint(1, 20)
                racer.forward(distance)

            # Kollar om någon har vunnit
            for racer in turtles:
                x, y = racer.pos()
                if y >= HEIGHT //2 - 15:
                    winnery = 0
                    for race in turtles:
                        if y > winnery:
                            winnery = y
                            winner_color = colors[turtles.index(racer)]
                    return winner_color


    def create_turtle(colors):
        turtles = []

        # Bestämer hur långt ifrån spelarna ska vara
        spacingx = WIDTH // (len(colors) + 1)

        # Skapar spelarna
        for i, color in enumerate(colors):
            racer = turtle.Turtle()
            racer.color(color)
            racer.shape("turtle")
            racer.setheading(90)
            racer.penup()
            racer.setpos(-WIDTH//2 + (i+1) * spacingx, -HEIGHT//2 + 20)
            racer.pendown()
            turtles.append(racer)

        return turtles


    # Kör race
    winner = race(colors)
    time.sleep(0.5)

    # Skriver vilken färg van på skärmen
    screen.clear()
    score_pen = turtle.Turtle()
    score_pen.hideturtle()
    score_pen. penup()
    score_pen.color(str(winner))
    score_pen.setposition(180, 0)
    score_pen.write(f"The Winning color is {winner.capitalize()}", False, align="right", font=("Arial", 25, "normal"))
    return winner


if __name__ == "__main__":
    print(f"The winner is: {game_turle_race(int(input('Enter amount of players: ')))}")
    time.sleep(1)
