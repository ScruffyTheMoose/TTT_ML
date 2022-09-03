class TicTacToe:
    def __init__(self) -> None:
        self.board = [
            [False, False, False],
            [False, False, False],
            [False, False, False],
        ]

    def move(self, row: int, column: int, player: str) -> None:
        """Places a new piece on the board

        Args:
            row (int): row index
            column (int): column index
            player (str): 'X' or 'O'
        """

        self.board[row][column] = player.upper()

    def board_status(self) -> tuple:
        """Checks the board for 4 conditions:
        - Game ongoing
        - Game draw
        - Player 'X' wins
        - Player 'O' wins

        Returns:
            tuple: (<status>, <winner>)
        """

        r = self._check_rows()
        c = self._check_columns()
        d = self._check_diag()

        for t in [r, c, d]:
            if True in t:
                return t

    def _check_rows(self) -> tuple:
        """Checks the rows of the game board for a winning position

        Returns:
            tuple: (<status>, <winner>)
        """

        for row in self.board:
            # checking for False values in row to bypass summation
            if False in row:
                continue

            return self._check_triple(row)

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
            if False in col:
                continue

            return self._check_triple(col)

        # if no winning columns found, return False
        return (False, None)

    def _check_diag(self) -> tuple:
        """Checks the diagonals of the game board for a winning position

        Returns:
            tuple: (<status>, <winner>)
        """

        # generating diagonals of game board into two lists
        diag_left = [self.board[i][i] for i in range(3)]
        diag_right = [self.board[i][i] for i in range(-3)]

        stat = self._check_triple(diag_left)
        if stat[0]:
            return stat

        stat = self._check_triple(diag_right)
        if stat[0]:
            return stat

    def _check_triple(self, triple: list) -> tuple:
        """Checks a list of 3 elements for a winning position

        Args:
            triple (list): list of 3 adjacent elements from the game board

        Returns:
            tuple: (<status>, <winner>)
        """

        if False in triple:
            return (False, None)

        ct = sum(triple)
        if ct == 0:
            return (True, "O")
        elif ct == 3:
            return (True, "X")

    def get_board(self) -> list(list()):
        """Getter for the game board object

        Args:
            self (_type_): class method

        Returns:
            _type_: 2D list
        """

        return self.board

    def string_board(self) -> str:
        """Generates a string version of the game board for printing to console

        Returns:
            str: a multi-line string representation of the game board
        """

        board = ""

        for i, row in enumerate(self.board):

            for j, element in enumerate(row):

                if element is False:
                    board += "   "
                elif element == 0:
                    board += " O "
                else:
                    board += " X "

                if j != 2:
                    board += "|"

            if i != 2:
                board += "\n-----------\n"

        return board
