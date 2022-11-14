from TicTacToe import Board, GameTools as gt
from sklearn.neural_network import MLPClassifier
import random
import pandas as pd
import numpy as np


def bot_vs_rand_environment(
    model: MLPClassifier,
    bot_first: bool = True,
    first_tracked: bool = True,
    train_model: bool = False,
    training_type: str = "dense",
    print_board: bool = False,
):
    # TTT instance
    game = Board()
    # track number of positions open on the board
    pos = 9

    # retrieving the available classes from the model for use
    classes = model.classes_

    # function that returns a list of all outputs from the model in order from most to least recommended
    # this allows us to take an alternate option if the space is unavailable
    def ordered_options(vector):
        # geting output values for each class

        probs = model.predict_proba(vector)
        # constructing dictionary of classes and probabilities

        d = {classes[i]: probs[0][i] for i in range(len(classes))}
        # returning a list classes in order of most likely to least likely

        result = sorted(d, key=d.get, reverse=True)
        return result

    # list to track all events in the match
    match_states = list()
    # initial game status for the loop
    game_stat = game.status()

    while pos > 0 and not game_stat[0]:

        # this iterations match state
        state = dict()
        # adding the vectorized game board to the state
        for idx, elem in enumerate(game.vector):
            state[idx + 1] = elem

        # getting all open spaces on the board
        coords = gt.avail_moves(game.board)

        # adding our additional feature
        # if our agent is aware of who plays first
        if first_tracked:
            v = game.vector + [bot_first]
        # if our agent is aware of the desired outcome (winning)
        else:
            v = game.vector

        # converting to 2D numpy array
        mod_board = np.array([v])

        # making different plays and tracking the decisions made
        if bot_first and pos % 2 != 0:
            # choices = ordered_options(mod_board)

            # for c in choices:
            #     move = ((c - 1) // 3, (c - 1) % 3)
            #     b = game.move(row=move[0], column=move[1], player=1)

            #     if b:
            #         state["label"] = c
            #         break

            pred = model.predict(mod_board)[0]
            move = ((pred - 1) // 3, (pred - 1) % 3)
            out = game.move(row=move[0], column=move[1], player=1)

            if out:
                state["label"] = pred
            else:
                move = random.choice(coords)
                state["label"] = (3 * move[0]) + move[1] + 1
                game.move(row=move[0], column=move[1], player=1)

            match_states.append(state)

        elif not bot_first and pos % 2 != 0:
            move = random.choice(coords)

            game.move(row=move[0], column=move[1], player=-1)

        elif bot_first and pos % 2 == 0:
            move = random.choice(coords)

            game.move(row=move[0], column=move[1], player=-1)

        elif not bot_first and pos % 2 == 0:
            # choices = ordered_options(mod_board)

            # for c in choices:
            #     move = ((c - 1) // 3, (c - 1) % 3)
            #     b = game.move(row=move[0], column=move[1], player=1)

            #     if b:
            #         state["label"] = c
            #         break

            pred = model.predict(mod_board)[0]
            move = ((pred - 1) // 3, (pred - 1) % 3)
            out = game.move(row=move[0], column=move[1], player=1)

            if out:
                state["label"] = pred
            else:
                move = random.choice(coords)
                state["label"] = (3 * move[0]) + move[1] + 1
                game.move(row=move[0], column=move[1], player=1)

            match_states.append(state)

        # end play making

        # updating game status variable
        game_stat = game.status()

        # decrementing the number of available positions on the board
        pos -= 1

    if train_model:
        # adding the outcome feature to all of our game states
        for state in match_states:
            # state["outcome"] = game_stat[1] # removing this for now
            state["first"] = bot_first

            # if bot lost, we want it to make literally anything other move so we feed it back ################################ THIS NEEDS TO BE CHANGED TO ACCOUNT ONLY FOR MOVES AVAILABLE ON THE BOARD DUDE WTF ####################################
            ################### Maybe only update labels where the models probability was below a threshold
            # If the model was extremely confident in a decision, it likely won multiple times that way so we shouldn't change it. We should only change what the model seems uncertain about.
            if game_stat[1] != 1:
                state["label"] = random.randint(1, 9)

        # steps to take if our agent is aware of who played first
        if first_tracked:
            # used dataframes to convert into numpy arrays since I think this is faster than parsing data from hundreds of dictionaries
            cols = [x for x in range(1, 10)] + [
                "first"
            ]  # removing this for now + ["outcome"]
        else:
            cols = [x for x in range(1, 10)]  # removing this for now + ["outcome"]

        df = pd.DataFrame(match_states)
        X = df[cols].values
        y = df["label"].values

        if training_type == "sparse" and game_stat[1] == 1:
            model.partial_fit(X, y, [x for x in range(1, 10)])

        if training_type == "dense" and game_stat:
            model.partial_fit(X, y, [x for x in range(1, 10)])

    if print_board:
        print(game.print())

    return game_stat[1], pd.DataFrame(match_states)


def bot_vs_bot_environment(
    model1: MLPClassifier,
    model2: MLPClassifier,
    random_order: bool = True,
    first_tracked: bool = True,
    train_model1: bool = False,
    train_model2: bool = False,
    training_type: str = "dense",
    print_board: bool = False,
):
    # TTT instance
    game = Board()
    # track number of positions open on the board
    pos = 9

    # randomly choosing first player
    if random_order and random.randint(0, 1):
        m1 = model2
        m2 = model1
    else:
        m1 = model1
        m2 = model2

    # function that returns a list of all outputs from the model in order from most to least recommended
    # this allows us to take an alternate option if the space is unavailable
    def ordered_options(model, classes, vector):
        # geting output values for each class

        probs = model.predict_proba(vector)
        # constructing dictionary of classes and probabilities

        d = {classes[i]: probs[0][i] for i in range(len(classes))}
        # returning a list classes in order of most likely to least likely

        result = sorted(d, key=d.get, reverse=True)
        return result

    # list to track all events in the match
    match_states1 = list()
    match_states2 = list()
    # initial game status for the loop
    game_stat = game.status()

    while pos > 0 and not game_stat[0]:

        # this iterations match state
        state = dict()
        # adding the vectorized game board to the state
        if pos % 2 != 0:
            for idx, elem in enumerate(game.vector):
                state[idx + 1] = elem
        else:
            for idx, elem in enumerate([-x for x in game.vector]):
                state[idx + 1] = elem

        # adding our additional feature
        # if our agent is aware of who plays first
        if first_tracked and pos % 2 != 0:
            v = game.vector + [1]
        elif first_tracked and pos % 2 == 0:
            v = [-x for x in game.vector] + [0]
        # if our agent is aware of the desired outcome (winning) and not player order
        elif not first_tracked and pos % 2 != 0:
            v = game.vector
        else:
            v = [-x for x in game.vector]

        # converting to 2D numpy array
        mod_board = np.array([v])

        # making different plays and tracking the decisions made
        if pos % 2 != 0:
            choices = ordered_options(m1, m1.classes_, mod_board)

            for c in choices:
                move = ((c - 1) // 3, (c - 1) % 3)
                b = game.move(row=move[0], column=move[1], player=1)

                if b:
                    state["label"] = c
                    break

            match_states1.append(state)

        else:
            choices = ordered_options(m2, m2.classes_, mod_board)

            for c in choices:
                move = ((c - 1) // 3, (c - 1) % 3)
                b = game.move(row=move[0], column=move[1], player=-1)

                if b:
                    state["label"] = c
                    break

            match_states2.append(state)
        # end play making

        # updating game status variable
        game_stat = game.status()

        # decrementing the number of available positions on the board
        pos -= 1

    if train_model1:
        # adding the outcome feature to all of our game states
        for state in match_states1:
            # state["outcome"] = game_stat[1] # removing this for now
            state["first"] = 1

        # steps to take if our agent is aware of who played first
        if first_tracked:
            # used dataframes to convert into numpy arrays since I think this is faster than parsing data from hundreds of dictionaries
            cols = [x for x in range(1, 10)] + [
                "first"
            ]  # removing this for now + ["outcome"]
        else:
            cols = [x for x in range(1, 10)]  # removing this for now + ["outcome"]

        df1 = pd.DataFrame(match_states1)
        X1 = df1[cols].values
        y1 = df1["label"].values

        if training_type == "sparse" and game_stat[1] == 1:
            m1.partial_fit(X1, y1, [x for x in range(1, 10)])

        if training_type == "dense":
            m1.partial_fit(X1, y1, [x for x in range(1, 10)])

    if train_model2:
        # adding the outcome feature to all of our game states
        for state in match_states2:
            # state["outcome"] = game_stat[1] # removing this for now
            state["first"] = 0

        # steps to take if our agent is aware of who played first
        if first_tracked:
            # used dataframes to convert into numpy arrays since I think this is faster than parsing data from hundreds of dictionaries
            cols = [x for x in range(1, 10)] + [
                "first"
            ]  # removing this for now + ["outcome"]
        else:
            cols = [x for x in range(1, 10)]  # removing this for now + ["outcome"]

        df2 = pd.DataFrame(match_states2)
        X2 = df2[cols].values
        y2 = df2["label"].values

        if training_type == "sparse" and game_stat[1] == 1:
            m2.partial_fit(X2, y2, [x for x in range(1, 10)])

        if training_type == "dense":
            m2.partial_fit(X2, y2, [x for x in range(1, 10)])

    if print_board:
        print(game.print())

    return game_stat[1]


def bot_vs_random(
    model: MLPClassifier,
    bot_first: bool = True,
    first_tracked: bool = True,
    print_board: bool = False,
):
    game = Board()
    pos = 9

    classes = model.classes_

    def ordered_options(vector):
        # geting output values for each class
        probs = model.predict_proba(vector)
        # constructing dictionary of classes and probabilities
        d = {classes[i]: probs[0][i] for i in range(len(classes))}
        # returning a list classes in order of most likely to least likely
        return sorted(d, key=d.get, reverse=True)

    while pos > 0 and not game.status()[0]:

        coords = gt.avail_moves(game.board)

        # adding our additional feature
        # if our agent is aware of who plays first
        if first_tracked:
            v = game.vector + [bot_first] + [1]
        # if our agent is aware of the desired outcome (winning)
        else:
            v = game.vector + [1]

        # converting to 2D numpy array
        mod_board = np.array([v])

        if bot_first and pos % 2 != 0:
            choices = ordered_options(mod_board)

            for c in choices:
                move = ((c - 1) // 3, (c - 1) % 3)
                b = game.move(row=move[0], column=move[1], player=1)

                if b:
                    break

        elif not bot_first and pos % 2 != 0:
            move = random.choice(coords)

            game.move(row=move[0], column=move[1], player=-1)

        elif bot_first and pos % 2 == 0:
            move = random.choice(coords)

            game.move(row=move[0], column=move[1], player=-1)

        elif not bot_first and pos % 2 == 0:
            choices = ordered_options(mod_board)

            for c in choices:
                move = ((c - 1) // 3, (c - 1) % 3)
                b = game.move(row=move[0], column=move[1], player=1)

                if b:
                    break

        pos -= 1

    if print_board:
        print(game.print())

    return game.status()[1]
