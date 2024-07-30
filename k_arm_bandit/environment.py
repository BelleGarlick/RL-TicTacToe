import random


class Environment:
    def __init__(self, k=3):
        self.__tq_values = [random.random() for _ in range(k)]

    def step(self, action):
        if action < len(self.__tq_values):
            return self.__tq_values[action] + (random.random() * 2 - 1)
        raise IndexError(f"The given action '{action}' is out of bounds for k={len(self.__tq_values)}")