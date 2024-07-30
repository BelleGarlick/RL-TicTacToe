import random


class Roulette:
    def __init__(self, american=False):
        self.obserable_numbers = 38 if american else 37
        self.actions = 2
        self.observations = 3
        self.history = []

    def __spin(self):
        """
        There are 37 / 38 obserable numbers, we spin a value includively between them.
        """
        random_number = random.randint(0, self.obserable_numbers - 1)
        if random_number < 18:
            return 0
        elif random_number < 36:
            return 1
        else:
            return 2

    def step(self, action):
        result = self.__spin()
        if action == result:
            return result, 2
        return result, -1
