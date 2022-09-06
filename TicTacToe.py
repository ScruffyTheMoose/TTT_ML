class Board:
    def __init__(self) -> None:
        self.board = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
        ]

    def move(self, row: int, column: int, player: str) -> bool:
        """Places a new piece on the board

        Args:
            row (int): row index
            column (int): column index
            player (str): 'X' or 'O'
        """

        # checking which player is making the move to determine value to place on board
        if player.upper() == "X":
            p = 1
        else:
            p = 0

        if self.board[row][column] == -1:
            self.board[row][column] = p
            return True

        return False

    def avail_moves(self) -> list(tuple()):
        """Returns a list of ordered pairs references available spaces on the board

        Args:
            self (_type_): class method

        Returns:
            matrix: 2D list
        """

        result = list()

        # iterate through rows
        for i, row in enumerate(self.board):
            # iterate through elements in row
            for j, element in enumerate(row):

                # if the space is open, add the coordinate to results
                if element == -1:
                    ord_pair = (i, j)
                    result.append(ord_pair)

        return result

    def board_status(self) -> tuple:
        """Checks the board for 4 conditions:
        - Game ongoing
        - Game draw
        - Player 'X' wins
        - Player 'O' wins

        Returns:
            tuple: (<status>, <winner>)
        """

        # running the three checks and storing outputs to variables
        r = self._check_rows()
        c = self._check_columns()
        d = self._check_diag()

        # checking the outputs for a winning case
        for t in [r, c, d]:
            if True in t:
                return t

        return self._check_draw()

    def _check_rows(self) -> tuple:
        """Checks the rows of the game board for a winning position

        Returns:
            tuple: (<status>, <winner>)
        """

        for row in self.board:
            # checking for False values in row to bypass summation
            if -1 in row:
                continue

            # checking the row for status
            check = self._check_triple(row)

            if check[0]:
                return check

        # if no winning rows found, return False
        return (False, None)

    def _check_columns(self) -> tuple:
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
            check = self._check_triple(col)

            if check[0]:
                return check

        # if no winning columns found, return False
        return (False, None)

    def _check_diag(self) -> tuple:
        """Checks the diagonals of the game board for a winning position

        Returns:
            tuple: (<status>, <winner>)
        """

        # generating diagonals of game board into two lists
        diag_left = [self.board[i][i] for i in range(3)]
        diag_right = [self.board[-i][i - 1] for i in range(1, 4)]

        # checking left status
        stat = self._check_triple(diag_left)
        if stat[0]:
            return stat

        # checking right status
        stat = self._check_triple(diag_right)
        if stat[0]:
            return stat

        return (False, None)

    def _check_triple(self, triple: list) -> tuple:
        """Checks a list of 3 elements for a winning position

        Args:
            triple (list): list of 3 adjacent elements from the game board

        Returns:
            tuple: (<status>, <winner>)
        """

        # if there is an open space in the given list, then there is no winner
        if -1 in triple:
            return (False, None)

        # the sum of the elements in the row will indicate status
        ct = sum(triple)
        if ct == 0:
            return (True, "O")
        elif ct == 3:
            return (True, "X")
        else:
            return (False, None)

    def _check_draw(self) -> tuple:
        """Checks the game board for a draw

        Returns:
            tuple: (<status>, <winner>)
        """

        for row in self.board:
            if -1 in row:
                return (False, None)

        return (True, None)

    def get_board(self) -> list(list()):
        """Getter for the game board object

        Args:
            self (_type_): class method

        Returns:
            matrix: 2D list
        """

        return self.board

    def string_board(self) -> str:
        """Generates a string version of the game board for printing to console

        Returns:
            str: a multi-line string representation of the game board
        """

        # initial string
        board = ""

        # iterating through the rows
        for i, row in enumerate(self.board):
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
