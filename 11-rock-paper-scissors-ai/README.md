# 11 · An AI that reads your rock-paper-scissors habits

The AI never sees your hand. It only remembers your past moves ("the last two times you played X then Y,
what came next?") and plays whatever beats your most likely next move. That's an **order-2 Markov model**, built from scratch.

```bash
python rps_ai.py
```

**What I found** (1,000 rounds, averaged over 50 matches)

| Opponent | AI wins | Ties | AI loses |
|---|---|---|---|
| "Rock is strongest" friend (rock 50% of the time) | **48.2%** | 25.6% | 26.2% |
| Human habits (win → repeat, lose → switch, never 3 in a row) | **57.4%** | 22.3% | 20.3% |
| Truly random | 33.3% | 33.4% | 33.2% |

The only way to beat it is to have no habits, and humans are terrible at being random.
