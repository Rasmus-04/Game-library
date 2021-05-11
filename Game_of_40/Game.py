from tkinter import *
from Slutprojekt.Game_of_40.config import *
import random
import time


def start_game_of_40():
    # Slår tärningen
    def roll():
        nummber = random.randint(1, 6)
        active_dice.append(nummber)
        update_screen()
        
        # Om tärnningen bliv 6 så byt aktiv spelare
        if nummber == 6:
            switch_players()


    # Byter spelare
    def switch_players():
        global active_player
        
        if active_player == "P1":
            active_player = "P2"
        else:
            active_player = "P1"
            
        # Tömmer aktiva törnings listan
        active_dice.clear()


    def late_dice():
        # Kollar den senaste tärnig slaget
        try:
            return active_dice[-1]
        except:
            return ""


    # skapar en text
    def lbl(txt, r, c, win, big_txt=True, size=20, c_span=1):
        """
        :param txt: Texten som ska visas
        :param r: Vilken row texten ska vara
        :param c: Vilken kolumn den ska vara 
        :param win: vilket fönster texten ska vara i
        :param big_txt: Om texten ska vara stor
        :param size: Vilken storlek den ska vara
        :param c_span: Hur många kolumner texten ska ta up
        :return: 
        """
        lbl = Label(win, text=txt)
        if big_txt:
            lbl.config(font=("Courier", size))
        lbl.grid(row=r, column=c, columnspan=c_span)


    # Skapar Knappar
    def btn(txt, r, c, win, x=0, y=0, com=0):
        """
        :param txt: Vilken text som ska vara på knappen
        :param r: Vilken row som knappen ska vara
        :param c: Vilken kolumn som knappen ska vara
        :param win: vilket fönster texten ska vara i
        :param x: Hur bred knappen ska vara
        :param y: Hur hög knappen ska vara
        :param com: Vilken funktion som ska användas när knppen klickas på
        """
        btn = Button(win, text=txt, command=com)
        btn.grid(row=r, column=c, ipadx=x, ipady=y)


    # sparar sina poäng och byter ativ spelare
    def save():
        global active_dice, p1_score, p2_score
        if len(active_dice) != 0:
            if active_player == "P1":
                p1_score += sum(active_dice)

            else:
                p2_score += sum(active_dice)
            active_dice = []

            switch_players()

    # Byter bilden till den senaste tärngslags värde som du fick
    def change_img():
        photos.config(file=f"D:\Python\Slutprojekt\Game_of_40\Assets\Dice_{str(late_dice())}.png")

    # updaterar fönstret
    def update_screen():
        global img
        img = f"D:\Python\Slutprojekt\Game_of_40\Assets\Dice_{str(late_dice())}.png"
        photos.config(file=img)
        score_round.config(text=f"Score this round: {str(active_dice)[1:-1]}")
        total_round.config(text=f"Total score on this round: {sum(active_dice):02d}")
        p1_text.config(text=f"{p1_score:02d}")
        total_for_player.config(text=f"Total for player 1: {p1_score:02d}")
        player_turn.config(text=f"player {active_player}s turn!")
        p2_text.config(text=f"{p2_score:02d}")


        # Om någon spelare har över 40 poäng sä visas winnar skärmen
        if int(p2_score) >= 40 or int(p1_score) >= 40:
            winning_screen()


    # Gör funtionen och sedan updaterar fönstret
    def function(funk):
        funk()
        update_screen()


    # Startar om spelet
    def re_open():
        global p1_score, p2_score, active_dice, active_player
        screen.destroy()
        p1_score = 0
        p2_score = 0
        active_dice = []
        active_player = "P1"
        game_of_40()


    # Stänger av spelet
    def close_game():
        screen.destroy()


    # Winnar fönstert
    def winning_screen():
        global screen
        game.destroy()

        # Skapar fönstet
        screen = Tk()
        screen.title("Game of 40")
        screen.geometry("440x100")
        screen.iconbitmap("D:\Python\Slutprojekt\Game_of_40\Assets\Game_of_40.ico")

        # Skriver text
        if int(p1_score) >= 40:
            lbl(f"Player 1 Won with {p1_score} points", 0, 0, screen, True, 20, 2)
        else:
            lbl(f"Player 2 won with {p2_score} points", 0, 0, screen, True, 20, 2)

        # Knappar
        btn("Exit", 1, 0, screen, 20, 10, close_game)
        btn("Play Again", 1, 1, screen, 20, 10, re_open)

        screen.mainloop()


    def game_of_40():
        global score_round, total_round, photos, p1_text, total_for_player, player_turn, p2_text, game
        # Skapar fönster
        game = Tk()
        game.title("Game of 40")
        game.geometry("580x550")
        game.iconbitmap("D:\Python\Slutprojekt\Game_of_40\Assets\Game_of_40.ico")

        # Text
        lbl("Game of 40", 0, 1, game)
        lbl("P1 Score:", 0, 0, game)
        lbl("P2 Score:", 0, 2, game)

        # Tärnings bilden
        img = f"D:\Python\Slutprojekt\Game_of_40\Assets\Dice_{str(late_dice())}.png"
        photos = PhotoImage(master=game, file=f"D:\Python\Slutprojekt\Game_of_40\Assets\Dice_{str(late_dice())}.png")
        dice_photos = Label(game, image=photos)
        dice_photos.grid(row=1, column=1)


        # Text
        player_turn = Label(game, text=f"player {active_player}s turn!")
        player_turn.config(font=("Courier", 15))
        player_turn.grid(row=2, column=0, columnspan=3)


        # slå tärning knapp
        btn("Roll", 3, 1, game, 30, 5, lambda: function(roll))

        # Poäng text
        score_round = Label(game, text="Score this round:")
        score_round.config(font=("Courier", 15))
        score_round.grid(row=4, column=0, columnspan=3)

        # Totala poäng text
        total_round = Label(game, text="Total score on this round: 00")
        total_round.config(font=("Courier", 15))
        total_round.grid(row=5, column=0, columnspan=3)


        # Text
        total_for_player = Label(game, text=f"Total for player 1: {p1_score:02d}")
        total_for_player.config(font=("Courier", 15))
        total_for_player.grid(row=6, column=0, columnspan=3)


        # Spara knapp
        btn("Save", 7, 1, game, 30, 5, lambda: function(save))

        # Spelar 1 poäng text
        p1_text = Label(game, text="00")
        p1_text.config(font=("Courier", 40))
        p1_text.grid(row=1, column=0)

        # Spelar 2 poäng text
        p2_text = Label(game, text="00")
        p2_text.config(font=("Courier", 40))
        p2_text.grid(row=1, column=2)


        game.mainloop()


    game_of_40()


if __name__ == "__main__":
    start_game_of_40()
