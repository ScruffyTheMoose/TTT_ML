![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)


`TTT ML` is a research repository looking at different approaches to training machine learning algorithms to play Tic-Tac-Toe (TTT).

[Project Overview](https://github.com/ScruffyTheMoose/TTT_ML/blob/master/walkthrough.ipynb)

## model_binaries
Binaries of compiled models that can be loaded elsewhere.

## model_builds
Jupyter Notebooks where we are building different models.

## model_evaluations
Jupyter Notebooks comparing and evaluating the performance of different models.

## data
The sample data generator notebook is located here along with the data sets it has been used to build. These datasets are structured so that they are easy to use with Pandas.

## tests
You can ignore this. We need to test basic functions every time we change up things about the main TTT module, and we use these tests to do it quickly.

## Modules

### TicTacToe.py
This python file contains two classes:
- Board: class which contains a functioning TTT game
- GameTools: contains the random match generator and a few other tools for working with TTT boards

### Sample.py
A module that generates samples for a training set based on a number of parameters and can save the dataset to a file.
- n_samples: int
- save_file: bool
- directory: save directory
- rand_first_player: bool
- first_player: int, if not rand_first_player
- open_space_range: the lower and upper bound for choosing open spaces on a board
- shuffled: bool

### play.py
If you want to play the game against another human player through your command line, you can run this file. We aim to use this module later on so a person can play against an AI.

### minimax.py
Ignore this. It's not done and probably will be deleted since we are working on different approaches.
