import sys

sys.path.append("..")

from TicTacToe import Board


def run():
    # must return (True, <winner>)
    test1 = test_1()
    test2 = test_2()
    test3 = test_3()
    test4 = test_4()

    # must return (False, None)
    test5 = test_5()

    # check and output results
    true_tests = [test1, test2, test3, test4]
    false_tests = [test5]

    for idx, t in enumerate(true_tests):
        if t[0]:
            print(f"Test {idx + 1} SUCCESS -> {t}")
        else:
            print(f"Test {idx + 1} FAILED -> {t}")

    for idx, t in enumerate(false_tests):
        if not t[0]:
            print(f"Test {idx + len(true_tests) + 1} SUCCESS -> {t}")
        else:
            print(f"Test {idx + 1} FAILED -> {t}")


# checks for row completion
def test_1():
    game = Board()

    moves = [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2)]

    # setting up board
    for idx, move in enumerate(moves):
        if idx % 2 == 0:
            game.move(move[0], move[1], 1)
        else:
            game.move(move[0], move[1], 0)

    return game.status()


# checks for column completion
def test_2():
    game = Board()

    moves = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 0)]

    # setting up board
    for idx, move in enumerate(moves):
        if idx % 2 == 0:
            game.move(move[0], move[1], 1)
        else:
            game.move(move[0], move[1], 0)

    return game.status()


# checks for diagonal completion
def test_3():
    game = Board()

    moves = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2)]

    # setting up board
    for idx, move in enumerate(moves):
        if idx % 2 == 0:
            game.move(move[0], move[1], 1)
        else:
            game.move(move[0], move[1], 0)

    return game.status()


# checks for draw game
def test_4():
    game = Board()

    moves = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (1, 1), (2, 2), (2, 1)]

    # setting up board
    for idx, move in enumerate(moves):
        if idx % 2 == 0:
            game.move(move[0], move[1], 1)
        else:
            game.move(move[0], move[1], 0)

    return game.status()


# checks for ongoing game
def test_5():
    game = Board()

    moves = [(0, 0), (0, 1)]

    # setting up board
    for idx, move in enumerate(moves):
        if idx % 2 == 0:
            game.move(move[0], move[1], 1)
        else:
            game.move(move[0], move[1], 0)

    return game.status()


if __name__ == "__main__":
    run()
