# RL-TicTacToe
An RL agent that learns to efficiently play the child game TicTacToe

## How it works
There are 255,168 possible games of TicTacToe which an AI could use to create a Min-Max tree and brute force the best game each time. However that seems fairly exhaustive to me. Instead this RL agent uses a simple look up table to learn a 'value' for each of the 19,683 possible board combinations. All permutations (symetry and rotations) are removed leaving just 1262 truly uniqe board states. For each of these unique combinations the AI learns a 'value' estimating how good the board state is towards winning - stored in a simple lookup table policy. At each time step the agent looks at all possible moves the it can take at looks up the value for winning - then performs the action with the highest value. Simple!

It learns using the temporal difference function:
<blockquote>
  V(s<sub>t</sub>) ←`V(s<sub>t</sub>) + η[V(s<sub>t+1</sub>) - V(s<sub>t</sub>)]
</blockquote>

In other words, the value in the current state is increased by  difference between the current and the next states multiplied by the learning rate.
This means that over time each value shifts slightly more towards the value of the future state. The states are initialised such that all winning states have value '1' and all losing states are value '-1', anything else (including draws) are set to a random value. The policy is learnt overtime using the afformentioned function by learning which states that lead towards a loss and which one leads towards a win. When training the agent always plays agains a policy which takes random actions, however, it could train using self play - a little tinkering is required but i've tried it and it does work. It takes about 10-30s to train.

## Licence
The Unlicence.

