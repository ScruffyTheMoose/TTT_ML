import random


class Board:
    def __init__(self) -> None:
        self.board = [[0, 0, 0] for _ in range(3)]
        self.vector = [0 for x in range(9)]
        self.move_num = 0

    def get_board(self) -> list:
        """Getter for the game board object

        Args:
            self (_type_): class method

        Returns:
            matrix: TTT game board
        """

        return self.board

    def move(self, row: int, column: int, player: int) -> bool:
        """Places a new piece on the board

        Args:
            row (int): row index
            column (int): column index
            player (int): 1 or -1
        """

        if self.board[row][column] == 0:
            self.board[row][column] = player

            vec_idx = (3 * row) + column
            self.vector[vec_idx] = player

            self.move_num += 1

            return True

        return False

    def status(self) -> tuple:
        """Checks the board for 4 conditions:
        - Game ongoing
        - Game draw
        - Player 'X' wins
        - Player 'O' wins

        Returns:
            tuple: (<status>, <winner>)
        """

        def check_rows() -> tuple:
            """Checks the rows of the game board for a winning position

            Returns:
                tuple: (<status>, <winner>)
            """

            for row in self.board:
                # checking for False values in row to bypass summation
                if 0 in row:
                    continue

                # checking the row for status
                check = check_triple(row)

                if check[0]:
                    return check

            # if no winning rows found, return False
            return (False, 0)

        def check_columns() -> tuple:
            """Checks the columns of the game board for a winning position

            Returns:
                tuple: (<status>, <winner>)
            """

            for column in range(3):
                # building column into list
                col = [x[column] for x in self.board]

                # checking for False values in column to bypass summation
                if 0 in col:
                    continue

                # checking column for status
                check = check_triple(col)

                if check[0]:
                    return check

            # if no winning columns found, return False
            return (False, 0)

        def check_diag() -> tuple:
            """Checks the diagonals of the game board for a winning position

            Returns:
                tuple: (<status>, <winner>)
            """

            # generating diagonals of game board into two lists
            diag_left = [self.board[i][i] for i in range(3)]
            diag_right = [self.board[-i][i - 1] for i in range(1, 4)]

            # checking left status
            stat = check_triple(diag_left)
            if stat[0]:
                return stat

            # checking right status
            stat = check_triple(diag_right)
            if stat[0]:
                return stat

            return (False, 0)

        def check_triple(triple: list) -> tuple:
            """Checks a list of 3 elements for a winning position

            Args:
                triple (list): list of 3 adjacent elements from the game board

            Returns:
                tuple: (<status>, <winner>)
            """

            # if there is an open space in the given list, then there is no winner
            if 0 in triple:
                return (False, 0)

            # the sum of the elements in the row will indicate status
            ct = sum(triple)
            if ct == -3:
                return (True, -1)
            elif ct == 3:
                return (True, 1)
            else:
                return (False, 0)

        # this logic could be improved
        def check_draw() -> tuple:
            """Checks the game board for a draw

            Returns:
                tuple: (<status>, <winner>)
            """

            for row in self.board:
                if 0 in row:
                    return (False, 0)

            return (True, 0)

        # running the three checks and storing outputs to variables
        r = check_rows()
        c = check_columns()
        d = check_diag()

        # checking the outputs for a winning case
        for t in [r, c, d]:
            if True in t:
                return t

        return check_draw()

    def print(self) -> str:
        """Generates a string version of the game board for printing to console

        Returns:
            str: a multi-line string representation of the game board
        """

        # initial string
        str_board = ""

        # iterating through the rows
        for i, row in enumerate(self.board):
            # iterating through the elements in each row
            for j, element in enumerate(row):

                # -1 is an open space
                if element == 0:
                    str_board += "   "
                # 0 is an O
                elif element == -1:
                    str_board += " O "
                # if not O or empty, then X
                else:
                    str_board += " X "

                if j != 2:
                    str_board += "|"

            if i != 2:
                str_board += "\n-----------\n"

        return str_board


