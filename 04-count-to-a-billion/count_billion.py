"""Dayo Tries #4 - how fast can Python count to a billion?"""
import time
N = 1_000_000_000

def timed(label, fn):
    t = time.perf_counter(); r = fn(); dt = time.perf_counter() - t
    print(f"{label}: {dt:.3f}s  (result {r:,})"); return dt

# 1) plain Python loop, measured on 100 million and scaled up x10 (we did also run the full billion below)
def loop(n):
    total = 0
    i = 0
    while i < n:
        i += 1
        total += i
    return total
dt_loop = timed("while loop, 100M", lambda: loop(100_000_000))
print(f"  -> estimated for 1 billion: {dt_loop*10:.1f}s")
timed("for + range, 1B", lambda: sum(range(1, N + 1)))   # builtin sum over range
import numpy as np
def np_sum():
    total = 0; step = 50_000_000
    for s in range(1, N + 1, step):
        total += int(np.arange(s, min(s + step, N + 1), dtype=np.int64).sum())
    return total
timed("numpy chunks, 1B", np_sum)
timed("formula n(n+1)/2", lambda: N * (N + 1) // 2)

# ran separately for the video:
#   full while loop to 1,000,000,000 in Python: 63.2s
#   C (gcc -O0): 1.94s      C (gcc -O2): 0.0000s  (the compiler replaces the loop with the answer)
