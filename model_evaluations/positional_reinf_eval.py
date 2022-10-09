from TicTacToe import Board, GameTools as gt
from sklearn.neural_network import MLPClassifier
import random
import numpy as np


def bot_vs_random(
    model: MLPClassifier, bot_plays_first: bool = True, print_board: bool = False
):

    if bot_plays_first:
        bot_first = 1
    else:
        bot_first = 0
    game = Board()
    pos = 9

    classes = model.classes_

    def ordered_options(vector):
        # geting output values for each class
        probs = model.predict_proba(vector)
        # constructing dictionary of classes and probabilities
        d = {classes[i]: probs[0][i] for i in range(len(classes))}
        # returning a list classes in order of most likely to least likely
        return sorted(d, key=d.get, reverse=True)

    while pos > 0 and not game.status()[0]:

        coords = gt.avail_moves(game.board)
        mod_board = np.array([game.vector])

        if bot_first and pos % 2 != 0:
            choices = ordered_options(mod_board)

            for c in choices:
                move = ((c - 1) // 3, (c - 1) % 3)
                b = game.move(row=move[0], column=move[1], player=1)

                if b:
                    break

        elif not bot_first and pos % 2 != 0:
            move = random.choice(coords)

            game.move(row=move[0], column=move[1], player=-1)

        elif bot_first and pos % 2 == 0:
            move = random.choice(coords)

            game.move(row=move[0], column=move[1], player=-1)

        elif not bot_first and pos % 2 == 0:
            choices = ordered_options(mod_board)

            for c in choices:
                move = ((c - 1) // 3, (c - 1) % 3)
                b = game.move(row=move[0], column=move[1], player=1)

                if b:
                    break

        pos -= 1

    if print_board:
        print(game.print())

    return game.status()[1]
