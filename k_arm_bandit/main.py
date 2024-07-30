import random as rnd
from k_arm_bandit.environment import Environment


K_BANDITS = 10
EPISODES = 1000
INITIAL_EPSILON = 0.1
EPSILON_DECAY = INITIAL_EPSILON / EPISODES

rnd.seed(3)


if __name__ == "__main__":
    # The true q*(a) values
    env = Environment(K_BANDITS)
    tq_values = [(rnd.random() * 2) for _ in range(K_BANDITS)]


    # the estimated Qt(a) values
    eq_values = [0 for _ in tq_values]
    results = [[] for _ in tq_values]


    # iterate through episodes
    epsilon, total_reward = INITIAL_EPSILON, 0
    for _ in range(EPISODES):
        # select action or random
        selected_action = rnd.randint(0, K_BANDITS - 1) if rnd.random() < epsilon else eq_values.index(max(eq_values))
        reward = env.step(selected_action)  # get the reward of the action

        total_reward += reward  # store reward
        results[selected_action] += [reward]  # add reward to the stored
        eq_values[selected_action] = sum(results[selected_action]) / len(results[selected_action])

        epsilon = max(0, epsilon - EPSILON_DECAY)  # decay epsilon

    #  output the total reward / the total obtainable reward (assuming no random variation)
    print(total_reward / (max(tq_values) * EPISODES))
