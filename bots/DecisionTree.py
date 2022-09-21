from TicTacToe import Board, GameTools as gt

import pandas as pd
import numpy as np


class Bot:
    def __init__(self, model, game: Board, player: int) -> None:
        self.game = game
        self.player = player
        self.model = model
