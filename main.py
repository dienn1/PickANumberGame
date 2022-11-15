import math
from PickANumberGame import PickANumberGame, start_game
from AI import UCB_AI, RandomAI, AI
import random

random.seed(69)


if __name__ == "__main__":
    choice = range(1, 4)
    AI_count = 5
    game_count = 1000000
    max_prior_strength = 100
    explore_param = math.sqrt(2)

    players: list[AI] = list()
    for _ in range(AI_count):
        prior_reward = [random.random() for __ in range(len(choice))]
        prior_strength = [random.random()*max_prior_strength for ___ in range(len(choice))]
        p = UCB_AI(choice, explore_param=explore_param, prior_reward=prior_reward, prior_strength=prior_strength)
        players.append(p)
    # weights = [random.random() for __ in range(len(choice))]
    # weights = [0 for _ in range(len(choice))]
    # weights[-1] = 1
    # players.append(RandomAI(choice, weights=weights))
    game = PickANumberGame(players, choice=choice)

    start_game(game, game_count)
    start_game(game, game_count)


