"""Dayo Tries #1 - the worst ways to sort numbers (the real code behind the video)."""
import random
import time

random.seed(7)


def bubble_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def is_sorted(a):
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def bogo_sort(a):
    """Shuffle until it happens to be sorted. Returns (sorted list, number of shuffles)."""
    a = a[:]
    shuffles = 0
    while not is_sorted(a):
        random.shuffle(a)
        shuffles += 1
    return a, shuffles


def delete_sort(a):
    """If a number is out of order... just delete it."""
    out = [a[0]]
    for x in a[1:]:
        if x >= out[-1]:
            out.append(x)
    return out


if __name__ == "__main__":
    numbers = [random.randint(1, 1_000_000) for _ in range(1_000_000)]

    t = time.perf_counter(); sorted(numbers)
    print(f"Python sort, 1,000,000 numbers: {time.perf_counter() - t:.2f}s")

    t = time.perf_counter(); bubble_sort(numbers[:10_000])
    print(f"Bubble sort, 10,000 numbers: {time.perf_counter() - t:.2f}s")

    sample = random.sample(range(100), 10)
    t = time.perf_counter(); _, k = bogo_sort(sample)
    print(f"Bogosort, 10 numbers: {k:,} shuffles in {time.perf_counter() - t:.2f}s")

    result = delete_sort(numbers)
    print(f"Delete sort, 1,000,000 numbers -> {len(result)} left: {result}")
