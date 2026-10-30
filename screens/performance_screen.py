
import tkinter as tk
from tkinter import ttk, messagebox
import time

from ciphers import caesar, playfair, vigenere, rail_fence


# ============================================================
# COLOR THEME
# ============================================================

BG = "#0B1220"
PANEL = "#151F32"
PANEL_LIGHT = "#1D2B42"
NAVY = "#123B5D"
BLUE = "#2878F0"
CYAN = "#22D3EE"
GREEN = "#22C55E"
ORANGE = "#F59E0B"
PURPLE = "#A78BFA"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
BORDER = "#2B3A52"


class PerformanceScreen(tk.Frame):
    """Modern benchmark dashboard for classical cipher algorithms."""

    def __init__(self, parent, show_home=None):
        super().__init__(parent, bg=BG)

        self.show_home = show_home
        self.results = []

        self.setup_styles()
        self.create_widgets()

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):
        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "Treeview.Heading",
            background="#223550",
            foreground=CYAN,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=(10, 12)
        )

        self.style.map(
            "Treeview",
            background=[("selected", "#245A86")],
            foreground=[("selected", WHITE)]
        )

        self.style.map(
            "Treeview.Heading",
            background=[("active", "#2B4566")]
        )

        self.style.configure(
            "Dark.TCombobox",
            fieldbackground=PANEL_LIGHT,
            background=PANEL_LIGHT,
            foreground=WHITE,
            arrowcolor=CYAN,
            padding=8
        )

        self.style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", PANEL_LIGHT)],
            foreground=[("readonly", WHITE)],
            selectbackground=[("readonly", PANEL_LIGHT)],
            selectforeground=[("readonly", WHITE)]
        )

        self.style.configure(
            "Vertical.TScrollbar",
            background=PANEL_LIGHT,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=CYAN
        )

    # ========================================================
    # REUSABLE GUI COMPONENTS
    # ========================================================

    def make_button(self, parent, text, command, color=BLUE,
                    fg=WHITE, width=None):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground="#3B82F6",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=10,
            width=width
        )

        button.bind(
            "<Enter>",
            lambda event: button.config(bg="#334B6D")
        )
        button.bind(
            "<Leave>",
            lambda event: button.config(bg=color)
        )

        return button

    def create_metric_card(self, parent, title, initial_value,
                           accent, column):
        card = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
            pady=4
        )

        tk.Frame(
            card,
            bg=accent,
            height=4
        ).pack(fill="x")

        inner = tk.Frame(card, bg=PANEL, padx=12, pady=10)
        inner.pack(fill="both", expand=True)

        tk.Label(
            inner,
            text=title.upper(),
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        value_label = tk.Label(
            inner,
            text=initial_value,
            bg=PANEL,
            fg=accent,
            font=("Segoe UI", 19, "bold")
        )
        value_label.pack(anchor="w", pady=(7, 0))

        return value_label

    # ========================================================
    # MAIN GUI
    # ========================================================

    def create_widgets(self):

        # Header
        header = tk.Frame(self, bg="#101C30")
        header.pack(fill="x")

        header_inner = tk.Frame(
            header,
            bg="#101C30",
            padx=28,
            pady=17
        )
        header_inner.pack(fill="x")

        title_area = tk.Frame(header_inner, bg="#101C30")
        title_area.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_area,
            text="CRYPTOLAB  /  PERFORMANCE",
            bg="#101C30",
            fg=CYAN,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Performance Analysis",
            bg="#101C30",
            fg=WHITE,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", pady=(3, 2))

        tk.Label(
            title_area,
            text="Benchmark and compare classical encryption algorithms",
            bg="#101C30",
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Label(
            header_inner,
            text="● SYSTEM READY",
            bg="#16352F",
            fg=GREEN,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        ).pack(side="right", anchor="center", padx=(10, 0))

        # Main content
        content = tk.Frame(self, bg=BG, padx=22, pady=14)
        content.pack(fill="both", expand=True)

        # Dashboard heading
        intro = tk.Frame(content, bg=BG)
        intro.pack(fill="x", pady=(0, 8))

        tk.Label(
            intro,
            text="Benchmark Dashboard",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Label(
            intro,
            text="MEASURE  •  COMPARE  •  ANALYZE",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(side="right", pady=5)

        # Metric cards
        metrics = tk.Frame(content, bg=BG)
        metrics.pack(fill="x", pady=(0, 12))

        for column in range(4):
            metrics.grid_columnconfigure(column, weight=1, uniform="metric")

        self.algorithms_value = self.create_metric_card(
            metrics, "Algorithms tested", "0", CYAN, 0
        )

        self.message_value = self.create_metric_card(
            metrics, "Message size", "—", BLUE, 1
        )

        self.fastest_value = self.create_metric_card(
            metrics, "Fastest cipher", "—", GREEN, 2
        )

        self.average_value = self.create_metric_card(
            metrics, "Average time", "—", PURPLE, 3
        )

        # Benchmark settings panel
        settings = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        settings.pack(fill="x", pady=(0, 12))

        settings_header = tk.Frame(settings, bg=PANEL, padx=15, pady=10)
        settings_header.pack(fill="x")

        tk.Label(
            settings_header,
            text="⚙  BENCHMARK CONFIGURATION",
            bg=PANEL,
            fg=CYAN,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        controls = tk.Frame(settings, bg=PANEL, padx=15, pady=12)
        controls.pack(fill="x")

        tk.Label(
            controls,
            text="Test message size",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(0, 10))

        self.message_size = tk.StringVar(value="1000")

        self.size_box = ttk.Combobox(
            controls,
            textvariable=self.message_size,
            values=["100", "1000", "5000", "10000"],
            state="readonly",
            width=12,
            style="Dark.TCombobox"
        )
        self.size_box.pack(side="left", padx=(0, 18))

        self.make_button(
            controls,
            "▶  Run Benchmark",
            self.run_benchmark,
            color=BLUE
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            controls,
            "▥  View Chart",
            self.show_chart,
            color="#0E7490"
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            controls,
            text="Average execution time in milliseconds",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="right", padx=(8, 0))

        # Results heading
        results_heading = tk.Frame(content, bg=BG)
        results_heading.pack(fill="x", pady=(0, 8))

        tk.Label(
            results_heading,
            text="Benchmark Results",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        self.result_count = tk.Label(
            results_heading,
            text="0 RESULTS",
            bg=BG,
            fg=CYAN,
            font=("Segoe UI", 9, "bold")
        )
        self.result_count.pack(side="right")

        # Table panel
        table_panel = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_panel.pack(fill="both", expand=True)

        table_frame = tk.Frame(table_panel, bg=PANEL)
        table_frame.pack(fill="both", expand=True, padx=1, pady=1)

        columns = ("algorithm", "size", "time", "status")

        self.results_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5
        )

        self.results_table.heading("algorithm", text="ENCRYPTION ALGORITHM")
        self.results_table.heading("size", text="MESSAGE SIZE")
        self.results_table.heading("time", text="AVERAGE TIME (MS)")
        self.results_table.heading("status", text="STATUS")

        self.results_table.column(
            "algorithm", width=240, minwidth=170, anchor="w"
        )
        self.results_table.column(
            "size", width=140, minwidth=100, anchor="center"
        )
        self.results_table.column(
            "time", width=190, minwidth=140, anchor="center"
        )
        self.results_table.column(
            "status", width=140, minwidth=100, anchor="center"
        )

        self.results_table.tag_configure(
            "even", background=PANEL, foreground=WHITE
        )
        self.results_table.tag_configure(
            "odd", background=PANEL_LIGHT, foreground=WHITE
        )
        self.results_table.tag_configure(
            "completed", foreground=GREEN
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.results_table.yview,
            style="Vertical.TScrollbar"
        )

        self.results_table.configure(yscrollcommand=scrollbar.set)

        self.results_table.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        # Footer actions
        footer = tk.Frame(content, bg=BG)
        footer.pack(fill="x", pady=(10, 0))

        self.status_label = tk.Label(
            footer,
            text="● Ready. Run a benchmark to begin.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)

        self.make_button(
            footer,
            "Clear Results",
            self.clear_results,
            color="#374151"
        ).pack(side="right", padx=(8, 0))

        if self.show_home is not None:
            self.make_button(
                footer,
                "← Back to Home",
                self.show_home,
                color=NAVY
            ).pack(side="right")

    # ========================================================
    # BENCHMARK LOGIC
    # ========================================================

    def run_benchmark(self):
        try:
            size = int(self.message_size.get())

            if size <= 0:
                raise ValueError(
                    "Message size must be greater than zero."
                )

            # Generate a repeatable test message of the requested size.
            pattern = "CryptographyTest123 "
            message = (pattern * ((size // len(pattern)) + 1))[:size]

            # Playfair operates on alphabetic characters.
            playfair_message = "".join(
                char for char in message
                if char.isascii() and char.isalpha()
            )

            if not playfair_message:
                raise ValueError(
                    "The generated message has no letters for Playfair."
                )

            algorithms = [
                (
                    "Caesar Cipher",
                    lambda: caesar.encrypt(message, 3)
                ),
                (
                    "Playfair Cipher",
                    lambda: playfair.encrypt(
                        playfair_message, "MONARCHY"
                    )
                ),
                (
                    "Vigenere Cipher",
                    lambda: vigenere.encrypt(message, "LEMON")
                ),
                (
                    "Rail Fence Cipher",
                    lambda: rail_fence.encrypt(message, 3)
                )
            ]

            # Use fewer repetitions for larger messages.
            repetitions = max(1, min(100, 100000 // size))
            new_results = []

            self.status_label.config(
                text="● Running benchmark...",
                fg=ORANGE
            )
            self.update_idletasks()

            for name, operation in algorithms:
                # Warm up once before measuring.
                operation()

                start = time.perf_counter()

                for _ in range(repetitions):
                    operation()

                elapsed = time.perf_counter() - start
                average_ms = (elapsed / repetitions) * 1000

                new_results.append({
                    "name": name,
                    "size": size,
                    "time_ms": average_ms
                })

            self.results = new_results
            self.update_results_table()
            self.update_metric_cards(size)

            self.status_label.config(
                text=f"● Benchmark completed successfully for "
                     f"{size:,} characters.",
                fg=GREEN
            )

        except (ValueError, TypeError) as error:
            self.status_label.config(
                text="● Benchmark could not be completed.",
                fg=ORANGE
            )
            messagebox.showerror("Benchmark Error", str(error))

        except Exception as error:
            self.status_label.config(
                text="● An error occurred during benchmarking.",
                fg=ORANGE
            )
            messagebox.showerror(
                "Benchmark Error",
                f"Could not complete the benchmark:\n{error}"
            )

    # ========================================================
    # UPDATE TABLE AND METRIC CARDS
    # ========================================================

    def update_results_table(self):
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        for index, result in enumerate(self.results):
            row_tag = "even" if index % 2 == 0 else "odd"

            self.results_table.insert(
                "",
                "end",
                values=(
                    result["name"],
                    f'{result["size"]:,} characters',
                    f'{result["time_ms"]:.6f}',
                    "Completed"
                ),
                tags=(row_tag,)
            )

        self.result_count.config(
            text=f"{len(self.results)} RESULTS"
        )

    def update_metric_cards(self, size):
        if not self.results:
            return

        fastest = min(self.results, key=lambda result: result["time_ms"])
        average = sum(
            result["time_ms"] for result in self.results
        ) / len(self.results)

        self.algorithms_value.config(text=str(len(self.results)))
        self.message_value.config(text=f"{size:,}")
        self.fastest_value.config(
            text=fastest["name"].replace(" Cipher", ""),
            font=("Segoe UI", 15, "bold")
        )
        self.average_value.config(text=f"{average:.4f} ms")

    # ========================================================
    # PERFORMANCE CHART
    # ========================================================

    def show_chart(self):
        if not self.results:
            messagebox.showwarning(
                "No Benchmark Data",
                "Please click 'Run Benchmark' before displaying the chart."
            )
            return

        try:
            # Import Matplotlib only when a chart is requested.
            import matplotlib.pyplot as plt
            import numpy as np
            from matplotlib.widgets import Button

            names = [result["name"] for result in self.results]
            times = [result["time_ms"] for result in self.results]

            chart_colors = [CYAN, BLUE, PURPLE, GREEN]

            fig, ax = plt.subplots(figsize=(11, 6))
            fig.patch.set_facecolor("#0B1220")
            ax.set_facecolor("#151F32")

            positions = np.arange(len(names))

            bars = ax.bar(
                positions,
                times,
                color=chart_colors[:len(names)],
                width=0.58,
                edgecolor="#334155",
                linewidth=0.8
            )

            ax.set_title(
                "CLASSICAL CIPHER PERFORMANCE",
                color=WHITE,
                fontsize=15,
                fontweight="bold",
                pad=20
            )

            ax.text(
                0.5,
                1.02,
                f"Average encryption time • "
                f"{self.results[0]['size']:,} characters",
                transform=ax.transAxes,
                ha="center",
                color=MUTED,
                fontsize=10
            )

            ax.set_xlabel(
                "Encryption Algorithm",
                color=CYAN,
                fontsize=11,
                labelpad=12
            )
            ax.set_ylabel(
                "Execution Time (milliseconds)",
                color=CYAN,
                fontsize=11,
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
                alpha=0.22,
                color="#94A3B8"
            )
            ax.set_axisbelow(True)

            for spine in ax.spines.values():
                spine.set_color(BORDER)

            max_time = max(times) if times else 0
            ax.set_ylim(
                bottom=0,
                top=max_time * 1.22 if max_time > 0 else 1
            )

            for bar, value in zip(bars, times):
                ax.annotate(
                    f"{value:.5f} ms",
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

            # =================================================
            # ADDED: BACK TO HOME BUTTON ON THE CHART
            # =================================================

            fig.subplots_adjust(bottom=0.23)

            button_ax = fig.add_axes([0.79, 0.035, 0.18, 0.065])

            back_button = Button(
                button_ax,
                "← Back to Home",
                color="#087F5B",
                hovercolor="#059669"
            )

            back_button.label.set_color("white")
            back_button.label.set_fontsize(10)
            back_button.label.set_fontweight("bold")

            def return_home(event):

                plt.close(fig)

                if self.show_home is not None:
                    self.show_home()

            back_button.on_clicked(return_home)

            # =================================================

            plt.show()

        except ImportError:
            messagebox.showerror(
                "Chart Dependency Missing",
                "Matplotlib and NumPy are required for charts.\n\n"
                "Open Anaconda Prompt and run:\n"
                "conda install matplotlib numpy"
            )

        except Exception as error:
            messagebox.showerror(
                "Chart Error",
                f"Could not display the chart:\n{error}"
            )

    # ========================================================
    # CLEAR RESULTS
    # ========================================================

    def clear_results(self):
        self.results = []

        for item in self.results_table.get_children():
            self.results_table.delete(item)

        self.algorithms_value.config(text="0")
        self.message_value.config(text="—")
        self.fastest_value.config(
            text="—",
            font=("Segoe UI", 19, "bold")
        )
        self.average_value.config(text="—")
        self.result_count.config(text="0 RESULTS")

        self.status_label.config(
            text="● Results cleared. Ready for a new benchmark.",
            fg=MUTED
        )
