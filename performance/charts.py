
"""
Charts module for the Cryptographic Systems Simulator.

Displays a dark-themed comparison of cipher execution times.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button


BACKGROUND = "#0B1220"
PANEL = "#151F32"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
CYAN = "#22D3EE"

BAR_COLORS = [
    "#22D3EE",
    "#2878F0",
    "#A78BFA",
    "#22C55E",
]


def show_performance_chart(results):
    """
    Display a bar chart using benchmark results.

    Expected result format:
        [
            {
                "name": "Caesar Cipher",
                "size": 1000,
                "time_ms": 0.1,
                "repetitions": 100
            }
        ]
    """
    if not results:
        raise ValueError(
            "No benchmark results available. Run a benchmark first."
        )

    names = [item["name"] for item in results]
    times = [float(item["time_ms"]) for item in results]

    if any(value < 0 for value in times):
        raise ValueError("Execution times cannot be negative.")

    fig, ax = plt.subplots(figsize=(11, 6))

    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(PANEL)

    positions = list(range(len(names)))
    colors = [
        BAR_COLORS[index % len(BAR_COLORS)]
        for index in range(len(names))
    ]

    bars = ax.bar(
        positions,
        times,
        color=colors,
        width=0.58,
        edgecolor="#334155",
        linewidth=0.8
    )

    message_size = results[0].get("size", "Unknown")

    ax.set_title(
        "CLASSICAL CIPHER PERFORMANCE",
        fontsize=16,
        fontweight="bold",
        color=WHITE,
        pad=25
    )

    ax.text(
        0.5,
        1.02,
        f"Average encryption time | Message size: {message_size:,}"
        if isinstance(message_size, int)
        else f"Average encryption time | Message size: {message_size}",
        transform=ax.transAxes,
        ha="center",
        color=MUTED,
        fontsize=10
    )

    ax.set_xlabel(
        "Encryption Algorithm",
        fontsize=11,
        color=CYAN,
        labelpad=12
    )

    ax.set_ylabel(
        "Average Execution Time (milliseconds)",
        fontsize=11,
        color=CYAN,
        labelpad=12
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(
        names,
        rotation=12,
        ha="right",
        color=WHITE,
        fontsize=9
    )

    ax.tick_params(axis="y", colors=WHITE)

    ax.grid(
        axis="y",
        linestyle="--",
        color="#64748B",
        alpha=0.25
    )
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color("#2B3A52")

    largest_time = max(times, default=0)
    ax.set_ylim(
        0,
        largest_time * 1.25 if largest_time > 0 else 1
    )

    for bar, value in zip(bars, times):
        ax.annotate(
            f"{value:.6f} ms",
            xy=(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height()
            ),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            va="bottom",
            color=WHITE,
            fontsize=9,
            fontweight="bold"
        )

    fig.tight_layout(pad=2.5)

    # =====================================================
    # ADDED: BACK TO HOME BUTTON
    # =====================================================

    button_ax = fig.add_axes([0.80, 0.025, 0.17, 0.065])

    back_button = Button(
        button_ax,
        "← Back",
        color="#087F5B",
        hovercolor="#059669"
    )

    back_button.label.set_color("white")
    back_button.label.set_fontsize(10)
    back_button.label.set_fontweight("bold")

    def go_back(event):
        plt.close(fig)

    back_button.on_clicked(go_back)

    # =====================================================

    plt.show()


if __name__ == "__main__":
    # Example data to test the chart independently.
    sample_results = [
        {
            "name": "Caesar Cipher",
            "size": 1000,
            "time_ms": 0.12,
            "repetitions": 100,
        },
        {
            "name": "Playfair Cipher",
            "size": 1000,
            "time_ms": 1.25,
            "repetitions": 100,
        },
        {
            "name": "Vigenere Cipher",
            "size": 1000,
            "time_ms": 0.55,
            "repetitions": 100,
        },
        {
            "name": "Rail Fence Cipher",
            "size": 1000,
            "time_ms": 0.18,
            "repetitions": 100,
        },
    ]

    show_performance_chart(sample_results)
