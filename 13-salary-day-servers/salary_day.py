"""Dayo Tries #13: Why bank apps crash on salary day.

A discrete-event simulation of a server handling requests.
Each request takes ~10 ms of work on average (one server = ~100 requests/second).
Part 1: one server at different loads -> how long do users wait?
Part 2: salary day: traffic doubles.
Part 3: 10 servers behind a load balancer: which balancing strategy wins?
"""
import heapq, random
import numpy as np

SERVICE_MS = 10.0                      # average work per request


def one_server(load, n=200_000, seed=0):
    """load = fraction of the server's capacity being used (0.5 = 50% busy)"""
    rng = random.Random(seed)
    t, free_at, times = 0.0, 0.0, []
    for _ in range(n):
        t += rng.expovariate(load / SERVICE_MS)          # next user arrives
        start = max(t, free_at)                           # wait if the server is busy
        free_at = start + rng.expovariate(1 / SERVICE_MS)
        times.append(free_at - t)                         # what the user feels: wait + work
    a = np.array(times[n // 10:])                         # skip warm-up
    return a.mean(), np.percentile(a, 99)


def salary_day(normal_load=0.6, surge=2.0, seconds=300, seed=1):
    """traffic jumps from normal_load to normal_load*surge. How many requests are stuck in the queue?"""
    rng = random.Random(seed)
    t, free_at, waiting, out = 0.0, 0.0, [], []
    load = normal_load * surge
    next_report = 1000.0
    while t < seconds * 1000:
        t += rng.expovariate(load / SERVICE_MS)
        start = max(t, free_at)
        free_at = start + rng.expovariate(1 / SERVICE_MS)
        heapq.heappush(waiting, start)
        while waiting and waiting[0] <= t:
            heapq.heappop(waiting)
        if t >= next_report:
            out.append((next_report / 1000, len(waiting), (free_at - t) / 1000))
            next_report += 1000
    return out


def balanced(strategy, servers=10, load=0.9, n=300_000, seed=2):
    """servers behind a load balancer. strategy: random | round_robin | least_busy | two_choices"""
    rng = random.Random(seed)
    free_at = [0.0] * servers
    queue_len = [[] for _ in range(servers)]               # finish times of jobs on each server
    t, rr, times = 0.0, 0, []
    for _ in range(n):
        t += rng.expovariate(load * servers / SERVICE_MS)
        for q in queue_len:
            while q and q[0] <= t:
                heapq.heappop(q)
        if strategy == "random":
            s = rng.randrange(servers)
        elif strategy == "round_robin":
            s = rr; rr = (rr + 1) % servers
        elif strategy == "least_busy":
            s = min(range(servers), key=lambda i: len(queue_len[i]))
        else:                                                # two_choices: pick 2 at random, use the less busy one
            a, b = rng.sample(range(servers), 2)
            s = a if len(queue_len[a]) <= len(queue_len[b]) else b
        start = max(t, free_at[s])
        free_at[s] = start + rng.expovariate(1 / SERVICE_MS)
        heapq.heappush(queue_len[s], free_at[s])
        times.append(free_at[s] - t)
    a = np.array(times[n // 10:])
    return a.mean(), np.percentile(a, 99)


if __name__ == "__main__":
    print("PART 1: one server, ~10 ms of work per request")
    for load in (0.5, 0.8, 0.9, 0.95, 0.99):
        avg, p99 = one_server(load)
        print(f"  {load:4.0%} busy -> average response {avg:7.0f} ms | slowest 1% wait {p99:7.0f} ms")

    print("\nPART 2: salary day (normal 60% busy, then traffic doubles to 120%)")
    for sec, q, wait in salary_day():
        if sec in (1, 10, 30, 60, 120, 300):
            print(f"  after {sec:3.0f} s: {q:6d} requests stuck in the queue | a new user waits {wait:6.1f} s")

    print("\nPART 3: 10 servers at 90% busy behind a load balancer")
    for strat in ("random", "round_robin", "least_busy", "two_choices"):
        avg, p99 = balanced(strat)
        print(f"  {strat:12s} -> average {avg:6.0f} ms | slowest 1% {p99:6.0f} ms")
