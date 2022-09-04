from TicTacToe import Board

# initializing the game and setting status
game = Board()
game_status = (False, None)

# for assigning first and second move
p1 = None
p2 = None

# tracks number of moves made to ensure plays are made in order
p1_ct = 0
p2_ct = 0

# setup loop
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

# play loop
while not game_status[0]:
    if p1_ct <= p2_ct:
        player = p1
        p1_ct += 1
        print(f"'{p1}' - please select your next move!", "\n")
    else:
        player = p2
        p2_ct += 1
        print(f"'{p2}' - please select your next move!", "\n")

    print(game.string_board(), "\n")

    row, column = None, None

    while row is None or column is None:
        row = int(input("Enter row index: "))
        column = int(input("Enter column index: "))

        if game.board[row][column] == -1:
            game.move(row, column, player)
        else:
            row, column = None, None
            print("That space is taken, please select another! \n")

    game_status = game.board_status()

# completion and results
if game_status[1] != None:
    print(
        "\n"
        + game.string_board()
        + "\n\n"
        + f"Congratulation '{game_status[1]}', you won!"
    )
else:
    print("\n" + game.string_board() + "\n\n" + "Draw!")
