"""Dayo Tries #8 - I trained a tiny AI (a word-level Markov model) on Nigerian pidgin."""
import random, time, re, os
from collections import defaultdict, Counter
lines = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus.txt")) if l.strip()]
words = [w for l in lines for w in l.split()]
print(f"corpus: {len(lines)} sentences, {len(words)} words, {len(set(words))} unique words")

def train(order):
    model = defaultdict(Counter)
    for l in lines:
        toks = ["<s>"] * order + l.split() + ["</s>"]
        for i in range(order, len(toks)):
            model[tuple(toks[i - order:i])][toks[i]] += 1
    return model

def generate(model, order, rng, max_words=16):
    ctx = ["<s>"] * order; out = []
    while len(out) < max_words:
        c = model[tuple(ctx[-order:])]
        if not c: break
        w = rng.choices(list(c), weights=list(c.values()))[0]
        if w == "</s>": break
        out.append(w); ctx.append(w)
    return " ".join(out)

t = time.perf_counter(); m1 = train(1); m2 = train(2); dt = time.perf_counter() - t
print(f"trained in {dt*1000:.1f} ms")
for order, m in ((1, m1), (2, m2)):
    rng = random.Random(order * 7)
    print(f"\n--- order {order} ---")
    for k in range(25):
        s = generate(m, order, rng)
        tag = "(copied)" if s in lines else "(NEW)"
        print(f"{k:2d} {tag} {s}")
