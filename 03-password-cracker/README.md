# 03 · How fast can a laptop guess a password?

A brute-force speed test. ⚠️ It only cracks **made-up passwords that the script hashes itself**, completely offline. It's for learning why long passphrases matter.

```bash
python password_guess.py
```

My results: about 2.4 million guesses per second. A 4-digit PIN fell in 0.001s, 8 characters with symbols ≈ 7.5 years (much less with a gaming GPU), and 5 random words ≈ 368,000+ years.

**Takeaway:** use long passphrases, a password manager, and 2FA, and never your birthday.
