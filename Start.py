from Slutprojekt.Pong.Game import *
from Slutprojekt.Turtle_race.Racing import *
from Slutprojekt.Game_of_40.Game import *
from Slutprojekt.Space_invader.Game import *
from Slutprojekt.Tetris.tetris import *
from os import path


# Bilderna
icon_img = path.join("Assets", "icon.ico")
pong_img = path.join("Assets", "Pong_img.png")
turtle_race_img = path.join("Assets", "Turtle_img.png")
game_of_40_img = path.join("Assets", "Game_of_40.png")
space_invader_img = path.join("Assets", "Space_invader.png")


# Funktioner
# Kollar high scores för Space invaders
def get_high_scores():
    with open(path.join("Space_invader", "high_scores.txt"), "r") as f:
        return str(f.read())


# öppnar nytt fönster och stänger det förra
def open_win(open, close):
    close.destroy()
    open()


# skapar en label
def lbl(txt, r, c, win, back_gr="white", for_g="black", rspan=1, cspan=2, big_text=True):
    """
    :param txt: Texten som ska visas
    :param r: Vilken rad
    :param c: Vilken kolumn
    :param win: I vilket fönster det ska visas
    :param back_gr: Bakgrundsfärgen
    :param for_g: Text färgen
    :param rspan: Hur många rader texten ska ta upp
    :param cspan: Hur många kolumner texten ska ta up
    :param big_text: Om det ska vara stor text eller vanlig
    """
    lbl = Label(win, text=txt, bg=back_gr, fg=for_g)
    if big_text:
        lbl.config(font=("Courier", 20))
    lbl.grid(row=r, column=c, columnspan=cspan, rowspan=rspan)


# Skapar en knapp
def btn(txt, r, c, x=0, y=0, win="root", com=0, cspan=1):
    """
    :param txt: Texten som ska visas på knappen
    :param r: Vilken rad
    :param c: Vilken kolumn
    :param x: Hur bredd knappen ska vara
    :param y: Hur hög knappen ska vara
    :param win: Vilket fönster knappen ska visas i
    :param com: Funktionen som ska hönda när knappen klickas på
    :param cspan: Hur många kolumner knappen ska ta upp
    """
    btn = Button(win, text=str(txt), bg="white", command=com)
    btn.grid(row=r, column=c, ipadx=x, ipady=y, pady=10, padx=5, columnspan=cspan)


# Kollar antal spelare
def check_players(players):
    """
    :param players: Hur många spelare man vill tävla
    """
    # Kollar om inputen är en siffra
    try:
        players = int(players)
        # kollar om spelaren valde ett nummer mellan 2 och 10
        if 2 <= players <= 10:
            # tar bort texten från text rutan
            e.delete(0, END)
            text.configure(text="Waiting for results...")
            # startar spelet
            winner = game_turle_race(players)
            # visar vinnaren
            text.configure(text=f"The winner is the turtle with the color: {winner.capitalize()}")
        else:
            text.configure(text="The number must be between 2 and 10")

    # om inputen inte är en siffra:
    except:
        # Ändrar texten
        text.configure(text="Must be a number!")
    # Tar bort det som står i text rutan
    e.delete(0, END)


# Start sidan
def start_menu():
    # Skapar fönstret
    root = Tk()
    root.iconbitmap(icon_img)
    root.title("Game Library")
    root.geometry("194x500")
    root.config(bg="white")

    # Texten som visas över alla knappar
    lbl("Game Libary", 0, 0, root)

    # Skapar alla knappar
    btn("Pong", 1, 0, 26, 10, root, Start_pong)
    btn("Info", 1, 1, 25, 10, root, lambda: open_win(pong_info, root))
    btn("Turtle Race", 2, 0, 11, 10, root, lambda: open_win(turtle_race, root))
    btn("Info", 2, 1, 25, 10, root, lambda: open_win(turtle_race_info, root))
    btn("Game of 40", 3, 0, 10, 10, root, start_game_of_40)
    btn("Info", 3, 1, 25, 10, root, lambda: open_win(game_of_40_info, root))
    btn("Space Invader", 4, 0, 4, 10, root, space_invader_game)
    btn("Info", 4, 1, 25, 10, root, lambda: open_win(space_invader_info, root))
    btn("Game", 5, 0, 25, 10, root, main_menu)
    btn("Info", 5, 1, 25, 10, root)
    btn("Game", 6, 0, 25, 10, root)
    btn("Info", 6, 1, 25, 10, root)
    btn("Exit", 7, 0, 76, 10, root, exit, 2)
    root.mainloop()


# Alla info sidor:

def pong_info():
    # Skapar fönstret för pong info sidan
    info = Tk()
    info.iconbitmap(icon_img)
    info.title("Pong Info")
    info.geometry("576x520")
    info.config(bg="black")

    # Bilden som visar hur spelet ser ut
    photo = PhotoImage(file=pong_img).zoom(2).subsample(3)
    pong_photo = Label(info, image=photo)
    pong_photo.grid(row=1, column=1, columnspan=1)

    # Texten som visas högst upp
    lbl("Pong info", 0, 1, info, "black", "white", 1, 1)

    # Knappar för Back och Play:
    btn("Back", 0, 0, 20, 10, info, lambda:open_win(start_menu, info))
    btn("Play", 0, 2, 23, 10, info, Start_pong)

    # Texten som beskriver hur man spelar
    lbl("Pong is a 2 Player game.", 2, 1, info, "black", "white", 1, 1, False)
    lbl('To score you need to get the ball past your oppenent.', 3, 1, info, "black", "white", 1, 1, False)
    lbl('Player 1 Controlls | Player 2 controlls', 4, 1, info, "black", "white", 1, 1, False)
    lbl('UP: "W" |   UP: "↑"', 5, 1, info, "black", "white", 1, 1, False)
    lbl(' DOWN: "S" |  DOWN: "↓"', 6, 1, info, "black", "white", 1, 1, False)
    info.mainloop()


