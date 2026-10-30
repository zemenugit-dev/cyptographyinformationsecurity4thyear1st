"""Modern Tkinter interface for the Cryptographic Systems Simulator.

Place this file at screens/cipher_screen.py in the project.
The cipher algorithms remain in the ciphers package.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ciphers import caesar, playfair, vigenere, rail_fence, columnar


class CipherScreen(tk.Frame):
    """Modern workspace for encrypting and decrypting text."""

    BG = "#F4F7FB"
    NAVY = "#142D4E"
    NAVY_LIGHT = "#203F66"
    BLUE = "#2563EB"
    BLUE_HOVER = "#1D4ED8"
    GREEN = "#059669"
    GREEN_HOVER = "#047857"
    RED = "#DC2626"
    RED_HOVER = "#B91C1C"
    TEXT = "#172B4D"
    MUTED = "#64748B"
    BORDER = "#D9E2EF"
    WHITE = "#FFFFFF"

    CIPHERS = [
        "Caesar Cipher",
        "Playfair Cipher",
        "Vigenere Cipher",
        "Rail Fence Cipher",
        "Columnar Transposition",
    ]

    def __init__(self, parent, show_home=None):
        super().__init__(parent, bg=self.BG)
        self.show_home = show_home
        self.selected_cipher = tk.StringVar(value="Caesar Cipher")
        self.key_value = tk.StringVar()
        self.last_action = None
        self.last_encryption = None
        self._configure_styles()
        self._create_widgets()
        self.update_key_label()

    def _configure_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Modern.TCombobox",
            padding=8,
            fieldbackground=self.WHITE,
            background=self.WHITE,
            foreground=self.TEXT,
            arrowcolor=self.NAVY,
        )
        style.configure(
            "Modern.TEntry",
            padding=8,
            fieldbackground=self.WHITE,
            foreground=self.TEXT,
        )

    def _create_widgets(self):
        # Header stays at the top; action buttons and status stay pinned at the
        # bottom of the application so they remain visible in shorter windows.
        header = tk.Frame(self, bg=self.NAVY, height=88)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        header_inner = tk.Frame(header, bg=self.NAVY)
        header_inner.pack(fill="both", expand=True, padx=22, pady=10)

        brand = tk.Frame(header_inner, bg=self.NAVY)
        brand.pack(side="left", fill="y")
        tk.Label(
            brand, text="CRYPTOGRAPHIC SYSTEMS",
            font=("Segoe UI", 17, "bold"), fg=self.WHITE, bg=self.NAVY,
        ).pack(anchor="w")
        tk.Label(
            brand, text="SECURE TEXT WORKSPACE  •  CLASSICAL CIPHERS",
            font=("Segoe UI", 8, "bold"), fg="#BFD7F4", bg=self.NAVY,
        ).pack(anchor="w", pady=(3, 0))

        if self.show_home is not None:
            self._button(
                header_inner, "←  Back to Home", self.show_home,
                self.NAVY_LIGHT, self.WHITE, hover=self.BLUE, padx=13,
            ).pack(side="right", pady=5)

        # Pinned bottom action bar (packed before the expanding workspace).
        status_frame = tk.Frame(self, bg="#E8EEF7", padx=12, pady=7)
        status_frame.pack(side="bottom", fill="x", padx=18, pady=(0, 10))
        self.status_dot = tk.Label(
            status_frame, text="●", font=("Segoe UI", 10),
            fg=self.BLUE, bg="#E8EEF7",
        )
        self.status_dot.pack(side="left", padx=(0, 8))
        self.status_label = tk.Label(
            status_frame, text="Ready — select a cipher to begin.",
            font=("Segoe UI", 9), fg=self.TEXT, bg="#E8EEF7", anchor="w",
        )
        self.status_label.pack(side="left", fill="x", expand=True)

        actions = tk.Frame(self, bg=self.BG)
        actions.pack(side="bottom", fill="x", padx=22, pady=(8, 7))
        self._button(
            actions, "🔒  Encrypt", self.encrypt_message,
            self.BLUE, self.WHITE, hover=self.BLUE_HOVER, padx=16,
        ).pack(side="left", padx=(0, 7))
        self._button(
            actions, "🔓  Decrypt", self.decrypt_message,
            self.GREEN, self.WHITE, hover=self.GREEN_HOVER, padx=16,
        ).pack(side="left", padx=7)
        self._button(
            actions, "↙  Output → Input", self.use_output_as_input,
            "#E2E8F0", self.NAVY, hover="#CBD5E1", padx=12,
        ).pack(side="left", padx=7)
        self._button(
            actions, "✕  Clear", self.clear_fields,
            "#FEE2E2", self.RED, hover="#FECACA", padx=12,
        ).pack(side="right")

        # The center workspace uses the remaining space and can shrink without
        # pushing the action buttons off-screen.
        main = tk.Frame(self, bg=self.BG)
        main.pack(side="top", fill="both", expand=True, padx=22, pady=(12, 6))

        intro = tk.Frame(main, bg=self.BG)
        intro.pack(fill="x", pady=(0, 10))
        tk.Label(
            intro, text="Cipher workspace", font=("Segoe UI", 18, "bold"),
            fg=self.NAVY, bg=self.BG,
        ).pack(anchor="w")
        tk.Label(
            intro,
            text="Choose an algorithm, enter the key and message, then encrypt or decrypt.",
            font=("Segoe UI", 9), fg=self.MUTED, bg=self.BG,
        ).pack(anchor="w", pady=(2, 0))

        settings = tk.Frame(
            main, bg=self.WHITE, highlightbackground=self.BORDER,
            highlightthickness=1, padx=14, pady=10,
        )
        settings.pack(fill="x", pady=(0, 10))
        tk.Label(
            settings, text="ENCRYPTION SETTINGS", font=("Segoe UI", 8, "bold"),
            fg=self.MUTED, bg=self.WHITE,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 7))
        tk.Label(
            settings, text="Algorithm", font=("Segoe UI", 9, "bold"),
            fg=self.TEXT, bg=self.WHITE,
        ).grid(row=1, column=0, sticky="w", padx=(0, 12))
        self.cipher_box = ttk.Combobox(
            settings, textvariable=self.selected_cipher, values=self.CIPHERS,
            state="readonly", style="Modern.TCombobox",
        )
        self.cipher_box.grid(row=2, column=0, sticky="ew", padx=(0, 14), pady=(3, 0))
        self.cipher_box.bind("<<ComboboxSelected>>", self._on_cipher_changed)

        self.key_label = tk.Label(
            settings, text="Shift", font=("Segoe UI", 9, "bold"),
            fg=self.TEXT, bg=self.WHITE,
        )
        self.key_label.grid(row=1, column=1, sticky="w")
        self.key_entry = ttk.Entry(
            settings, textvariable=self.key_value, style="Modern.TEntry",
        )
        self.key_entry.grid(row=2, column=1, sticky="ew", pady=(3, 0))
        self.key_help = tk.Label(
            settings, text="Use a whole number, e.g. 3.",
            font=("Segoe UI", 8), fg=self.MUTED, bg=self.WHITE,
        )
        self.key_help.grid(row=3, column=1, sticky="w", pady=(3, 0))
        settings.columnconfigure(0, weight=1, uniform="setting")
        settings.columnconfigure(1, weight=1, uniform="setting")

        editors = tk.Frame(main, bg=self.BG)
        editors.pack(fill="both", expand=True)
        editors.columnconfigure(0, weight=1, uniform="editor")
        editors.columnconfigure(1, weight=1, uniform="editor")
        editors.rowconfigure(0, weight=1)
        self._editor_card(
            editors, 0, "01  INPUT MESSAGE",
            "Type the original text or paste ciphertext here.", output=False,
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self._editor_card(
            editors, 1, "02  RESULT",
            "Encrypted or decrypted text appears here.", output=True,
        ).grid(row=0, column=1, sticky="nsew", padx=(6, 0))

    def _editor_card(self, parent, column, title, subtitle, output=False):
        card = tk.Frame(
            parent, bg=self.WHITE, highlightbackground=self.BORDER,
            highlightthickness=1, padx=12, pady=12
        )
        top = tk.Frame(card, bg=self.WHITE)
        top.pack(fill="x", pady=(0, 8))
        tk.Label(
            top, text=title, font=("Segoe UI", 10, "bold"),
            fg=self.NAVY, bg=self.WHITE
        ).pack(anchor="w")
        tk.Label(
            top, text=subtitle, font=("Segoe UI", 8),
            fg=self.MUTED, bg=self.WHITE
        ).pack(anchor="w", pady=(3, 0))

        editor_bg = "#F7FAFE" if output else "#FFFFFF"
        text_box = tk.Text(
            card, height=5, wrap="word", font=("Consolas", 11),
            bg=editor_bg, fg=self.TEXT, insertbackground=self.BLUE,
            selectbackground="#BFDBFE", relief="flat", bd=0,
            padx=10, pady=10, undo=True,
        )
        text_box.pack(fill="both", expand=True)
        text_box.configure(highlightthickness=1, highlightbackground=self.BORDER,
                           highlightcolor=self.BLUE)

        if output:
            self.output_box = text_box
            footer = tk.Frame(card, bg=self.WHITE)
            footer.pack(fill="x", pady=(7, 0))
            self.output_count = tk.Label(
                footer, text="0 characters", font=("Segoe UI", 8),
                fg=self.MUTED, bg=self.WHITE
            )
            self.output_count.pack(side="right")
            self.output_box.bind("<KeyRelease>", lambda _event: self._update_counts())
        else:
            self.input_box = text_box
            footer = tk.Frame(card, bg=self.WHITE)
            footer.pack(fill="x", pady=(7, 0))
            self.input_count = tk.Label(
                footer, text="0 characters", font=("Segoe UI", 8),
                fg=self.MUTED, bg=self.WHITE
            )
            self.input_count.pack(side="right")
            self.input_box.bind("<KeyRelease>", lambda _event: self._update_counts())
        return card

    @staticmethod
    def _button(parent, text, command, bg, fg, hover, padx=14):
        button = tk.Button(
            parent, text=text, command=command,
            font=("Segoe UI", 9, "bold"),
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            relief="flat", bd=0, padx=padx, pady=10,
            cursor="hand2", takefocus=True,
        )
        button.bind("<Enter>", lambda _event: button.configure(bg=hover))
        button.bind("<Leave>", lambda _event: button.configure(bg=bg))
        return button

    def _on_cipher_changed(self, _event=None):
        self.update_key_label()
        self.last_action = None
        self.last_encryption = None
        self._set_status("Cipher changed. Check the key before decrypting.", self.BLUE)

    def update_key_label(self):
        cipher = self.selected_cipher.get()
        details = {
            "Caesar Cipher": ("Shift", "Use a whole number, e.g. 3."),
            "Playfair Cipher": ("Keyword", "English letters, e.g. MONARCHY."),
            "Vigenere Cipher": ("Keyword", "English letters, e.g. LEMON."),
            "Rail Fence Cipher": ("Number of rails", "Use a whole number, e.g. 3."),
            "Columnar Transposition": ("Keyword", "English letters, e.g. ZEBRA."),
        }
        label, help_text = details.get(cipher, ("Key", "Enter the key for the selected cipher."))
        self.key_label.config(text=label)
        self.key_help.config(text=help_text)

    def get_input_and_key(self):
        message = self.input_box.get("1.0", "end-1c")
        key = self.key_value.get().strip()
        if not message.strip():
            raise ValueError("Please enter a message in the input box.")
        if not key:
            raise ValueError("Please enter the required key.")
        return message, key

    def _encrypt_with(self, message, key, cipher):
        if cipher == "Caesar Cipher":
            return caesar.encrypt(message, int(key))
        if cipher == "Playfair Cipher":
            return playfair.encrypt(message, key)
        if cipher == "Vigenere Cipher":
            return vigenere.encrypt(message, key)
        if cipher == "Rail Fence Cipher":
            return rail_fence.encrypt(message, int(key))
        if cipher == "Columnar Transposition":
            return columnar.encrypt(message, key)
        raise ValueError("Please select a supported cipher.")

    def _decrypt_with(self, ciphertext, key, cipher):
        if cipher == "Caesar Cipher":
            return caesar.decrypt(ciphertext, int(key))
        if cipher == "Playfair Cipher":
            return playfair.decrypt(ciphertext, key)
        if cipher == "Vigenere Cipher":
            return vigenere.decrypt(ciphertext, key)
        if cipher == "Rail Fence Cipher":
            return rail_fence.decrypt(ciphertext, int(key))
        if cipher == "Columnar Transposition":
            return columnar.decrypt(ciphertext, key)
        raise ValueError("Please select a supported cipher.")

    def encrypt_message(self):
        try:
            message, key = self.get_input_and_key()
            cipher = self.selected_cipher.get()
            result = self._encrypt_with(message, key, cipher)
            self._show_output(result)
            self.last_action = "encrypt"
            self.last_encryption = {
                "cipher": cipher,
                "key": key,
                "plaintext": message,
                "ciphertext": result,
            }
            self._set_status(f"{cipher} encryption completed successfully.", self.GREEN)
        except (ValueError, TypeError) as error:
            messagebox.showerror("Encryption Error", str(error), parent=self.winfo_toplevel())
        except Exception as error:
            messagebox.showerror(
                "Encryption Error", f"An unexpected error occurred:\n{error}",
                parent=self.winfo_toplevel()
            )

    def decrypt_message(self):
        try:
            cipher = self.selected_cipher.get()
            key = self.key_value.get().strip()

            # Use generated ciphertext only when the cipher and key still match.
            if self.last_action == "encrypt" and self.last_encryption is not None:
                saved = self.last_encryption
                if cipher != saved["cipher"] or key != saved["key"]:
                    raise ValueError(
                        "The selected cipher or key changed after encryption. "
                        "Restore the original cipher and key, or paste the ciphertext "
                        "into the input box before decrypting."
                    )
                ciphertext = self.output_box.get("1.0", "end-1c")
                if ciphertext != saved["ciphertext"]:
                    # Output was manually edited; use the edited ciphertext if non-empty.
                    if not ciphertext.strip():
                        raise ValueError("Please enter ciphertext before decrypting.")
            else:
                ciphertext = self.input_box.get("1.0", "end-1c")

            if not ciphertext.strip():
                raise ValueError("Please enter ciphertext in the input box or encrypt a message first.")
            if not key:
                raise ValueError("Please enter the required key.")

            result = self._decrypt_with(ciphertext, key, cipher)
            self._show_output(result)
            self.last_action = "decrypt"
            self._set_status(f"{cipher} decryption completed successfully.", self.GREEN)
        except (ValueError, TypeError) as error:
            messagebox.showerror("Decryption Error", str(error), parent=self.winfo_toplevel())
        except Exception as error:
            messagebox.showerror(
                "Decryption Error", f"An unexpected error occurred:\n{error}",
                parent=self.winfo_toplevel()
            )

    def _show_output(self, text):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self._update_counts()

    def use_output_as_input(self):
        result = self.output_box.get("1.0", "end-1c")
        if not result.strip():
            messagebox.showwarning(
                "No Output", "Please generate output first.", parent=self.winfo_toplevel()
            )
            return
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", result)
        self.last_action = None
        self.last_encryption = None
        self._update_counts()
        self._set_status("Output copied into the input area.", self.BLUE)

    def clear_fields(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.key_value.set("")
        self.last_action = None
        self.last_encryption = None
        self._update_counts()
        self._set_status("All fields cleared. Ready for a new message.", self.BLUE)
        self.input_box.focus_set()

    def _update_counts(self):
        if hasattr(self, "input_count"):
            count = len(self.input_box.get("1.0", "end-1c"))
            self.input_count.config(text=f"{count} character{'s' if count != 1 else ''}")
        if hasattr(self, "output_count"):
            count = len(self.output_box.get("1.0", "end-1c"))
            self.output_count.config(text=f"{count} character{'s' if count != 1 else ''}")

    def _set_status(self, message, color):
        self.status_label.config(text=message)
        self.status_dot.config(fg=color)
