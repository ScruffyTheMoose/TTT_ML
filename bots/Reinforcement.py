# we can potentially use our metrics from the clustering (assuming shorter euclidian distance = in favor of player X/O) to make static evaluations of a game board for reinforcement learning
# in other words, did the last move improve our position? if so, reward.
# maybe this should be contrasted against whether or not the opponents position was decreased. It is possible that a move for X may both benefit X and O.
# ^ this line of thought can be easily applied to a decision tree to find a 'compromise' move which best helps X and damages O
