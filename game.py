import random
import json


class DynamicDarts:
    def __init__(self, nb_players, probability):
        self.nb_players = nb_players
        self.probability = probability
        self.players = [Player(f"Player {i}") for i in range(1, nb_players + 1)]
        self.current_player = nb_players - 1
        self.modifiers = json.load(open("data/modifiers.json", encoding="utf-8"))
        self.challenges = json.load(open("data/challenges.json", encoding="utf-8"))
        self.current_challenge = None
        self.current_challenge_difficulty = None
        self.current_modifier_is_bonus = None
        self.current_modifier = None

    def next_turn(self, success):
        self.resolve_challenge(success)
        self.next_player()

    def resolve_challenge(self, success):
        self.players[self.current_player].modifiers = []
        if self.current_challenge is None:
            return
        if self.current_modifier_is_bonus:
            if success:
                if self.current_modifier.startswith("Donne un"):
                    target_player = int(self.current_modifier[-1]) - 1
                    new_modifier = self.new_modifier(False, 4 - self.current_challenge_difficulty)
                    self.players[target_player].modifiers.append(new_modifier)
                else:
                    self.players[self.current_player].modifiers.append(self.current_modifier)
        else:
            if not success:
                self.players[self.current_player].modifiers.append(self.current_modifier)

    def next_player(self):
        self.current_player = (self.current_player + 1) % self.nb_players
        if random.random() < self.probability:
            self.current_modifier, self.current_challenge = self.new_modifier_challenge()
        else:
            self.current_modifier = None
            self.current_challenge = None

    def get_current_player(self):
        return self.players[self.current_player]

    def new_modifier_challenge(self):
        self.current_challenge_difficulty = random.randint(1,3)
        challenges, weights = zip(*self.challenges[str(self.current_challenge_difficulty)])
        new_challenge = random.choices(challenges, weights)[0]

        self.current_modifier_is_bonus = random.random() < 0.5
        new_modifier = self.new_modifier(self.current_modifier_is_bonus, self.current_challenge_difficulty)

        return new_modifier, new_challenge
    
    def new_modifier(self, is_bonus, challenge_difficulty):
        if is_bonus:
            bonus_level = challenge_difficulty
            new_modifier = random.choice(self.modifiers['+'+str(bonus_level)])
            if new_modifier.startswith("Donne un"):
                new_modifier = new_modifier.replace("X", str(random.choice([i+1 for i in range(self.nb_players) if i != self.current_player])))
        else:
            penalty_level = -(4 - challenge_difficulty)
            new_modifier = random.choice(self.modifiers[str(penalty_level)])

        return new_modifier

class Player:
    def __init__(self, name):
        self.name = name
        self.modifiers = []
