"""Dayo Tries #7 - is your phone's shuffle really random?"""
import random
from collections import Counter
random.seed(11)
ARTISTS = ["Burna", "Wiz", "Davido", "Tems", "Asake", "Rema", "Ayra", "Olamide", "Fireboy", "Ckay"]
playlist = [(a, i) for a in ARTISTS for i in range(10)]        # 100 songs, 10 artists x 10 songs
TRIALS = 100_000

def back_to_back(order):
    return sum(1 for x, y in zip(order, order[1:]) if x[0] == y[0])

counts = []
three_in_row = 0
for _ in range(TRIALS):
    o = playlist[:]; random.shuffle(o)
    counts.append(back_to_back(o))
    if any(o[i][0] == o[i+1][0] == o[i+2][0] for i in range(98)): three_in_row += 1
has_any = sum(1 for c in counts if c > 0) / TRIALS
print(f"truly random shuffles with at least one same-artist back-to-back: {has_any*100:.2f}%")
print(f"average back-to-backs per shuffle: {sum(counts)/TRIALS:.2f}")
print(f"shuffles with 3 in a row from the same artist: {three_in_row/TRIALS*100:.1f}%")

def spread_shuffle(pl):
    """'less random' shuffle: spread each artist's songs evenly, with a little jitter"""
    by = {}
    for s in pl: by.setdefault(s[0], []).append(s)
    placed = []
    for a, songs in by.items():
        random.shuffle(songs); n = len(songs); off = random.random() / n
        for k, s in enumerate(songs):
            placed.append((off + k / n + random.uniform(-0.3, 0.3) / n, s))
    return [s for _, s in sorted(placed)]
c2 = [back_to_back(spread_shuffle(playlist)) for _ in range(20_000)]
print(f"'less random' shuffle - average back-to-backs: {sum(c2)/len(c2):.2f}, any at all: {sum(1 for c in c2 if c)/len(c2)*100:.1f}%")
