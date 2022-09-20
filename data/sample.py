from TicTacToe import GameTools as gt
import pandas as pd
import random


def random_samples(
    n_samples: int = 500,
    directory: str = "samples.csv",
    rand_first_player: bool = True,
    first_player: int = 1,
    fixed_open_spaces: bool = False,
    open_space_range: tuple = (1, 8),
    shuffled: bool = True,
) -> None:
    """Creates a set of random samples and saves them to the specified directory as a .csv file.

    Returns:
        File: a CSV file containing the sample data
    """

    osr = open_space_range

    samples = list()

    if rand_first_player and not fixed_open_spaces:

        for _ in range(n_samples):

            player = random.randint(0, 1)
            open_spaces = random.randint(1, 8)

            match = gt.randomized_match(first_player=player, open_pos=open_spaces)

            samples.append(match)

    elif rand_first_player and fixed_open_spaces:

        for _ in range(n_samples):

            player = random.randint(0, 1)
            open_spaces = random.randint(osr[0], osr[1])

            match = gt.randomized_match(first_player=player, open_pos=open_spaces)

            samples.append(match)

    elif not rand_first_player and not fixed_open_spaces:

        for _ in range(n_samples):

            player = first_player
            open_spaces = random.randint(1, 8)

            match = gt.randomized_match(first_player=player, open_pos=open_spaces)

            samples.append(match)

    else:

        for _ in range(n_samples):

            player = first_player
            open_spaces = random.randint(osr[0], osr[1])

            match = gt.randomized_match(first_player=player, open_pos=open_spaces)

            samples.append(match)

    if shuffled:
        samples = random.shuffle(samples)

    df = pd.DataFrame(samples)

    df.to_csv(path_or_buf=directory, index=False)
