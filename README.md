<div align="center">

# 🧠 Tiny Intelligence

**Tiny experiments. Real intelligence. Surprising results.**

Neural networks, learning agents, simulations and algorithms, built from first principles,
run for real, and explained in under 60 seconds.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-arrays-013243?logo=numpy&logoColor=white)
![C](https://img.shields.io/badge/C-performance-A8B9CC?logo=c&logoColor=black)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

</div>

---

## Why this exists

Most "AI content" is someone typing into a chatbot. This repo is the opposite: every experiment here
**builds the intelligence itself**, trains or simulates it, measures it honestly, and then tries to break it.

Each experiment is a short video in the **Dayo Tries** series. Every number shown on screen comes from running the code in this repo.

## 🔬 The experiments

| # | Experiment | What it shows | Key result |
|---|-----------|---------------|------------|
| 13 | [**Why bank apps crash on salary day**](13-salary-day-servers) | System design: queueing theory, load balancing, tail latency | 99% busy = **60× slower**; smart load balancing = **5× faster** on the same servers |
| 12 | [**Evolving danfo drivers with natural selection**](12-danfo-evolution) | Genetic algorithms, neuroevolution, emergent behaviour | 51 m → **284 m** per trip; they evolved to drive slow **99.8%** of the time |
| 11 | [**An AI that reads your rock-paper-scissors habits**](11-rock-paper-scissors-ai) | Markov models, sequence prediction, why randomness is unbeatable | Beat human-like players **57% vs 20%**, stuck at **33%** against pure randomness |
| 10 | [**Building an AI that catches scam SMS**](10-scam-sms-detector) | Naive Bayes from scratch, text classification, false positives vs. false negatives | **89%** accurate… but flagged a real salary alert as **100% scam** |
| 09 | [**Teaching an AI to cross a Lagos road**](09-lagos-road-ai) | Reinforcement learning (Q-learning), reward design, reward hacking | Hit rate **86% → 3%**… then it learned to **never cross at all** |
| 02 | [**Teaching a neural network to read handwriting**](02-handwriting-ai) | Neural networks, train/test split, dataset bias | 96.7% accuracy… but it read a Nigerian-style "1" as a **2** |
| 08 | [**Training a language model on Nigerian Pidgin**](08-pidgin-ai) | N-gram language models, overfitting vs. underfitting | Small data either talks nonsense or **copies 48%** of its training set |
| 06 | [**Simulating phantom traffic jams**](06-phantom-traffic-jam) | Agent-based simulation (Nagel–Schreckenberg) | Removing random braking cut stopped cars from **30.6% → 1.2%** |
| 03 | [**How fast can a laptop guess a password?**](03-password-cracker) | Brute-force search, hashing, security engineering | 4-digit PIN: **0.001 s** · 5-word passphrase: **368,000+ years** |
| 07 | [**Is shuffle actually random?**](07-is-shuffle-random) | Probability, Monte Carlo (100,000 trials), UX vs. true randomness | **99.99%** of truly random shuffles cluster an artist |
| 05 | [**Optimal naira change**](05-naira-change) | Greedy vs. dynamic programming, proof by exhaustive check | Greedy was optimal for all **20,000** amounts |
| 04 | [**Counting to a billion**](04-count-to-a-billion) | Interpreted vs. compiled code, compiler optimisation, math | Python **63 s** → C **1.9 s** → `gcc -O2` **0 s** |
| 01 | [**The worst way to sort numbers**](01-worst-way-to-sort) | Algorithmic complexity: O(n log n) vs. O(n²) vs. O(n·n!) | Bubble sort ≈ **7.5 h** for 1M items; bogosort ≈ **100,000+ years** for 20 |

## ⚡ Quick start

```bash
git clone https://github.com/Hashimdev-spec/tiny-intelligence.git
cd tiny-intelligence
pip install -r requirements.txt

cd 02-handwriting-ai && python digits_ai.py
```

Every folder is self-contained, with its own README explaining the experiment, how to run it and what I found.
Timings will differ on your machine, and that's part of the fun.

## 🛠️ Skills on display

- **Machine learning:** neural networks, language models, reinforcement learning, overfitting and dataset bias
- **Simulation and modelling:** agent-based systems, Monte Carlo experiments, genetic algorithms
- **Algorithms and complexity:** greedy vs. dynamic programming, sorting, brute-force search
- **System design:** queueing theory, load balancing, tail latency (p99)
- **Performance engineering:** Python vs. NumPy vs. C, compiler optimisation
- **Security fundamentals:** hashing, password entropy, why passphrases win
- **Communicating technical ideas:** every experiment is explained for a general audience in under a minute

## 👋 About me

I'm **Hasheem**, a software engineer from Kano, Nigeria, building mobile and web products with
**Flutter, Next.js/React and Firebase**, and exploring AI one experiment at a time.

📺 Watch the experiments: **@dayodeploys** on TikTok, YouTube and Instagram
💼 Open to collaborations and opportunities · [Connect on LinkedIn](https://www.linkedin.com/in/hashim-aliyu-hashim-71b29529b/)

## 💡 Suggest an experiment

Got an idea Dayo should try? Comment on any video or open an issue. If it can be built and measured, it's fair game.

<sub>MIT licensed · Built with curiosity, Python, and a generator. ⚡</sub>
