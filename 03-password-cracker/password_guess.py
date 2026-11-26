"""Dayo Tries #3 - how long would my laptop take to guess a password? (dummy passwords, offline)"""
import hashlib, itertools, string, time

def h(s): return hashlib.sha256(s.encode()).hexdigest()

def crack(target_hash, alphabet, length):
    tries = 0
    for combo in itertools.product(alphabet, repeat=length):
        tries += 1
        if h("".join(combo)) == target_hash:
            return "".join(combo), tries
    return None, tries

# measure speed
t = time.perf_counter(); n = 0
for combo in itertools.product(string.ascii_lowercase, repeat=4):
    h("".join(combo)); n += 1
rate = n / (time.perf_counter() - t)
print(f"speed: {rate:,.0f} guesses/second")

for pw, alpha in [("2580", string.digits), ("zzzz", string.ascii_lowercase)]:
    t = time.perf_counter(); found, k = crack(h(pw), alpha, len(pw))
    print(f"cracked {pw!r} in {k:,} guesses, {time.perf_counter()-t:.3f}s")

def est(space):
    s = space / rate
    for unit, sec in [("years", 31_557_600), ("days", 86_400), ("hours", 3_600), ("minutes", 60)]:
        if s >= sec: return f"{s/sec:,.1f} {unit}"
    return f"{s:.2f} seconds"

full = string.ascii_letters + string.digits + "!@#$%^&*"
cases = {
    "4-digit PIN": 10**4,
    "6 lowercase letters": 26**6,
    "8 chars: letters+numbers+symbols": len(full)**8,
    "12 chars: letters+numbers+symbols": len(full)**12,
    "4 random words (from 7,776)": 7776**4,
    "5 random words (from 7,776)": 7776**5,
}
for k, v in cases.items():
    print(f"{k}: {v:,} combos -> {est(v)}")
