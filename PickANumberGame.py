from copy import copy, deepcopy
import time
import random
from AI import AI


class PickANumberGame:
    def __init__(self, players, choice=range(1, 10), compare=None):
        self.choice = choice
        self.players = players
        self.player_id = {p: i for i, p in enumerate(self.players)}
        self.compare = compare if compare is not None else PickANumberGame.default_compare

        self.full_result = {c: 0 for c in self.choice}
        self.result = None
        self.history = {"result": list(), "full_result": list()}

        self.final_candidates = list()

    @staticmethod
    def default_compare(freq_dict):
        final_candidates = list()
        current_max = min(freq_dict.values())
        for c in freq_dict:
            if freq_dict[c] == current_max:
                final_candidates.append(c)
        return random.choice(final_candidates)

    def reset_result(self):
        self.full_result = {c: 0 for c in self.choice}
        self.result = None

    def play(self):
        self.reset_result()
        players_choice = list()
        for p in self.players:
            p_choice = p.get_move()
            players_choice.append(p_choice)
            self.full_result[p_choice] += 1
        self.process_result()
        for p in self.players:
            p.process_result(self.result)
        return self.result

    def process_result(self):
        self.result = self.compare(self.full_result)

    def append_history(self, players_choice):
        self.history["result"].append(self.result)
        self.history["full_result"].append(players_choice)

    def get_choice(self):
        return copy(self.choice)

    def get_full_result(self):
        return copy(self.full_result)

    def get_result(self):
        return self.result






def start_game(game: PickANumberGame, count: int):
    t = time.time()
    for i in range(count):
        result = game.play()
    print(count, "GAMES IN", time.time() - t, "SECONDS")
    print("=================")
    policy_dict = {c: 0 for c in game.get_choice()}     # find distribution of deterministic policy among players
    for i, p in enumerate(game.players):
        print("PLAYER", i, "stats:")
        p_dis = {c: p.play_count[c] / sum(p.play_count.values()) for c in p.play_count}
        print("play distribution:", p_dis)
        for c in p_dis:
            if p_dis[c] > 0.6:
                policy_dict[c] += 1
                break
        # print("normalized reward per choice:", p.reward)
        print("total reward:", p.total_reward)
        print("rounds won:", p.win_count)
        # if type(p) is AI.UCB_AI:
        #     print(p.prior_reward)
        #     print(p.prior_strength)
        print("=================")
    print("POLICY DISTRIBUTION", {c: policy_dict[c]/sum(policy_dict.values()) for c in policy_dict})
    print(policy_dict)
    print("____________________________________________________\n")