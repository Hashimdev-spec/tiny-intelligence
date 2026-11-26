"""Dayo Tries #6 - I simulated traffic (Nagel-Schreckenberg model): jams out of nothing."""
import random, json

def simulate(n_cars, L=400, vmax=5, p_brake=0.3, steps=600, seed=1, danfo=None):
    """cars on a ring road. danfo=(car_index, start_step, duration): that car stops to pick passengers."""
    r = random.Random(seed)
    pos = sorted(r.sample(range(L), n_cars)); vel = [0] * n_cars
    hist = []
    for t in range(steps):
        new_v = []
        for i in range(n_cars):
            gap = (pos[(i + 1) % n_cars] - pos[i] - 1) % L
            v = min(vel[i] + 1, vmax, gap)                       # accelerate, don't crash
            if v > 0 and r.random() < p_brake: v -= 1            # random human braking
            if danfo and i == danfo[0] and danfo[1] <= t < danfo[1] + danfo[2]: v = 0
            new_v.append(v)
        vel = new_v
        pos = [(pos[i] + vel[i]) % L for i in range(n_cars)]
        hist.append((pos[:], vel[:]))
    return hist

def stats(hist, warm=200):
    vs = [v for _, vel in hist[warm:] for v in vel]
    return sum(vs) / len(vs), sum(1 for v in vs if v == 0) / len(vs)

out = {}
for cars in (40, 80, 120):
    h = simulate(cars); avg, stopped = stats(h)
    out[cars] = (avg, stopped); print(f"{cars} cars: avg speed {avg:.2f}/5, stopped {stopped*100:.1f}%")
h = simulate(120, p_brake=0.0); avg, stopped = stats(h)
print(f"120 perfect drivers (no random braking): avg {avg:.2f}/5, stopped {stopped*100:.1f}%")
h = simulate(40, p_brake=0.0, danfo=(0, 300, 20)); 
avg0, st0 = stats(simulate(40, p_brake=0.0), warm=300)
avgd, std = stats(h, warm=300)
print(f"40 perfect cars, one danfo stops 20 steps: stopped {std*100:.2f}% vs {st0*100:.2f}% without")
# how long until the jam caused by the danfo disappears (perfect drivers)
for t in range(300, 600):
    if all(v == 5 for v in h[t][1]): print("jam fully cleared at step", t, "(", t - 320, "steps after danfo left)"); break
else: print("jam never cleared")
