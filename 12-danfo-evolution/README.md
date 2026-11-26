# 12 · Evolving danfo drivers with natural selection

A **genetic algorithm** evolves tiny neural-network drivers (10 inputs → 8 hidden → 5 outputs, NumPy only)
on a 3-lane Lagos road with potholes, slow cars and passengers waiting at the kerb.

**How it works:** 100 drivers with random brains each drive 6 random roads. The best 10 survive and have
mutated children. Repeat for 80 generations. Every generation gets brand-new roads, so they can't memorise one.

```bash
python danfo_evolution.py          # reward = distance + 40 per passenger
python danfo_evolution.py money    # reward = passengers only
python danfo_evolution.py distance # reward = distance only
```

**What I found** (tested on 20 roads the drivers had never seen)

| | Generation 1 | Generation 80 |
|---|---|---|
| Distance per trip | 51 m (average driver) | **284 m** (best driver) |
| Passengers picked up | 2.8 (best driver) | **13.2** |
| Trips finished | 0% | **35%** |
| Time spent driving slow | 53% (whole population) | **99.8%** |
| Time in the kerb lane | 63% | **91%** |

Nobody told them to slow down or hug the roadside: fast drivers kept dying, and passengers live at the kerb.
What still ends most trips? **Potholes** (11 of 20), not other cars (2 of 20).
