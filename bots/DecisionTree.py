from TicTacToe import Board, GameTools as gt

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from copy import deepcopy


class Bot:
    def __init__(self, centroid: np.ndarray, player: int) -> None:
        # ensuring proper player value selected
        if player != 1 or player != 0:
            raise Exception("Player value must be a 0 or 1")

        self.player = player
        self.centroid = centroid

    def determine_move(self, game: Board) -> int:
        """Given a game, determines the optimal move based on a cluster centroid.

        Args:
            self: instance method
            centroid: the np array of coordinates for the target centroid
            player: 0 for 'O' or 1 for 'X'

        Returns:
            int: The recommended move based on the model
        """

        # first get the board
        board = game.get_vec_board()

        # determine index of move to be made in the vector
        idx = board.index(0)  # returns first occurrence of 0 in the list
        board = np.array(board)  # converting board to numpy array

        # generating list of potential move values based on player attribute
        pot_moves = (
            [x for x in range(1, 10)]
            if self.player == 1
            else [x for x in range(-1, -10, -1)]
        )

        # determine possible moves that can be made
        for m in board:
            val = abs(m)
            if val in pot_moves:
                pot_moves.remove(val)

        # calculate euclidian distance
        def distance(centroid: np.ndarray, point: np.ndarray) -> float:
            dist = np.subtract(centroid, point)
            dist = dist**2
            dist = np.sqrt(np.sum(dist))

            return dist

        # use distance formula to determine best move
        min_dist = None
        opt_move = None

        for value in pot_moves:
            board[idx] = value  # we can alter the value of the board
            dist = distance(self.centroid, board)

            if min_dist is None or dist < min_dist:
                min_dist = dist
                opt_move = value

        return opt_move
