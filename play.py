from TicTacToe import Board, GameTools as gt

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
    tmp = int(tmp)

    if tmp == 1:
        p1 = tmp
        p2 = 0
    elif tmp == 0:
        p1 = tmp
        p2 = 1
    else:
        print("\nEnter a valid symbol - 1 for 'X' or 0 for 'O'")

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

    print(game.print(), "\n")

    row, column = None, None

    while row is None or column is None:
        row = int(input("Enter row index: "))
        column = int(input("Enter column index: "))

        move = game.move(row, column, player)

        if not move:
            row, column = None, None
            print("That space is taken, please select another! \n")

    game_status = game.status()

# completion and results
if game_status[1] != None:
    print("\n" + game.print() + "\n\n" + f"Congratulation '{game_status[1]}', you won!")
else:
    print("\n" + game.print() + "\n\n" + "Draw!")
