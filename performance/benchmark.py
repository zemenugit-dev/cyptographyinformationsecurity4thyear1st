
"""
Benchmark module for the Cryptographic Systems Simulator.

Measures average encryption execution time for classical ciphers.
"""

import time

from ciphers import caesar
from ciphers import playfair
from ciphers import vigenere
from ciphers import rail_fence


def run_benchmark(message_size=1000, repetitions=None):
    """
    Benchmark classical cipher encryption.

    Args:
        message_size: Number of characters in the test message.
        repetitions: Number of timed runs per algorithm.
                     If None, choose automatically.

    Returns:
        A list of dictionaries containing benchmark results.
    """
    try:
        message_size = int(message_size)
    except (TypeError, ValueError):
        raise ValueError("Message size must be a whole number.")

    if message_size <= 0:
        raise ValueError("Message size must be greater than zero.")

    if repetitions is None:
        repetitions = max(1, min(100, 100000 // message_size))

    try:
        repetitions = int(repetitions)
    except (TypeError, ValueError):
        raise ValueError("Repetitions must be a whole number.")

    if repetitions <= 0:
        raise ValueError("Repetitions must be greater than zero.")

    pattern = "CryptographyTest123 "
    message = (pattern * ((message_size // len(pattern)) + 1))[
        :message_size
    ]

    # Playfair is tested with alphabetic characters only.
    playfair_message = "".join(
        char for char in message
        if char.isascii() and char.isalpha()
    )

    if not playfair_message:
        raise ValueError("Playfair requires alphabetic input.")

    algorithms = [
        ("Caesar Cipher", lambda: caesar.encrypt(message, 3)),
        (
            "Playfair Cipher",
            lambda: playfair.encrypt(playfair_message, "MONARCHY")
        ),
        ("Vigenere Cipher", lambda: vigenere.encrypt(message, "LEMON")),
        ("Rail Fence Cipher", lambda: rail_fence.encrypt(message, 3)),
    ]

    results = []

    for name, operation in algorithms:
        # Warm-up call is not included in the measurement.
        operation()

        start_time = time.perf_counter()

        for _ in range(repetitions):
            operation()

        elapsed_seconds = time.perf_counter() - start_time
        average_ms = (elapsed_seconds / repetitions) * 1000

        results.append({
            "name": name,
            "size": message_size,
            "time_ms": average_ms,
            "repetitions": repetitions,
        })

    return results


def print_results(results):
    """Print benchmark results in a readable terminal table."""

    print("\n" + "=" * 76)
    print("CRYPTOGRAPHIC SYSTEMS SIMULATOR - BENCHMARK RESULTS")
    print("=" * 76)

    print(
        f"{'Algorithm':<24}"
        f"{'Message Size':>15}"
        f"{'Average Time (ms)':>22}"
        f"{'Runs':>10}"
    )

    print("-" * 76)

    for result in results:
        print(
            f"{result['name']:<24}"
            f"{result['size']:>15,}"
            f"{result['time_ms']:>22.6f}"
            f"{result['repetitions']:>10}"
        )

    print("=" * 76)


if __name__ == "__main__":
    benchmark_results = run_benchmark(message_size=1000)
    print_results(benchmark_results)
