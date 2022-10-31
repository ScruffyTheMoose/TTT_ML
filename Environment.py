from TicTacToe import Board, GameTools as gt

from sklearn.neural_network import MLPClassifier

import random
import pickle
import hashlib
import numpy as np
from copy import deepcopy


class RandomEnvironment:
    def __init__(self, agent: MLPClassifier) -> None:
        self.agent = agent
        self.states_data = dict()
        self.states_seen = set()
        self.training_iters = 0

    def play(
        self,
        model_plays_first: bool,
        train_model: bool = False,
        rand_move_proba: float = 0.0,
        print_board: bool = False,
    ) -> None:
        game = Board()

        iter_score = 1 + self.training_iters / 1000

        match_states = list()
        match_labels = list()

        status = game.status()

        ### begin while loop ###

        rem_moves = 9

        while rem_moves > 0 and not status[0]:
            state = deepcopy(game.vector)
            state_matrix = np.array([state])

            label = None

            coords = gt.avail_moves(game.board)

            if model_plays_first and rem_moves % 2 != 0:

                roll = random.random()

                if roll < rand_move_proba:
                    move = random.choice(coords)
                    coords.remove(move)

                    label = self.__coord_to_int(move)
                    game.move(row=move[0], column=move[1], player=1)

                else:
                    pred, move = self.agent_predict(state_matrix)

                    out = game.move(row=move[0], column=move[1], player=1)

                    if not out:
                        label = pred
                    else:
                        move = random.choice(coords)
                        coords.remove(move)

                        label = self.__coord_to_int(move)
                        game.move(row=move[0], column=move[1], player=1)

                match_states.append(state)
                match_labels.append(label)

            elif not model_plays_first and rem_moves % 2 != 0:
                move = random.choice(coords)
                game.move(row=move[0], column=move[1], player=-1)

            elif model_plays_first and rem_moves % 2 == 0:
                move = random.choice(coords)
                game.move(row=move[0], column=move[1], player=-1)

            else:
                roll = random.random()

                if roll < rand_move_proba:
                    move = random.choice(coords)
                    coords.remove(move)

                    label = self.__coord_to_int(move)
                    game.move(row=move[0], column=move[1], player=1)

                else:
                    pred, move = self.agent_predict(state_matrix)

                    out = game.move(row=move[0], column=move[1], player=1)

                    if out:
                        label = pred
                    else:
                        move = random.choice(coords)
                        coords.remove(move)

                        label = self.__coord_to_int(move)
                        game.move(row=move[0], column=move[1], player=1)

                match_states.append(state)
                match_labels.append(label)

            rem_moves -= 1
            status = game.status()

        ### end while loop ###

        if train_model:
            self.training_iters += 1
            self.states_seen = self.states_seen.union(
                [tuple(state) for state in match_states]
            )

            classes = [x for x in range(1, 10)]

            # updating our environments saved states and quality values based on the outcome of this match
            w = status[1]  # winner acts as multiplier for quality points
            for idx, state in enumerate(match_states):
                enc = pickle.dumps(state, -1)
                h = hashlib.sha256(enc).hexdigest()  # getting state hash
                l = match_labels[idx]  # getting label for this match based on move made

                if h in self.states_data:
                    self.states_data[h][l - 1] += iter_score * w

                else:
                    self.states_data[h] = [0 for _ in range(9)]
                    self.states_data[h][l - 1] += iter_score * w

            features = np.array(match_states)
            labels = np.array(self._states_matrix_lookup(match_states))

            self.agent.partial_fit(features, labels, classes)

        if print_board:
            print(game.print())

        return status[1]

    def agent_predict(self, matrix: np.ndarray) -> int:
        n = self.agent.predict(matrix)[0]
        coord = self.__int_to_coord(n)

        return n, coord

    def data_gen(self) -> tuple[np.ndarray, np.ndarray, list]:
        features = np.array(list(self.states_seen))
        labels = np.array(self._states_matrix_lookup(self.states_seen))
        classes = [x for x in range(1, 10)]

        return features, labels, classes

    def _states_matrix_lookup(self, states_matrix: list) -> list:
        result = list()  # list to return of highest rated labels for a matrix of states

        for state in states_matrix:
            enc = pickle.dumps(list(state), -1)  # encoding state
            h = hashlib.sha256(enc).hexdigest()  # getting state hash

            scores = self.states_data[h]  # getting list of scores
            m = max(scores)  # getting highest score in list
            choice = (
                scores.index(m) + 1
            )  # getting index of highest score + 1 which is the best rated move

            result.append(choice)  # adding best rated move to results

        return result

    @staticmethod
    def __coord_to_int(coord: tuple) -> int:
        return 3 * coord[0] + coord[1] + 1

    @staticmethod
    def __int_to_coord(n: int) -> tuple:
        return ((n - 1) // 3, (n - 1) % 3)

    @staticmethod
    def rand_play(
        model: MLPClassifier, model_plays_first: bool, print_board: bool = False
    ):
        game = Board()  # initializing a new game of TTT

        status = (
            game.status()
        )  # function specific to TTT. Will be used to check if the game has ended

        moves_remaining = 9

        # while loop which plays a game of TTT
        while moves_remaining > 0 and not status[0]:
            state = deepcopy(
                game.vector
            )  # getting copy of the board state in a vectorized format - Ex: [0, 0, 0, 0, 0, 0, 0, 0, 0]

            label = None

            coords = gt.avail_moves(
                game.board
            )  # using a tool specific to our TTT game to get the (row, column) coordinates for available positions on the board

            matrix_state = np.array(
                [state]
            )  # putting our state into a numpy matrix. we need to use a consistent data structure and format for training the model and numpy works well

            # if model is playing first and it is first player's turn
            # this is the model's move
            if model_plays_first and moves_remaining % 2 != 0:
                prediction = model.predict(matrix_state)[
                    0
                ]  # predicting the best move based on the current game board

                move = (
                    (prediction - 1) // 3,
                    (prediction - 1) % 3,
                )  # converting an integer into (row, column) coordinates. This is specific to our TTT

                # it is possible the model will try to make a move that isn't possible because the space is taken. We will validate that the move was made successfully here.
                out = game.move(
                    row=move[0], column=move[1], player=1
                )  # move() function returns True if move was successful, false otherwise

                if out:
                    label = prediction
                else:
                    move = random.choice(
                        coords
                    )  # choosing randomly from known available positions
                    coords.remove(
                        move
                    )  # dropping our selected move from the available positions on the board

                    label = (
                        (3 * move[0]) + move[1] + 1
                    )  # converting coordinates to integer value
                    game.move(
                        row=move[0], column=move[1], player=1
                    )  # placing random move on the board

            # if model is playing second and it is first player's turn
            # this is the random players move
            elif not model_plays_first and moves_remaining % 2 != 0:
                move = random.choice(coords)
                game.move(row=move[0], column=move[1], player=-1)

            # if model is playing first and it is the second player's turn
            # this is the random players move
            elif model_plays_first and moves_remaining % 2 == 0:
                move = random.choice(coords)
                game.move(row=move[0], column=move[1], player=-1)

            # if model is playing second and it is the second player's turn
            # this is the model's move
            else:
                prediction = model.predict(matrix_state)[
                    0
                ]  # predicting the best move based on the current game board

                move = (
                    (prediction - 1) // 3,
                    (prediction - 1) % 3,
                )  # converting an integer into (row, column) coordinates. This is specific to our TTT

                # it is possible the model will try to make a move that isn't possible because the space is taken. We will validate that the move was made successfully here.
                out = game.move(
                    row=move[0], column=move[1], player=1
                )  # move() function returns True if move was successful, false otherwise

                if out:
                    label = prediction
                else:
                    move = random.choice(
                        coords
                    )  # choosing randomly from known available positions
                    label = (
                        (3 * move[0]) + move[1] + 1
                    )  # converting coordinates to integer value
                    game.move(
                        row=move[0], column=move[1], player=1
                    )  # placing random move on the board

            moves_remaining -= 1
            status = game.status()
        # end of the while loop for playing a game of TTT

        # if print_board set to true, will print a nice string formatting version of the board
        if print_board:
            print(game.print())

        return status[1]
