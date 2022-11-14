![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)


`TTT ML` is a research repository looking at different approaches to training machine learning algorithms to play Tic-Tac-Toe (TTT).

The resulting models were built using a combination of incrementally training a dense neural network in a reinforcement training environment.

## Training Process
After testing numerous possible solutions, the most success was found by tracking and scoring every game state and move seen in the environment based on its historical performance.

Every game state seen in the environment has 9 associate labels for the 9 possible moves that could be made. This data is stored in a hashmap (python dictionary). The game state is hashed to be used as a key, the the possible moves are stored as the associated value in an array. The dictionary is called the 'state data'.

In TTT, there is a finite number of game states. There are 4520 incomplete game states. For every incomplete game state that the model sees, there are several potential moves that could be made. In order to ensure the model is exposed to as many game states and moves as possible, a randomness parameter was added. Usually set to 0.5, this means that 50% of the time a random move will be made rather than a move based on the models prediction. These random moves will update the scores in the 'state data'.

![training explained](https://raw.githubusercontent.com/ScruffyTheMoose/TTT_ML/master/Training%20Explained.jpg)

## Application
1)  Instantiate a Multi-Layer Perceptron multiclassifier using the SKL library
2)  Feed the model initial information about the game - ie: show the model a game state and a label
3)  Instantiate the training environment and give the environment a reference to the model
4)  Iteratively train the model in the environment, gradually improving its performance.

### model_binaries
Binaries of compiled models that can be loaded elsewhere.

### model_builds
Jupyter Notebooks that walk through the builds for each model.
