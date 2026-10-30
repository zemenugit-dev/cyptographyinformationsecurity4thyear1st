
import tkinter as tk
from tkinter import messagebox
import math
import random


class WelcomeScreen(tk.Frame):

    # ========================================================
    # COLORS
    # ========================================================

    BG = "#071426"
    CARD = "#FFFFFF"
    NAVY = "#102A43"
    GREEN = "#159B62"
    GREEN_HOVER = "#087A4A"
    BLUE = "#173F70"
    BLUE_HOVER = "#102F56"
    TEXT = "#243B53"
    MUTED = "#718096"
    LIGHT = "#F1F5F9"

    def __init__(self, parent, on_login, on_register, on_exit):
        super().__init__(parent, bg=self.BG)

        self.on_login = on_login
        self.on_register = on_register
        self.on_exit = on_exit

        self.animation_running = True
        self.particles = []
        self.canvas = None

        self.create_widgets()
        self.create_particles()
        self.animate_background()

        self.bind("<Destroy>", self.stop_animation)

    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def create_widgets(self):

        # Animated background canvas
        self.canvas = tk.Canvas(
            self,
            bg=self.BG,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Main card
        self.card = tk.Frame(
            self.canvas,
            bg=self.CARD,
            highlightbackground="#294867",
            highlightthickness=1
        )

        self.card_window = self.canvas.create_window(
            0,
            0,
            window=self.card,
            width=790,
            height=550
        )

        self.canvas.bind("<Configure>", self.resize_card)

        self.create_card_content()

    def resize_card(self, event):

        card_width = min(790, max(600, event.width - 50))
        card_height = min(550, max(500, event.height - 40))

        self.canvas.coords(
            self.card_window,
            event.width / 2,
            event.height / 2
        )

        self.canvas.itemconfigure(
            self.card_window,
            width=card_width,
            height=card_height
        )

    # ========================================================
    # CARD CONTENT
    # ========================================================

    def create_card_content(self):

        # Left panel
        self.left_panel = tk.Frame(
            self.card,
            bg=self.NAVY,
            width=340
        )

        self.left_panel.pack(
            side="left",
            fill="both"
        )

        self.left_panel.pack_propagate(False)

        # Right panel
        self.right_panel = tk.Frame(
            self.card,
            bg=self.CARD
        )

        self.right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_left_panel()
        self.create_right_panel()

    # ========================================================
    # LEFT PANEL
    # ========================================================

    def create_left_panel(self):

        tk.Label(
            self.left_panel,
            text="◈  CRYPTOGRAPHY",
            font=("Arial", 12, "bold"),
            fg="#50DCA0",
            bg=self.NAVY
        ).pack(pady=(48, 30))

        # Security icon
        tk.Label(
            self.left_panel,
            text="🔐",
            font=("Segoe UI Emoji", 65),
            bg=self.NAVY,
            fg="white"
        ).pack(pady=(5, 15))

        tk.Label(
            self.left_panel,
            text="SECURE YOUR",
            font=("Arial", 22, "bold"),
            fg="white",
            bg=self.NAVY
        ).pack()

        tk.Label(
            self.left_panel,
            text="DIGITAL WORLD",
            font=("Arial", 22, "bold"),
            fg="#50DCA0",
            bg=self.NAVY
        ).pack()

        tk.Label(
            self.left_panel,
            text=(
                "Understand the science of protecting "
                "information through cryptography."
            ),
            font=("Arial", 10),
            fg="#C1D3E5",
            bg=self.NAVY,
            wraplength=260,
            justify="center"
        ).pack(padx=30, pady=(20, 30))

        # Feature information
        features = [
            "✓  Encryption and Decryption",
            "✓  Classical Cipher Algorithms",
            "✓  Performance Analysis"
        ]

        for feature in features:

            tk.Label(
                self.left_panel,
                text=feature,
                font=("Arial", 10),
                fg="#D9E8F5",
                bg=self.NAVY,
                anchor="w"
            ).pack(
                anchor="w",
                padx=35,
                pady=8
            )

        tk.Label(
            self.left_panel,
            text="LEARN  •  EXPLORE  •  PROTECT",
            font=("Arial", 8, "bold"),
            fg="#50DCA0",
            bg=self.NAVY
        ).pack(side="bottom", pady=25)

    # ========================================================
    # RIGHT PANEL
    # ========================================================

    def create_right_panel(self):

        content = tk.Frame(
            self.right_panel,
            bg=self.CARD
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=35
        )

        tk.Label(
            content,
            text="WELCOME",
            font=("Arial", 11, "bold"),
            fg=self.GREEN,
            bg=self.CARD
        ).pack(pady=(18, 8))

        tk.Label(
            content,
            text="Cryptographic",
            font=("Arial", 23, "bold"),
            fg=self.NAVY,
            bg=self.CARD
        ).pack()

        tk.Label(
            content,
            text="Systems Simulator",
            font=("Arial", 21, "bold"),
            fg=self.BLUE,
            bg=self.CARD
        ).pack(pady=(0, 12))

        tk.Label(
            content,
            text=(
                "Your interactive environment for learning "
                "cryptographic techniques."
            ),
            font=("Arial", 9),
            fg=self.MUTED,
            bg=self.CARD,
            wraplength=320,
            justify="center"
        ).pack(pady=(5, 20))

        # Separator
        tk.Frame(
            content,
            bg="#E2E8F0",
            height=1
        ).pack(fill="x", pady=(0, 20))

        tk.Label(
            content,
            text="GET STARTED",
            font=("Arial", 10, "bold"),
            fg=self.TEXT,
            bg=self.CARD
        ).pack(anchor="w", pady=(0, 12))

        # Login button
        self.create_action_button(
            content,
            text="LOGIN TO YOUR ACCOUNT",
            command=self.on_login,
            bg=self.GREEN,
            hover_bg=self.GREEN_HOVER
        )

        # Register button
        self.create_action_button(
            content,
            text="CREATE NEW ACCOUNT",
            command=self.on_register,
            bg=self.BLUE,
            hover_bg=self.BLUE_HOVER
        )

        # About button
        self.create_action_button(
            content,
            text="ABOUT THE APPLICATION",
            command=self.show_about,
            bg="#E9EFF6",
            hover_bg="#DCE6F0",
            fg=self.TEXT,
            hover_fg=self.NAVY
        )

        # Exit button
        self.create_action_button(
            content,
            text="EXIT APPLICATION",
            command=self.exit_application,
            bg="#FFF0F0",
            hover_bg="#FADADA",
            fg="#B42318",
            hover_fg="#912018"
        )

        tk.Label(
            content,
            text="© 2026 Cryptographic Systems Simulator",
            font=("Arial", 8),
            fg="#98A2B3",
            bg=self.CARD
        ).pack(side="bottom", pady=(18, 0))

    # ========================================================
    # BUTTON DESIGN AND HOVER EFFECT
    # ========================================================

    def create_action_button(
        self,
        parent,
        text,
        command,
        bg,
        hover_bg,
        fg="white",
        hover_fg="white"
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=hover_fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            height=2,
            width=30
        )

        button.pack(
            fill="x",
            pady=5
        )

        button.bind(
            "<Enter>",
            lambda event: button.config(
                bg=hover_bg,
                fg=hover_fg
            )
        )

        button.bind(
            "<Leave>",
            lambda event: button.config(
                bg=bg,
                fg=fg
            )
        )

        return button

    # ========================================================
    # ANIMATED BACKGROUND
    # ========================================================

    def create_particles(self):

        self.particles = []

        for _ in range(45):

            particle = {
                "x": random.randint(0, 1100),
                "y": random.randint(0, 750),
                "speed": random.uniform(0.3, 1.2),
                "size": random.randint(2, 4)
            }

            self.particles.append(particle)

    def animate_background(self):

        if not self.animation_running:
            return

        if not self.winfo_exists():
            return

        self.canvas.delete("particle")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            self.after(50, self.animate_background)
            return

        # Move and draw particles
        for particle in self.particles:

            particle["y"] -= particle["speed"]

            if particle["y"] < 0:
                particle["y"] = height
                particle["x"] = random.randint(0, width)

            x = particle["x"]
            y = particle["y"]
            size = particle["size"]

            self.canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill="#2875A8",
                outline="",
                tags="particle"
            )

        # Draw connecting lines between nearby particles
        for i, particle in enumerate(self.particles):

            for other in self.particles[i + 1:]:

                distance = math.sqrt(
                    (particle["x"] - other["x"]) ** 2
                    +
                    (particle["y"] - other["y"]) ** 2
                )

                if distance < 95:

                    self.canvas.create_line(
                        particle["x"],
                        particle["y"],
                        other["x"],
                        other["y"],
                        fill="#173A58",
                        width=1,
                        tags="particle"
                    )

        self.after(45, self.animate_background)

    def stop_animation(self, event):

        if event.widget == self:
            self.animation_running = False

    # ========================================================
    # ABOUT APPLICATION
    # ========================================================

    def show_about(self):

        messagebox.showinfo(
            "About the Application",
            (
                "CRYPTOGRAPHIC SYSTEMS SIMULATOR\n\n"
                "This application is designed to demonstrate "
                "cryptographic techniques through an interactive "
                "learning environment.\n\n"
                "Main Features:\n"
                "• Classical encryption algorithms\n"
                "• Encryption and decryption\n"
                "• Performance comparison and charts\n"
                "• Cryptography learning environment\n\n"
                "Developed as an educational project."
            ),
            parent=self
        )

    # ========================================================
    # EXIT APPLICATION
    # ========================================================

    def exit_application(self):

        answer = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit?",
            parent=self
        )

        if answer:
            self.on_exit()
