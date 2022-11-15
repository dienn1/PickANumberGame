import math
import random
from abc import ABC, abstractmethod
from itertools import accumulate


class AI(ABC):
    def __init__(self, choice=range(1, 10)):
        self.total_count = 0
        self.win_count = 0
        self.total_reward = 0
        self.choice = choice
        self.move = None
        self.play_count = {c: 0 for c in self.choice}
        self.reward = {c: 0 for c in self.choice}

    @abstractmethod
    def get_move(self):
        pass

    def process_reward(self, reward):
        return reward

    def process_result(self, result):
        self.total_count += 1
        self.play_count[self.move] += 1
        if result == self.move:
            self.reward[self.move] += self.process_reward(self.move)
            self.total_reward += self.move
            self.win_count += 1


class RandomAI(AI):
    def __init__(self, choice=range(1, 10), weights=None):
        super(RandomAI, self).__init__(choice)
        if weights is None:
            self.weights =[1 for c in self.choice]
        else:
            self.set_weight(weights)
        # self.normalize_weights()

    def set_weight(self, weights):
        if type(weights) == dict:
            self.weights = [weights[c] for c in self.choice]
        else:
            self.weights = weights
        # self.normalize_weights()

    def normalize_weights(self):
        weight_sum = sum(self.weights)
        for i in range(len(self.weights)):
            self.weights[i] /= weight_sum

    def get_move(self):
        self.move = random.choices(self.choice, weights=self.weights)[0]
        return self.move


class TrueRandomAI(AI):
    def __init__(self, choice=range(1, 10)):
        super(TrueRandomAI, self).__init__(choice)
        self.randomAI = RandomAI(self.choice)

    def get_move(self):
        rand_weights = [random.random() for __ in range(len(self.choice))]
        self.randomAI.set_weight(rand_weights)
        self.move = self.randomAI.get_move()
        return self.move


class UCB_AI(AI):
    def __init__(self, choice=range(1, 10), prior_reward=None, prior_strength=None, explore_param=math.sqrt(2)):
        super(UCB_AI, self).__init__(choice)

        self.explore_param = explore_param

        self.count_padding = len(self.choice)

        self.reward_range = max(self.choice)
        self.move = None

        self.prior_reward = prior_reward
        self.prior_strength = prior_strength
        self._initialize_prior()

    def _initialize_prior(self):
        if self.prior_reward is None or self.prior_strength is None:
            return
        if type(self.prior_reward) == dict:
            self.prior_reward = {c: self.prior_reward[c] for c in self.choice}
        else:
            self.prior_reward = {c: w for c, w in zip(self.choice, self.prior_reward)}
        if type(self.prior_strength) == dict:
            self.prior_strength = {c: self.prior_strength[c] for c in self.choice}
        else:
            self.prior_strength = {c: w for c, w in zip(self.choice, self.prior_strength)}

    def average_reward(self, c):
        if self.play_count[c]:
            if self.prior_reward and self.prior_strength:
                r = (self.reward[c] + self.prior_reward[c] * self.prior_strength[c]) / (self.prior_strength[c] + self.play_count[c])
            else:
                r = self.reward[c] / self.play_count[c]
            return r
        return 0

    def ucb(self, c):
        avg_reward = self.average_reward(c)
        exploration_term = self.explore_param * math.sqrt(math.log(self.total_count+1) / (self.play_count[c] + 1))
        return avg_reward + exploration_term

    def ucb_selection(self):
        current_ucb = 0
        move = None
        for c in self.reward:
            ucb_c = self.ucb(c)
            # tiebreak with fair coin
            if move is None or ucb_c > current_ucb or (ucb_c == current_ucb and random.randint(0, 1)):
                current_ucb = ucb_c
                move = c
        return move

    def get_move(self):
        self.move = self.ucb_selection()
        return self.move

    def normalize_reward(self, reward):
        return reward/self.reward_range

    def process_reward(self, reward):
        return self.normalize_reward(reward)
