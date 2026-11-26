# 13 · Why bank apps crash on salary day

A **discrete-event simulation** of servers handling requests (~10 ms of work each), exploring
queueing theory and load balancing.

```bash
python salary_day.py
```

**Part 1: one server. Latency doesn't grow gently, it falls off a cliff**

| Server busy | Average response | Slowest 1% |
|---|---|---|
| 50% | 20 ms | 91 ms |
| 80% | 50 ms | 222 ms |
| 90% | 102 ms | 443 ms |
| 95% | 215 ms | 883 ms |
| 99% | **1,234 ms** | **4,190 ms** |

**Part 2: salary day.** Normal traffic is 60% of capacity, then everyone gets paid and traffic doubles.
The queue never recovers: 207 requests stuck after 10 s, 1,108 after 1 minute, and after 5 minutes a new user waits **56 seconds**
(that's your "network error").

**Part 3: 10 servers at 90% busy. The load-balancing strategy matters**

| Strategy | Average | Slowest 1% |
|---|---|---|
| Random | 101 ms | 470 ms |
| Round robin | 54 ms | 243 ms |
| Power of two choices | 30 ms | 106 ms |
| Least busy | **19 ms** | **77 ms** |

Same hardware, **5× faster**, just by routing smarter.
