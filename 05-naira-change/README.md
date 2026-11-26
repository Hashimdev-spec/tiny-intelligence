# 05 · The best way to give naira change

Greedy (biggest note first) vs dynamic programming (guaranteed fewest notes), checked on every amount from ₦5 to ₦100,000.

```bash
python naira_change.py
```

My results: greedy was optimal for all 20,000 amounts, so naira notes are well designed. With imaginary ₦1/₦3/₦4 coins, greedy fails (₦6 → 4+1+1 instead of 3+3). There are 104,561 ways to make ₦1,000.
