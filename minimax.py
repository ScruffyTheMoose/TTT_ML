from TicTacToe import GameTools as gt
import copy

######## THIS IS A SCRAP FILE - NOTHING HERE IS COMPLETE OR USEFUL ########

# I was attempting to find a different way to build and evaluate a tree of different gameplay outcomes by changing up the minimax algorithm a bit.

# the best move from the initial position should be the move which results in the most winning opportuntities
# this can most easily be determined by summing the total number of children with winning status for the maximizing player
# ex: if maximizing player takes position [0][0] and this results in 20 different winning children vs moving to [0][1] and this results in 7 winning children, we will take position [0][0]

# count the number of triples that don't have any opponent pieces in them - this would indicate that you *can* still win using that triple

# need to define 'position' - right now we are using this as equivalent to 'board' but that doesn't work
# 'position' needs to be a quantifier for the status of the board to indicate how good or bad the setup is


def best_move(board):
    choices = generate_children(board=board, player=1)
    results = list()

    for choice in choices:
        results.append(minimax(board=choice, depth=100, maximizing_player=False))

    print(results)


def minimax(board: list[list], depth: int, maximizing_player: bool):

    board_stat = gt.board_status(board)
    if depth == 0 or board_stat[0]:
        if board_stat[1] == "X":
            return 1
        elif board_stat[1] == "O":
            return -1
        else:
            return 0

    if maximizing_player:
        max_eval = -1000
        children = generate_children(
            board, 1
        )  # assumes maximizing player is always 'X'

        eval = 0
        for child in children:
            eval += minimax(child, depth - 1, False)

        # print(eval)
        max_eval = max(max_eval, eval)

        return max_eval

    else:
        min_eval = 1000
        children = generate_children(
            board, 0
        )  # assumes minimizing player is always 'O'

        eval = 0
        for child in children:
            eval += minimax(child, depth - 1, True)

        # print(eval)
        min_eval = min(min_eval, eval)

        return min_eval


def generate_children(board: list[list], player: int) -> list:
    """Generates a list of matrices containing all possible permuations of the given game board

    Args:
        board (list[list]): game board matrix
        player (int): int value of player making move

    Returns:
        list: new game board matrix
    """

    moves = gt.avail_moves(board)
    children = list()

    for m in moves:
        r = m[0]
        c = m[1]
        child_board = copy.deepcopy(board)
        child_board[r][c] = player
        children.append(child_board)

    return children


fake_board = [
    [-1, -1, 0],
    [0, 1, -1],
    [1, -1, -1],
]

print(best_move(fake_board))
