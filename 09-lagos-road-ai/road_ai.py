"""Dayo Tries #9: I taught an AI to cross a Lagos road.

Tabular Q-learning. The agent stands on one side of a 4-lane road and can
step FORWARD, BACK or WAIT. Each step it sees only:
  - which row it is on (pavement, lane 1-4, other side)
  - how close the nearest approaching vehicle is in its own lane
  - how close the nearest approaching vehicle is in the next lane
Vehicles: cars (steady), danfos (fast), okadas (sometimes speed up at random).
"""
import random

LANES, WIDTH, COL = 4, 21, 10           # agent always crosses at column 10
GOAL = LANES + 1                        # row 0 = start pavement, rows 1-4 = lanes, row 5 = other side
ACTIONS = ["forward", "back", "wait"]
KINDS = {"car": 1, "danfo": 2, "okada": 1}   # base speed in cells per step


class Road:
    def __init__(self, rng, density=0.13):
        self.rng, self.density = rng, density
        self.dirs = [1 if l % 2 == 0 else -1 for l in range(LANES)]   # alternate directions
        self.v = [[] for _ in range(LANES)]       # vehicles: [x, kind]
        for _ in range(40):                        # warm up so the road is already busy
            self.tick()

    def speed(self, kind):
        s = KINDS[kind]
        if kind == "okada" and self.rng.random() < 0.35:
            s += 1                                  # okada: unpredictable burst
        return s

    def tick(self):
        """move every vehicle; return set of (lane, x) cells each vehicle swept through this step"""
        swept, self.hit_by = set(), {}
        for l in range(LANES):
            d, keep = self.dirs[l], []
            for veh in self.v[l]:
                s = self.speed(veh[1])
                for k in range(1, s + 1):
                    self.hit_by[(l, veh[0] + d * k)] = veh[1]
                    swept.add((l, veh[0] + d * k))
                veh[0] += d * s
                if 0 <= veh[0] < WIDTH:
                    keep.append(veh)
            self.v[l] = keep
            if self.rng.random() < self.density:
                edge = 0 if d == 1 else WIDTH - 1
                if all(abs(veh[0] - edge) > 2 for veh in self.v[l]):
                    kind = self.rng.choices(["car", "danfo", "okada"], [0.5, 0.25, 0.25])[0]
                    self.v[l].append([edge, kind])
                    self.hit_by[(l, edge)] = kind
                    swept.add((l, edge))
        return swept

    def gap(self, lane):
        """distance bucket (0-3) of nearest vehicle still coming towards the crossing column"""
        if lane < 0 or lane >= LANES:
            return 3
        d, best = self.dirs[lane], 99
        for x, _ in self.v[lane]:
            dist = (COL - x) * d
            if dist >= 0:
                best = min(best, dist)
        return 0 if best <= 1 else 1 if best <= 3 else 2 if best <= 6 else 3


def observe(road, row):
    return (row, road.gap(row - 1), road.gap(row))      # (where I am, my lane, next lane)


def episode(Q, rng, eps, alpha=0.2, gamma=0.95, step_cost=-0.05, hit=-10.0, goal=10.0, max_steps=60, log=False):
    road, row = Road(rng), 0
    path = []
    s = observe(road, row)
    for t in range(max_steps):
        if rng.random() < eps:
            a = rng.randrange(3)
        else:
            q = Q.get(s, [0.0, 0.0, 0.0])
            a = max(range(3), key=lambda i: (q[i], -i))
        row = min(GOAL, row + 1) if a == 0 else max(0, row - 1) if a == 1 else row
        swept = road.tick()
        if log:
            path.append((row, [[(veh[0], veh[1]) for veh in lane] for lane in road.v]))
        if 1 <= row <= LANES and (row - 1, COL) in swept:
            r, done, out = hit, True, "hit by " + road.hit_by[(row - 1, COL)]
        elif row == GOAL:
            r, done, out = goal, True, "crossed"
        else:
            r, done, out = step_cost, False, None
        s2 = observe(road, row)
        q = Q.setdefault(s, [0.0, 0.0, 0.0])
        target = r if done else r + gamma * max(Q.get(s2, [0.0, 0.0, 0.0]))
        q[a] += alpha * (target - q[a])
        s = s2
        if done:
            return out, t + 1, path
    return "never crossed", max_steps, path


def summary(outs):
    n = len(outs)
    hits = [o for o in outs if o.startswith("hit")]
    return {"crossed": outs.count("crossed") / n, "hit": len(hits) / n, "never crossed": outs.count("never crossed") / n,
            "hit by": {k: hits.count("hit by " + k) for k in KINDS}}


def train(n=20000, seed=1, report_every=None, **kw):
    rng, Q, hist = random.Random(seed), {}, []
    for i in range(n):
        eps = max(0.02, 1.0 - i / (n * 0.6))          # explore a lot early, then trust what it learned
        out, steps, _ = episode(Q, rng, eps, **kw)
        hist.append(out)
        if report_every and (i + 1) % report_every == 0:
            w = summary(hist[-report_every:])
            print(f"attempts {i + 2 - report_every:>6}-{i + 1:<6} crossed {w['crossed']:6.1%}  hit {w['hit']:6.1%}"
                  f"  never crossed {w['never crossed']:6.1%}")
    return Q, hist


def evaluate(Q, n=2000, seed=99, eps=0.0, **kw):
    rng = random.Random(seed)
    runs = [episode(Q, rng, eps, alpha=0.0, **kw) for _ in range(n)]
    return summary([r[0] for r in runs]), sum(r[1] for r in runs) / n


def show(label, res):
    s_, avg = res
    print(f"{label}: crossed {s_['crossed']:.1%} | hit {s_['hit']:.1%} {s_['hit by']} | never crossed {s_['never crossed']:.1%}"
          f" | avg steps {avg:.1f}")


if __name__ == "__main__":
    show("No brain (random moves)", evaluate({}, eps=1.0))

    print("\nTraining: 20,000 attempts")
    Q, _ = train(20000, report_every=2000)
    show("\nTrained AI on 2,000 new roads", evaluate(Q))

    print("\nTwist: getting hit costs 100x more, waiting is free")
    Q2, _ = train(20000, hit=-1000.0, step_cost=0.0, report_every=4000)
    show("Scared AI on 2,000 new roads", evaluate(Q2, hit=-1000.0, step_cost=0.0))
