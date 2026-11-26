"""Dayo Tries #10: I built an AI that catches scam SMS.

A Naive Bayes classifier written from scratch (no ML libraries).
It learns how often each word shows up in scam texts vs normal texts,
then scores new messages word by word.
"""
import math, os, random, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def load(path=os.path.join(HERE, "messages.txt")):
    rows = []
    for line in open(path, encoding="utf-8"):
        if line.strip():
            label, text = line.rstrip("\n").split("\t", 1)
            rows.append((label, text))
    return rows


class NaiveBayes:
    def fit(self, rows):
        self.counts = {"scam": Counter(), "normal": Counter()}
        self.docs = Counter(label for label, _ in rows)
        for label, text in rows:
            self.counts[label].update(words(text))
        self.vocab = set(self.counts["scam"]) | set(self.counts["normal"])
        self.totals = {k: sum(c.values()) for k, c in self.counts.items()}
        return self

    def word_logp(self, word, label):                      # Laplace smoothing: unseen words don't break it
        return math.log((self.counts[label][word] + 1) / (self.totals[label] + len(self.vocab)))

    def scam_probability(self, text):
        score = {}
        for label in ("scam", "normal"):
            score[label] = math.log(self.docs[label] / sum(self.docs.values()))
            score[label] += sum(self.word_logp(w, label) for w in words(text) if w in self.vocab)
        diff = score["normal"] - score["scam"]
        return 1 / (1 + math.exp(min(50, diff)))

    def scammiest_words(self, n=10, min_count=3):
        cand = [w for w in self.vocab if self.counts["scam"][w] + self.counts["normal"][w] >= min_count]
        return sorted(cand, key=lambda w: self.word_logp(w, "scam") - self.word_logp(w, "normal"), reverse=True)[:n]


if __name__ == "__main__":
    rows = load()
    print(f"Dataset: {len(rows)} messages ({sum(1 for r in rows if r[0] == 'scam')} scam, "
          f"{sum(1 for r in rows if r[0] == 'normal')} normal), written by me")

    # honest test: train on 75%, test on the 25% it has never seen, repeated over 200 random splits
    accs = []
    for seed in range(200):
        r = rows[:]; random.Random(seed).shuffle(r)
        cut = int(len(r) * 0.75)
        nb = NaiveBayes().fit(r[:cut])
        test = r[cut:]
        accs.append(sum((nb.scam_probability(t) > 0.5) == (lab == "scam") for lab, t in test) / len(test))
    print(f"Accuracy on unseen messages: {sum(accs) / len(accs):.1%} (average of 200 train/test splits)")

    nb = NaiveBayes().fit(rows)
    print("Scammiest words it learned:", ", ".join(nb.scammiest_words(12)))

    tests = [
        "Congratulations! You have won 1 million naira. Click the link to claim",
        "Mum: please send me 5,000 urgently, I will explain later",
        "Congratulations on your graduation my son, we are so proud",
        "Your account has been credited with 50,000 naira salary",
        "Hello dear, hope your day is going well. Reply when you are free so we can talk",
        "Hi, it's me. I changed my number. Please save this one",
    ]
    print("\nNew messages it has never seen:")
    for t in tests:
        p = nb.scam_probability(t)
        print(f"  {p:6.1%} scam  {'SCAM ' if p > 0.5 else 'SAFE '}  {t}")
