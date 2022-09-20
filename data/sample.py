from TicTacToe import GameTools as gt
import pandas as pd
import random


def random_samples(
    n_samples: int = 500,
    directory: str = "samples.csv",
    rand_first_player: bool = True,
    first_player: int = 1,
    open_space_range: tuple = (1, 8),
    shuffled: bool = True,
) -> pd.DataFrame:
    """Creates a set of random samples and saves them to the specified directory as a .csv file.

    n_samples: the number of samples to generate
    directory: the directory and filename
    rand_first_player: will randomly select first player for each sample
    first_player: if not rand_first_player, this will be the first player for each sample
    open_space_range: the lower and upper bound for randomly determining the number of open spaces to leave on the board
    shuffled: will shuffle the samples into a random order

    Returns:
        File: a CSV file containing the sample data
    """

    # shorter variable name to be called later
    osr = open_space_range

    # list to store the samples that we generate
    samples = list()

    # Condition 1
    if rand_first_player:
        # generate n samples
        for _ in range(n_samples):
            # determining player and open space count
            player = random.randint(0, 1)
            open_spaces = random.randint(osr[0], osr[1])
            # generating and storing the sample
            match = gt.randomized_match(first_player=player, open_pos=open_spaces)
            samples.append(match)

    # Condition 2
    else:
        # generating n samples
        for _ in range(n_samples):
            # setting player and determining open space count
            player = first_player
            open_spaces = random.randint(osr[0], osr[1])
            # generating and storing the sample
            match = gt.randomized_match(first_player=player, open_pos=open_spaces)
            samples.append(match)

    # will randomly order the samples before saving
    if shuffled:
        samples = random.shuffle(samples)

    # converting the list into a DataFrame and then a .csv file
    df = pd.DataFrame(samples)
    df.to_csv(path_or_buf=directory, index=False)

    # returning the DataFrame
    return df
