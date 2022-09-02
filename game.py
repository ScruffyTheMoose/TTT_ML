class TicTacToe:
    def __init__(self) -> None:
        self.board = [
            [False, False, False],
            [False, False, False],
            [False, False, False],
        ]

    def move(self, row: int, column: int, player: str) -> None:
        """
        Places a piece on the board for the requesting player
        """

        self.board[row][column] = player

    def board_status(self) -> tuple:
        """
        Checks the board for 4 conditions:
        - Game ongoing
        - Game draw
        - Player 'X' wins
        - Player 'O' wins
        """

        r = self.check_rows()
        c = self.check_columns()
        d = self.check_diag()

        for t in [r, c, d]:
            if True in t:
                return t

    def check_rows(self) -> tuple:
        """
        Checks the rows of the game board for a winning status
        """

        for row in self.board:
            # checking for False values in row to bypass summation
            if False in row:
                continue

            return self.check_triple(row)

        # if no winning rows found, return False
        return (False, None)

    def check_columns(self) -> tuple:
        """
        Checks the columns of the game board for a winning status
        """

        for column in range(3):
            # building column into list
            col = [x[column] for x in self.board]

            # checking for False values in column to bypass summation
            if False in col:
                continue

            return self.check_triple(col)

        # if no winning columns found, return False
        return (False, None)

    def check_diag(self) -> tuple:
        """
        Checks the diagonals of the game board for a winning status
        """

        # generating diagonals of game board into two lists
        diag_left = [self.board[i][i] for i in range(3)]
        diag_right = [self.board[i][i] for i in range(-3)]

        stat = self.check_triple(diag_left)
        if stat[0]:
            return stat

        stat = self.check_triple(diag_right)
        if stat[0]:
            return stat

    def check_triple(self, triple: list) -> tuple:
        """
        Checks a list of three elements for a winning status
        """

        if False in triple:
            return (False, None)

        ct = sum(triple)
        if ct == 0:
            return (True, "O")
        elif ct == 3:
            return (True, "X")
