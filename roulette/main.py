from collections import deque

import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import math
import random
import matplotlib.pyplot as plt

from roulette.environment import Roulette

step_size = 0.001
runs = 10_000_000

if __name__ == "__main__":
    env = Roulette()

    max_history = 2
    history_rewards = [[] for _ in range(max_history)]
    for history in [0, 1, 5, 10]:
        q_table_size = (3,) * history + (2,)
        q_table = np.zeros(q_table_size)
        past_hist = deque(maxlen=history)
        for _ in range(history): past_hist.append(2)  # fill with green

        total_reward, reward_history, history_buffer = 0, [], []
        observation = tuple(past_hist)
        for i in range(runs):
            action = np.argmax(q_table[observation])
            obs, reward = env.step(action)
            q_table[observation + (action,)] = (reward * step_size) + (q_table[observation + (action,)] * (1 - step_size))

            past_hist.append(obs)
            observation = tuple(past_hist)

            total_reward += reward
            history_buffer += [total_reward / (i + 1)]
            if len(history_buffer) == runs / 1000:
                reward_history += [np.mean(history_buffer)]
                history_buffer = []

        print(q_table)
        plt.plot([i for i in range(len(reward_history))], [i for i in reward_history], label=f"{history}")

    plt.ylim(0, 1)
    plt.legend()
    plt.show()
