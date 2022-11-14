from TicTacToe import Board, GameTools as gt

from sklearn.neural_network import MLPClassifier

import random
import pickle
import hashlib
import numpy as np
from copy import deepcopy


class RandomEnvironment:
    def __init__(self, agent: MLPClassifier, binary_encode_data: bool = False) -> None:
        self.agent = agent
        self.binary_encode_data = binary_encode_data

        self.states_data = dict()
        self.states_seen = set()

        self.training_iters = 0
        self.score_iters = 0

    def play(
        self,
        model_plays_first: bool,
        update_scores: bool = False,
        train_model: bool = False,
        rand_move_proba: float = 0.0,
        print_board: bool = False,
    ) -> None:
        game = Board()

        match_states = list()
        match_labels = list()

        status = game.status()

        ### begin while loop ###

        rem_moves = 9

        while rem_moves > 0 and not status[0]:

            state = deepcopy(game.vector)

            if self.binary_encode_data:
                state_matrix = np.array([self.binary_encode(state)])
            else:
                state_matrix = np.array([state])

            label = None

            coords = gt.avail_moves(game.board)

            if (model_plays_first and rem_moves % 2 != 0) or (
                not model_plays_first and rem_moves % 2 == 0
            ):

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

            else:
                move = random.choice(coords)
                game.move(row=move[0], column=move[1], player=-1)

            rem_moves -= 1
            status = game.status()

        ### end while loop ###

        if update_scores:
            self.states_seen = self.states_seen.union(
                [tuple(state) for state in match_states]
            )

            classes = [x for x in range(1, 10)]

            # updating our environments saved states and quality values based on the outcome of this match
            # has significant impact on how model performs when playing second for some reason...
            if status[1] == 1:
                w = 1  # winner acts as multiplier for quality points
            elif status[1] == -1:
                w = -1  # loss and draw result in neg points
            else:
                w = -1

            for idx, state in enumerate(match_states):
                enc = pickle.dumps(state, -1)
                h = hashlib.sha256(enc).hexdigest()  # getting state hash
                l = match_labels[idx]  # getting label for this match based on move made

                if h in self.states_data:
                    self.states_data[h][l - 1] += w

                else:
                    self.states_data[h] = [0 for _ in range(9)]
                    self.states_data[h][l - 1] += w

        if train_model and not self.binary_encode_data:
            self.training_iters += 1

            features = np.array(match_states)
            labels = np.array(self._states_matrix_lookup(match_states))

            self.agent.partial_fit(features, labels, classes)
        elif train_model and self.binary_encode_data:
            self.training_iters += 1

            features = [
                self.binary_encode(m) for m in match_states
            ]  # binary encoding the board
            features = np.array(features)
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
    def binary_encode(vec: list) -> list:
        x_pos = [0 for _ in range(9)]
        o_pos = [0 for _ in range(9)]

        for idx, val in enumerate(vec):
            if val == 1:
                x_pos[idx] = 1
            elif val == -1:
                o_pos[idx] = 1

        return x_pos + o_pos
