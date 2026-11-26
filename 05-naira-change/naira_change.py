"""Dayo Tries #5 - the best way to give naira change (greedy vs dynamic programming)."""
import time
NAIRA = [1000, 500, 200, 100, 50, 20, 10, 5]          # notes in circulation

def greedy(amount, notes):
    out = []
    for n in sorted(notes, reverse=True):
        while amount >= n:
            amount -= n; out.append(n)
    return out if amount == 0 else None

def best(amount, notes):
    """dynamic programming: true minimum number of notes"""
    INF = float("inf"); dp = [0] + [INF] * amount; pick = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for n in notes:
            if n <= a and dp[a - n] + 1 < dp[a]:
                dp[a] = dp[a - n] + 1; pick[a] = n
    if dp[amount] == INF: return None
    out = []
    while amount: out.append(pick[amount]); amount -= pick[amount]
    return sorted(out, reverse=True)

def ways(amount, notes):
    w = [1] + [0] * amount
    for n in notes:
        for a in range(n, amount + 1): w[a] += w[a - n]
    return w[amount]

amt = 4750
print("greedy", amt, greedy(amt, NAIRA)); print("best  ", amt, best(amt, NAIRA))
# is greedy always optimal for naira? check every amount (multiples of 5) up to 100,000
def min_table(limit, notes):
    INF = float("inf"); dp = [0] + [INF] * limit
    for a in range(1, limit + 1):
        for n in notes:
            if n <= a and dp[a - n] + 1 < dp[a]: dp[a] = dp[a - n] + 1
    return dp
T = min_table(100_000, NAIRA)
bad = [a for a in range(5, 100_001, 5) if len(greedy(a, NAIRA)) != T[a]]
print("amounts where greedy loses (naira, up to 100k):", len(bad))
print("ways to make 1000:", f"{ways(1000, NAIRA):,}")
# a silly made-up currency where greedy fails
DAYO = [1, 3, 4]
print("dayo coins 6 greedy", greedy(6, DAYO), "best", best(6, DAYO))
