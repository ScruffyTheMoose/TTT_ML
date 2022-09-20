import random


class Board:
    def __init__(self) -> None:
        self.board = [[-1, -1, -1] for _ in range(3)]

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
            player (str): 'X' or 'O'
        """

        if self.board[row][column] == -1:
            self.board[row][column] = player
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
                if -1 in row:
                    continue

                # checking the row for status
                check = check_triple(row)

                if check[0]:
                    return check

            # if no winning rows found, return False
            return (False, -1)

        def check_columns() -> tuple:
            """Checks the columns of the game board for a winning position

            Returns:
                tuple: (<status>, <winner>)
            """

            for column in range(3):
                # building column into list
                col = [x[column] for x in self.board]

                # checking for False values in column to bypass summation
                if -1 in col:
                    continue

                # checking column for status
                check = check_triple(col)

                if check[0]:
                    return check

            # if no winning columns found, return False
            return (False, -1)

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

            return (False, -1)

        def check_triple(triple: list) -> tuple:
            """Checks a list of 3 elements for a winning position

            Args:
                triple (list): list of 3 adjacent elements from the game board

            Returns:
                tuple: (<status>, <winner>)
            """

            # if there is an open space in the given list, then there is no winner
            if -1 in triple:
                return (False, -1)

            # the sum of the elements in the row will indicate status
            ct = sum(triple)
            if ct == 0:
                return (True, 0)
            elif ct == 3:
                return (True, 1)
            else:
                return (False, -1)

        def check_draw() -> tuple:
            """Checks the game board for a draw

            Returns:
                tuple: (<status>, <winner>)
            """

            for row in self.board:
                if -1 in row:
                    return (False, -1)

            return (True, -1)

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
                if element == -1:
                    str_board += "   "
                # 0 is an O
                elif element == 0:
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
                if element == -1:
                    ord_pair = (i, j)
                    result.append(ord_pair)

        return result

    @staticmethod
    def string_board() -> str:
        """Generates a string version of the game board for printing to console

        Returns:
            str: a multi-line string representation of the game board
        """

        # initial string
        board = ""

        # iterating through the rows
        for i, row in enumerate(board):
            # iterating through the elements in each row
            for j, element in enumerate(row):

                # -1 is an open space
                if element == -1:
                    board += "   "
                # 0 is an O
                elif element == 0:
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
        """Generates random TTT game board

        Args:
            first_player (int): player making first move; 'X' = 1, 'O' = 0
            open_spaces (int): number of open positions to leave on the board

        Returns:
            dict: {
            "board": game board matrix,
            "winner": winner of match,
            }
        """

        if first_player == 1:
            n = 1
        else:
            n = -1

        game = Board()

        # generating list of all positions on the board to randomly choose from
        # this is better than the alternative of randomly generating numbers
        coords = []
        for r in range(3):
            for c in range(3):
                coords.append((r, c))

        # for tracking moves made during match
        hist = [0 for _ in range(9)]

        # placing moves on the board until desired number of positions filled
        pos = 9

        while pos > open_pos:

            # choosing a random position to take
            move = random.choice(coords)
            coords.remove(move)

            if pos % 2 != 0:
                game.move(row=move[0], column=move[1], player=first_player)
            else:
                game.move(row=move[0], column=move[1], player=(1 - first_player))

            # decrementing positions open
            idx = 9 - pos

            int_pos = ((move[0] + 1) * 2) + move[1] + 1

            # recording move
            if pos % 2 != 0:
                hist[idx] = n * int_pos
            else:
                hist[idx] = n * -int_pos

            pos -= 1

            # checking game status after new move made - if game over, break loop and return
            status = game.status()
            if status[0]:
                break

        # dict to return containing all relevant information from the randomized match
        results = {
            "board": game.board,
            "winner": status[1],  # None, X, or O
        }

        for i in range(9):
            results[i + 1] = hist[i]

        return results
