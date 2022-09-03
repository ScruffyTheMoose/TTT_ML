from TicTacToe import TicTacToe

game = TicTacToe()
game_status = False

p1 = None
p2 = None

p1_ct = 0
p2_ct = 0

while p1 is None:
    tmp = input("\nPlease enter which player goes first: ")
    tmp = tmp.upper()

    if tmp == "X":
        p1 = tmp
        p2 = "O"
    elif tmp == "O":
        p1 = tmp
        p2 = "X"
    else:
        print("\nEnter a valid symbol - 'X' or 'O'")

    print("\n")

while not game_status:
    pass
