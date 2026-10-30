
import tkinter as tk
from tkinter import messagebox

from screens.profile_screen import ProfileScreen


class HomeScreen(tk.Frame):

    def __init__(
        self,
        parent,
        open_cipher_screen=None,
        open_performance_screen=None,
        current_user=None,
        on_logout=None,
        on_profile=None
    ):
        super().__init__(parent, bg="#F3F6FB")

        self.open_cipher_screen = open_cipher_screen
        self.open_performance_screen = open_performance_screen
        self.current_user = current_user or {}
        self.on_logout = on_logout
        self.on_profile = on_profile

        self.create_widgets()

    # =====================================================
    # MAIN DASHBOARD
    # =====================================================

    def create_widgets(self):

        # Header
        header = tk.Frame(
            self,
            bg="#102A43",
            height=90
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        header_left = tk.Frame(header, bg="#102A43")
        header_left.pack(side="left", padx=25, pady=15)

        tk.Label(
            header_left,
            text="🔐 CRYPTOGRAPHIC SYSTEMS SIMULATOR",
            font=("Segoe UI", 17, "bold"),
            bg="#102A43",
            fg="white"
        ).pack(anchor="w")

        full_name = self.current_user.get("full_name", "User")
        username = self.current_user.get("username", "")

        tk.Label(
            header_left,
            text=f"Welcome, {full_name}  |  @{username}",
            font=("Segoe UI", 9),
            bg="#102A43",
            fg="#CBD5E1"
        ).pack(anchor="w", pady=(4, 0))

        header_buttons = tk.Frame(header, bg="#102A43")
        header_buttons.pack(side="right", padx=20)

        self.create_header_button(
            header_buttons,
            "👤 My Profile",
            "#2563EB",
            self.open_profile
        ).pack(side="left", padx=5)

        self.create_header_button(
            header_buttons,
            "Logout",
            "#DC2626",
            self.logout
        ).pack(side="left", padx=5)

        # Main content area
        main = tk.Frame(self, bg="#F3F6FB")
        main.pack(fill="both", expand=True, padx=35, pady=25)

        tk.Label(
            main,
            text="Dashboard",
            font=("Segoe UI", 25, "bold"),
            bg="#F3F6FB",
            fg="#102A43"
        ).pack(anchor="w")

        tk.Label(
            main,
            text="Explore encryption algorithms and analyze their performance.",
            font=("Segoe UI", 11),
            bg="#F3F6FB",
            fg="#64748B"
        ).pack(anchor="w", pady=(5, 22))

        # Main action cards
        action_frame = tk.Frame(main, bg="#F3F6FB")
        action_frame.pack(fill="x", pady=(0, 22))

        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.create_action_card(
            action_frame,
            0,
            "🔐",
            "Encryption & Decryption",
            "Explore classical encryption algorithms. "
            "Encrypt and decrypt messages using different techniques.",
            "Start Encryption",
            "#087F5B",
            self.open_ciphers
        )

        self.create_action_card(
            action_frame,
            1,
            "📊",
            "Performance Analysis",
            "Compare encryption algorithms by execution time "
            "and observe their performance.",
            "Analyze Performance",
            "#2563EB",
            self.open_performance
        )

        # Cipher information section
        tk.Label(
            main,
            text="Available Cryptographic Algorithms",
            font=("Segoe UI", 16, "bold"),
            bg="#F3F6FB",
            fg="#102A43"
        ).pack(anchor="w", pady=(0, 13))

        cipher_frame = tk.Frame(main, bg="#F3F6FB")
        cipher_frame.pack(fill="x")

        cipher_items = [
            ("Caesar Cipher", "A substitution cipher that shifts letters by a fixed number."),
            ("Playfair Cipher", "A digraph substitution cipher that encrypts pairs of letters."),
            ("Vigenere Cipher", "A polyalphabetic cipher that uses a keyword."),
            ("Rail Fence Cipher", "A transposition cipher that rearranges letters in a zigzag pattern."),
            ("Columnar Transposition", "A cipher that rearranges text according to column order."),
            ("Cryptographic Comparison", "Compare algorithms and understand their execution performance.")
        ]

        for index, (name, description) in enumerate(cipher_items):
            row = index // 3
            column = index % 3

            self.create_cipher_card(
                cipher_frame,
                row,
                column,
                name,
                description
            )

        for column in range(3):
            cipher_frame.columnconfigure(column, weight=1)

        # Footer
        tk.Label(
            main,
            text="Cryptographic Systems Simulator  |  Information System Project",
            font=("Segoe UI", 9),
            bg="#F3F6FB",
            fg="#94A3B8"
        ).pack(side="bottom", pady=(22, 0))

    # =====================================================
    # HEADER BUTTON
    # =====================================================

    def create_header_button(self, parent, text, color, command):

        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=9,
            command=command
        )

    # =====================================================
    # ACTION CARDS
    # =====================================================

    def create_action_card(
        self,
        parent,
        column,
        icon,
        title,
        description,
        button_text,
        button_color,
        command
    ):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=8,
            pady=5
        )

        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 27),
            bg="white"
        ).pack(anchor="w", padx=20, pady=(18, 5))

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#102A43"
        ).pack(anchor="w", padx=20, pady=5)

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 10),
            bg="white",
            fg="#64748B",
            wraplength=350,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(3, 15))

        tk.Button(
            card,
            text=button_text,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg="white",
            activebackground=button_color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=10,
            command=command
        ).pack(anchor="w", padx=20, pady=(0, 20))

    # =====================================================
    # CIPHER INFORMATION CARDS
    # =====================================================

    def create_cipher_card(
        self,
        parent,
        row,
        column,
        title,
        description
    ):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=7,
            pady=7
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#087F5B"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748B",
            wraplength=230,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 15))

    # =====================================================
    # NAVIGATION FUNCTIONS
    # =====================================================

    def open_ciphers(self):

        if self.open_cipher_screen:
            self.open_cipher_screen()
        else:
            messagebox.showerror(
                "Navigation Error",
                "Encryption screen is not configured.",
                parent=self
            )

    def open_performance(self):

        if self.open_performance_screen:
            self.open_performance_screen()
        else:
            messagebox.showerror(
                "Navigation Error",
                "Performance screen is not configured.",
                parent=self
            )

    def open_profile(self):

        if self.on_profile:
            self.on_profile()
        else:
            messagebox.showerror(
                "Navigation Error",
                "Profile screen is not configured.",
                parent=self
            )

    def logout(self):

        answer = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to log out?",
            parent=self
        )

        if answer and self.on_logout:
            self.on_logout()
