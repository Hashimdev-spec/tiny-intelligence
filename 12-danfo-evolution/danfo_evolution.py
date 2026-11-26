"""Dayo Tries #12: I evolved danfo drivers with natural selection.

Each driver is a tiny neural network (13 inputs -> 8 hidden -> 5 outputs).
The road has 3 lanes, potholes, slow cars, and passengers waiting at the roadside.
A driver picks up a passenger by being in the kerb lane (lane 0) and driving SLOW past them.
Hit a pothole or a car = trip over.

Natural selection: 100 random drivers -> keep the best 10 -> they have mutated children -> repeat.
"""
import numpy as np

LANES, LENGTH, VIEW = 3, 400, 12
N_IN, N_HID, N_OUT = 3 + LANES + 2 + 2, 8, 5     # see sense() for the 10 inputs


def make_road(rng):
    pot = rng.random((LENGTH, LANES)) < 0.03              # potholes
    pot[:15] = False
    cars = []                                               # slow cars: [lane, position]
    for x in range(30, LENGTH, 25):
        if rng.random() < 0.7:
            cars.append([int(rng.integers(LANES)), float(x)])
    pax = sorted(int(x) for x in rng.choice(np.arange(20, LENGTH), 20, replace=False))   # passengers at kerb
    return pot, cars, pax


def sense(lane, pos, speed, pot, cars, pax_left):
    ahead = []
    for l in range(LANES):                                  # distance to next obstacle in each lane
        d = VIEW
        for k in range(1, VIEW):
            p = int(pos) + k
            if p < LENGTH and pot[p, l]:
                d = k; break
        for cl, cp in cars:
            if cl == l and 0 < cp - pos < d:
                d = cp - pos
        ahead.append(d / VIEW)
    lane_1h = [1.0 if lane == l else 0.0 for l in range(LANES)]
    nxt = next((x for x in pax_left if x >= pos), None)
    dpax = min(VIEW, nxt - pos) / VIEW if nxt is not None else 1.0
    return np.array(ahead + lane_1h + [speed / 2.0, dpax, 1.0, 0.0])


def drive(w, seed, fitness="pax", record=False):
    rng = np.random.default_rng(seed)
    pot, cars, pax = make_road(rng)
    W1, W2 = w
    lane, pos, speed, picked, frames, crash = 0, 0.0, 1, 0, [], None
    pax_left = list(pax)
    for t in range(800):
        h = np.tanh(sense(lane, pos, speed, pot, cars, pax_left) @ W1)
        o = h @ W2
        lane = int(np.clip(lane + [-1, 0, 1][int(np.argmax(o[:3]))], 0, LANES - 1))
        speed = 1 if o[3] > o[4] else 2                     # slow or fast
        for c in cars:
            c[1] += 0.5                                      # traffic crawls along
        start = pos
        pos += speed
        if record:
            frames.append((lane, pos, speed, picked, [tuple(c) for c in cars]))
        for p in range(int(start) + 1, int(pos) + 1):        # anything we drove over?
            if p < LENGTH and pot[p, lane]:
                crash = "pothole"
        for cl, cp in cars:
            if cl == lane and start < cp <= pos + 0.5:
                crash = "car"
        while pax_left and pax_left[0] <= pos:
            x = pax_left.pop(0)
            if lane == 0 and speed == 1:
                picked += 1
        if crash or pos >= LENGTH:
            break
    score = {"pax": pos + 40 * picked,              # balanced: distance + passengers
             "distance": pos,                       # only distance matters
             "money": 40 * picked}[fitness]         # only passengers (money) matter
    out = dict(distance=min(pos, LENGTH), passengers=picked, crash=crash, finished=pos >= LENGTH, score=score)
    if record:
        out.update(frames=frames, pot=pot, pax=pax)
    return out


def evaluate(w, seeds, fitness="pax"):
    return np.mean([drive(w, s, fitness)["score"] for s in seeds])


def evolve(generations=80, pop=100, elite=10, seed=0, fitness="pax", log=True):
    rng = np.random.default_rng(seed)
    P = [(rng.normal(0, 1, (N_IN, N_HID)), rng.normal(0, 1, (N_HID, N_OUT))) for _ in range(pop)]
    history = []
    for g in range(generations):
        seeds = [1000 * g + k for k in range(6)]             # new roads every generation: no memorising
        scores = np.array([evaluate(w, seeds, fitness) for w in P])
        order = np.argsort(-scores)
        best = P[order[0]]
        test = [drive(best, 999_000 + k, fitness) for k in range(20)]
        stats = dict(gen=g + 1, best=float(scores[order[0]]), avg=float(scores.mean()),
                     test_distance=float(np.mean([r["distance"] for r in test])),
                     test_passengers=float(np.mean([r["passengers"] for r in test])),
                     test_finished=float(np.mean([r["finished"] for r in test])))
        history.append(stats)
        if log and (g == 0 or (g + 1) % 10 == 0):
            print(f"gen {g + 1:3d}: best driver on fresh roads -> {stats['test_distance']:5.0f} m, "
                  f"{stats['test_passengers']:4.1f} passengers, finished {stats['test_finished']:4.0%} of trips")
        parents = [P[i] for i in order[:elite]]
        children = list(parents)
        while len(children) < pop:
            a = parents[rng.integers(elite)]
            children.append(tuple(m + rng.normal(0, 0.25, m.shape) * (rng.random(m.shape) < 0.2) for m in a))
        P = children
    return P[0], history


def behaviour(w, fitness="pax", n=20):
    """how does a driver actually drive? (on 20 roads it has never seen)"""
    runs = [drive(w, 999_000 + k, fitness, record=True) for k in range(n)]
    return dict(distance=np.mean([r["distance"] for r in runs]), passengers=np.mean([r["passengers"] for r in runs]),
                finished=np.mean([r["finished"] for r in runs]),
                kerb_lane=np.mean([np.mean([f[0] == 0 for f in r["frames"]]) for r in runs]),
                slow=np.mean([np.mean([f[2] == 1 for f in r["frames"]]) for r in runs]),
                pothole_crashes=sum(r["crash"] == "pothole" for r in runs), car_crashes=sum(r["crash"] == "car" for r in runs))


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "pax"     # pax | distance | money
    print(f"Evolving 100 danfo drivers for 80 generations (reward: {mode})")
    best, hist = evolve(fitness=mode)
    b = behaviour(best, mode)
    print(f"\nBest evolved driver on 20 new roads:")
    print(f"  {b['distance']:.0f} m per trip, {b['passengers']:.1f} passengers, finished {b['finished']:.0%} of trips")
    print(f"  drives in the kerb lane {b['kerb_lane']:.0%} of the time, drives slow {b['slow']:.0%} of the time")
    print(f"  trips ended by potholes: {b['pothole_crashes']}/20, by cars: {b['car_crashes']}/20")
