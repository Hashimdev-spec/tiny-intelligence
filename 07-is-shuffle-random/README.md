# 07 · Is your shuffle really random?

A 100-song playlist (10 artists × 10 songs) shuffled 100,000 times, plus a "less random" shuffle that spreads artists out (similar to what Spotify described in 2014).

```bash
python shuffle_test.py
```

My results: 99.99% of truly random shuffles put the same artist back-to-back, and 49% had 3 in a row. The spread-out shuffle got that down to 0.8%.
