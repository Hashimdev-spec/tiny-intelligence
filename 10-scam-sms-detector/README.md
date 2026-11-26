# 10 · Building an AI that catches scam SMS

A **Naive Bayes** spam classifier written from scratch (no ML libraries), trained on 120 Nigerian-style
text messages I wrote myself: 60 scams ("your BVN has been suspended…") and 60 normal texts ("have you eaten?").

**How it works:** it counts how often each word appears in scam texts vs normal texts, then scores a new
message word by word (with Laplace smoothing so unseen words don't break it).

```bash
python scam_detector.py
```

**What I found**
- **89.1%** accuracy on messages it had never seen (average over 200 random train/test splits)
- Scammiest words it learned: *pay, claim, account, fee, link, click, receive, card, naira, now, details, pin*
- A genuine salary alert ("your account has been credited with 50,000 naira") → **100% scam** 😅
- A polite scammer ("Hello dear, hope your day is going well…") → **0.1% scam**, completely missed

It learned scam **words**, not scam **intent**, and scammers can always change their words.