def turtle_race_info():
    # Skapar fönstret för turtle race info sidan
    info = Tk()
    info.iconbitmap(icon_img)
    info.title("Turtle Race")
    info.geometry("526x480")
    info.config(bg="black")

    # Bilden som visar hur spelet ser ut
    photo = PhotoImage(file=turtle_race_img).zoom(2).subsample(3)
    turtle_photo = Label(info, image=photo)
    turtle_photo.grid(row=1, column=1, columnspan=1)

    # Texten som visas högst upp
    lbl("Turtle Race", 0, 1, info, "black", "white")

    # Knappar för Back och Play:
    btn("Back", 0, 0, 20, 10, info, lambda:open_win(start_menu, info))
    btn("Play", 0, 3, 23, 10, info, lambda:open_win(turtle_race, info))

    # Texten som beskriver hur man spelar
    lbl("To play you need to enter how many racer you want to race (2-10)", 2, 1, info, "black", "white", 1, 1, False)
    info.mainloop()


def turtle_race():
    # Fönstret för att skriva in hur många spelar man vill tävla
    global e, text

    # Skapar fönstert för menyn
    t_race = Tk()
    t_race.iconbitmap(icon_img)
    t_race.title("Turtle Race")
    t_race.geometry("260x200")
    t_race.config(bg="black")

    # Texten som visas högst up
    text = Label(t_race, text="Plese enter the amount of racers (2-10)", bg="black", fg="white")
    text.grid(row=1, column=0, columnspan=2)

    # Där man skriver antal tävlare
    e = Entry(t_race, width=35, borderwidth=5)
    e.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Text och knappar
    lbl("Turle Race", 0, 1, t_race, "black", "white")
    btn("Back", 0, 0, 20, 10, t_race, lambda: open_win(start_menu, t_race))
    btn("play", 3, 0, 20, 5, t_race, lambda: check_players(e.get()), 3)
    t_race.mainloop()


def game_of_40_info():
    # Skapar fönstret för game of 40 info sidan
    info = Tk()
    info.iconbitmap(icon_img)
    info.title("Game of 40")
    info.geometry("663x620")
    info.config(bg="black")

    # Knappar för Back och Play:
    btn("Back", 0, 0, 20, 10, info, lambda: open_win(start_menu, info))
    btn("play", 0, 2, 23, 10, info, start_game_of_40)

    # Bilden som visar hur spelet ser ut
    photo = PhotoImage(file=game_of_40_img).zoom(2).subsample(3)
    game_of_40_photo = Label(info, image=photo)
    game_of_40_photo.grid(row=1, column=1, columnspan=1)

    # Texten som beskriver hur man spelar
    lbl("Game of 40", 0, 1, info, "black", "white", 1, 1)
    lbl("##################################", 2, 1, info, "black", "white", 1, 1, False)
    lbl("#  Welcome to the dice game: Game of 40  #", 3, 1, info, "black", "white", 1, 1, False)
    lbl("##################################", 4, 1, info, "black", "white", 1, 1, False)
    lbl("Game of 40 is a dice game where you first have to reach at least 40 points.", 5, 1, info, "black", "white", 1, 1, False)
    lbl("If you hit a six, you lose the points you did not save and the turn goes over to the opponent.", 6, 1, info, "black", "white", 1, 1, False)
    lbl("You can save your points at any time and let the luck go over to the opponent.", 7, 1, info, "black", "white", 1, 1, False)
    lbl("The player who starts the game is: Player 1", 8, 1, info, "black", "white", 1, 1, False)
    lbl("Press Play to start the game.", 9, 1, info, "black", "white", 1, 1, False)
    info.mainloop()


def space_invader_info():
    # Skapar fönstret för Space invader info sidan
    info = Tk()
    info.iconbitmap(icon_img)
    info.title("Space Invader Info")
    info.geometry("604x666")
    info.config(bg="black")

    # Bilden som visar hur spelet ser ut
    photo = PhotoImage(file=space_invader_img).zoom(1).subsample(2)
    space_invader_photo = Label(info, image=photo)
    space_invader_photo.grid(row=2, column=1, columnspan=1)

    # Texten som visas högst upp
    lbl("Space Invader", 0, 1, info, "black", "white")

    # Knappar för Back och Play:
    btn("Back", 0, 0, 20, 10, info, lambda:open_win(start_menu, info))
    btn("Play", 0, 3, 23, 10, info, space_invader_game)

    # Texten som beskriver hur man spelar
    lbl(f"Current High Score: {get_high_scores()}", 1, 1, info, "black", "white")
    lbl("The goal is to gain as many points as possible by killing the invaders.", 3, 1, info, "black", "white", big_text=False)
    lbl("Every 5th round you meet a boss and every 100 points you will get an extra bullet", 4, 1, info, "black", "white", big_text=False)
    lbl("C͟o͟n͟t͟r͟o͟l͟s͟", 5, 1, info, "black", "white", 1, 1, False)
    lbl("Left: ←", 6, 1, info, "black", "white", 1, 1, False)
    lbl("Right: →", 7, 1, info, "black", "white", 1, 1, False)
    lbl("Shoot: Space", 8, 1, info, "black", "white", 1, 1, False)
    lbl("Pause: P", 9, 1, info, "black", "white", 1, 1, False)
    info.mainloop()


start_menu()