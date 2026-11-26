# 09 · Teaching an AI to cross a Lagos road

A reinforcement learning agent learns, by trial and error, to cross a busy 4-lane road full of
cars, fast danfos and okadas that speed up at random.

**How it works:** tabular Q-learning. The agent can only step **forward**, step **back** or **wait**,
and it only sees where it is and how close the nearest approaching vehicle is in its lane and the next one.
Crossing earns +10, getting hit costs −10, and every step costs a little so it doesn't dawdle.

```bash
python road_ai.py
```

**What I found**
- No brain (random moves): crossed **14%**, hit **86%**
- After 20,000 attempts: crossed **97%**, hit **3%**. Nobody taught it to wait for a gap; it learned that by itself
- Twist: make getting hit cost 100× more and make waiting free, and it learns the "safest" strategy ever:
  **never cross the road** (0% hit, 0% crossed). The AI doesn't do what you want; it does what you reward.
