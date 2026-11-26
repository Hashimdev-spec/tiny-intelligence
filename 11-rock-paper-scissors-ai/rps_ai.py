"""Dayo Tries #11: I built an AI that reads your rock-paper-scissors habits.

The AI never sees your hand. It only remembers your past moves:
"the last 2 times this person played X then Y, what did they play next?"
Then it plays whatever beats your most likely next move (an order-2 Markov model).
"""
import random
from collections import Counter, defaultdict

MOVES = "RPS"
BEATS = {"R": "P", "P": "S", "S": "R"}          # BEATS[x] = the move that beats x
NAME = {"R": "rock", "P": "paper", "S": "scissors"}


def result(a, b):
    """+1 if a beats b, 0 tie, -1 loss"""
    return 0 if a == b else (1 if BEATS[b] == a else -1)


class HabitAI:
    def __init__(self, rng, order=2):
        self.rng, self.order, self.seen = rng, order, defaultdict(Counter)

    def move(self, history):
        key = tuple(history[-self.order:])
        if len(history) >= self.order and self.seen[key]:
            guess = self.seen[key].most_common(1)[0][0]          # their most likely next move
            return BEATS[guess]
        return self.rng.choice(MOVES)

    def learn(self, history, their_move):
        if len(history) >= self.order:
            self.seen[tuple(history[-self.order:])][their_move] += 1


# ---- opponents --------------------------------------------------------------
def rock_lover(rng, mine, theirs, results):
    """'rock is strongest': rock half the time"""
    return rng.choices(MOVES, [0.5, 0.25, 0.25])[0]


def human_habits(rng, mine, theirs, results):
    """habits researchers keep finding in real players:
    win -> often play the same move again; lose -> often switch to the next move in R->P->S;
    and people avoid playing the same move 3 times in a row because it 'doesn't feel random'"""
    if not mine:
        return rng.choice(MOVES)
    last, r = mine[-1], results[-1]
    if r == 1 and rng.random() < 0.6:
        m = last                                          # win-stay
    elif r == -1 and rng.random() < 0.6:
        m = BEATS[last]                                   # lose-shift (R->P->S)
    else:
        m = rng.choice(MOVES)
    if len(mine) >= 2 and mine[-1] == mine[-2] == m:      # "too many in a row, switch"
        m = rng.choice([x for x in MOVES if x != m])
    return m


def truly_random(rng, mine, theirs, results):
    return rng.choice(MOVES)


def play(opponent, rounds=1000, seed=0):
    rng = random.Random(seed)
    ai = HabitAI(random.Random(seed + 1))
    opp_moves, ai_moves, opp_results, log = [], [], [], []
    for _ in range(rounds):
        a = ai.move(opp_moves)
        o = opponent(rng, opp_moves, ai_moves, opp_results)
        ai.learn(opp_moves, o)
        r = result(a, o)
        opp_moves.append(o); ai_moves.append(a); opp_results.append(-r); log.append(r)
    return log, opp_moves, ai_moves


def rates(log):
    n = len(log)
    return log.count(1) / n, log.count(0) / n, log.count(-1) / n


if __name__ == "__main__":
    print("AI result over 1,000 rounds (averaged over 50 matches):")
    for name, opp in (("Rock lover", rock_lover), ("Human habits", human_habits), ("Truly random", truly_random)):
        w = t = l = 0; first20 = []
        for seed in range(50):
            log, _, _ = play(opp, seed=seed)
            a, b, c = rates(log); w += a; t += b; l += c
            first20.append(log[:20].count(1) / 20)
        print(f"  vs {name:13s} AI wins {w / 50:5.1%} | ties {t / 50:5.1%} | AI loses {l / 50:5.1%}"
              f"   (first 20 rounds: AI wins {sum(first20) / 50:5.1%})")

    log, opp, ai = play(human_habits, rounds=100, seed=7)
    print("\nOne 100-round match vs human habits: AI won", log.count(1), "tied", log.count(0), "lost", log.count(-1))
