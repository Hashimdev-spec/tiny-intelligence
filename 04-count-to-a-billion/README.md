# 04 · Counting to a billion

Adding up 1 → 1,000,000,000 with a Python loop, `sum()`, NumPy, C, and Gauss's formula `n(n+1)/2`.

```bash
python count_billion.py

gcc -O0 count_billion.c -o slow && ./slow
gcc -O2 count_billion.c -o fast && ./fast   # the compiler skips the loop 👀
```

My results: Python loop 63.2s, `sum()` 11.8s, NumPy 2.9s, C 1.94s, C with -O2 0.0000s, formula: instant.