# a separate class to hold static methods strictly for making observations about any game board
# probably not necessary, but nice for organization at the moment
class GameTools:
    @staticmethod
    def avail_moves(board: list) -> list:
        """Returns a list of ordered pairs references available spaces on the board

        Args:
            self (_type_): class method

        Returns:
            matrix: list(tuple())
        """

        result = list()

        # iterate through rows
        for i, row in enumerate(board):
            # iterate through elements in row
            for j, element in enumerate(row):

                # if the space is open, add the coordinate to results
                if element == 0:
                    ord_pair = (i, j)
                    result.append(ord_pair)

        return result

    @staticmethod
    def string_board(matrix) -> str:
        """Generates a string version of the game board for printing to console

        Returns:
            str: a multi-line string representation of the game board
        """

        # initial string
        board = ""

        # iterating through the rows
        for i, row in enumerate(matrix):
            # iterating through the elements in each row
            for j, element in enumerate(row):

                # -1 is an open space
                if element == 0:
                    board += "   "
                # 0 is an O
                elif element == -1:
                    board += " O "
                # if not O or empty, then X
                else:
                    board += " X "

                if j != 2:
                    board += "|"

            if i != 2:
                board += "\n-----------\n"

        return board

    @staticmethod
    def randomized_match(first_player: int, open_pos: int) -> dict:
        """Generates random TTT game

        Args:
            first_player (int): player making first move; 'X' = 1, 'O' = 0
            open_spaces (int): number of open positions to leave on the board

        Returns:
            dict: {
            "board": game board matrix,
            "winner": winner of match,
            }
        """

        game = Board()

        # generating list of all positions on the board to randomly choose from
        # this is better than the alternative of randomly generating numbers
        coords = []
        for r in range(3):
            for c in range(3):
                coords.append((r, c))

        # placing moves on the board until desired number of positions filled
        pos = 9

        while pos >= open_pos:

            # choosing a random position to take
            move = random.choice(coords)
            coords.remove(move)

            if pos % 2 != 0:
                game.move(row=move[0], column=move[1], player=first_player)
            else:
                game.move(row=move[0], column=move[1], player=(-1 * first_player))

            pos -= 1

            # checking game status after new move made - if game over, break loop and return
            status = game.status()
            if status[0]:
                break

        # dict to return containing all relevant information from the randomized match
        results = {
            "board": game.board,
            "winner": status[1],  # 0, -1, or 1
            "first_move": first_player,
        }

        for idx, elem in enumerate(game.vector):
            results[idx + 1] = elem

        return results

    @staticmethod
    def randomized_reinforcement_match(first_player: int, class_type: str) -> list:
        """Generates random TTT game board

        Args:
            first_player (int): player making first move; 'X' = 1, 'O' = -1
            open_spaces (int): number of open positions to leave on the board
            class_type (str): 'XOD' or 'position'

        Returns:
            list: dictionaries of game states, outcomes, and labels
        """

        # nested function to for tracking game states
        def track():

            # dictionary and pre-move board state stored here
            s = dict()
            v = game.vector

            # for X/O/Draw classification, we assign the board state to a label of '0' to be changed later
            if class_type == "XOD":
                for idx, elem in enumerate(v):
                    s[idx + 1] = elem
                s["label"] = 0

            # for positional classification, we assign the board state to a label of the position just taken
            else:
                for idx, elem in enumerate(v):
                    s[idx + 1] = elem
                s["label"] = (move[0] * 3) + move[1] + 1

            # add data to the tracked game states
            states.append(s)

        # tic tac toe instance
        game = Board()

        # tracking all board states prior to making a move
        states = list()

        # generating list of all positions on the board to randomly choose from
        # this is better than the alternative of randomly generating numbers
        coords = []
        for r in range(3):
            for c in range(3):
                coords.append((r, c))

        # placing moves on the board until desired number of positions filled
        pos = 9

        while pos >= 0:

            # choosing a random position to take
            move = random.choice(coords)
            coords.remove(move)

            if pos % 2 != 0:
                # tracking state
                track()

                # making move
                game.move(row=move[0], column=move[1], player=first_player)
            else:
                # tracking state
                track()

                # making move
                game.move(row=move[0], column=move[1], player=(-1 * first_player))

            pos -= 1

            # checking game status after new move made - if game over, break loop and return
            status = game.status()
            if status[0]:
                break

        # for X/O/Draw, we use the final game outcome to label all the states
        if class_type == "XOD":
            for s in states:
                s["label"] = status[1]

        if class_type == "positional":
            for s in states:
                s["outcome"] = status[1]

        return states
