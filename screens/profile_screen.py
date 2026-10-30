
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database.db import (
    get_connection,
    hash_password,
    verify_password,
    validate_email
)


class ProfileScreen(tk.Frame):

    def __init__(self, parent, current_user, on_back=None):

        super().__init__(parent, bg="#F3F6FB")

        self.current_user = current_user
        self.on_back = on_back

        self.configure(bg="#F3F6FB")

        self.full_name_var = tk.StringVar(
            value=current_user.get("full_name", "")
        )

        self.username_var = tk.StringVar(
            value=current_user.get("username", "")
        )

        self.email_var = tk.StringVar(
            value=current_user.get("email", "")
        )

        self.old_password_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        self.show_password_var = tk.BooleanVar(value=False)

        self.create_interface()

    # =====================================================
    # MAIN INTERFACE
    # =====================================================

    def create_interface(self):

        # Header
        header = tk.Frame(
            self,
            bg="#102A43",
            height=85
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="👤  USER PROFILE",
            font=("Segoe UI", 21, "bold"),
            bg="#102A43",
            fg="white"
        ).pack(side="left", padx=30, pady=20)

        tk.Button(
            header,
            text="← Back to Home",
            font=("Segoe UI", 10, "bold"),
            bg="#16A085",
            fg="white",
            activebackground="#138D75",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9,
            command=self.go_back
        ).pack(side="right", padx=30)

        # Main content
        content = tk.Frame(
            self,
            bg="#F3F6FB"
        )
        content.pack(fill="both", expand=True, padx=30, pady=25)

        title = tk.Label(
            content,
            text="My Account",
            font=("Segoe UI", 23, "bold"),
            bg="#F3F6FB",
            fg="#102A43"
        )
        title.pack(anchor="w")

        tk.Label(
            content,
            text="Manage your personal information and account security.",
            font=("Segoe UI", 10),
            bg="#F3F6FB",
            fg="#64748B"
        ).pack(anchor="w", pady=(3, 20))

        # Two-column layout
        columns = tk.Frame(
            content,
            bg="#F3F6FB"
        )
        columns.pack(fill="both", expand=True)

        columns.columnconfigure(0, weight=1)
        columns.columnconfigure(1, weight=1)

        # Left column
        left = tk.Frame(columns, bg="#F3F6FB")
        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        # Right column
        right = tk.Frame(columns, bg="#F3F6FB")
        right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(12, 0)
        )

        self.create_account_card(left)
        self.create_edit_card(left)
        self.create_password_card(right)

    # =====================================================
    # ACCOUNT INFORMATION CARD
    # =====================================================

    def create_account_card(self, parent):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(fill="x", pady=(0, 18))

        tk.Label(
            card,
            text="ACCOUNT INFORMATION",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#102A43"
        ).pack(anchor="w", padx=22, pady=(20, 15))

        # Profile avatar
        avatar = tk.Label(
            card,
            text=self.get_initials(),
            font=("Segoe UI", 24, "bold"),
            bg="#D1FAE5",
            fg="#047857",
            width=4,
            height=2
        )
        avatar.pack(anchor="w", padx=22)

        tk.Label(
            card,
            textvariable=self.full_name_var,
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#102A43"
        ).pack(anchor="w", padx=22, pady=(12, 2))

        tk.Label(
            card,
            text="@" + self.username_var.get(),
            font=("Segoe UI", 10),
            bg="white",
            fg="#64748B"
        ).pack(anchor="w", padx=22, pady=(0, 15))

        self.create_info_row(
            card,
            "Username",
            self.username_var
        )

        self.create_info_row(
            card,
            "Email Address",
            self.email_var
        )

        self.create_info_row(
            card,
            "Account Created",
            tk.StringVar(
                value=self.current_user.get(
                    "created_at", "Not available"
                )
            )
        )

        tk.Label(
            card,
            text="Account Status: Active",
            font=("Segoe UI", 10, "bold"),
            bg="#ECFDF5",
            fg="#047857",
            padx=12,
            pady=8
        ).pack(anchor="w", padx=22, pady=20)

    def create_info_row(self, parent, label, variable):

        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", padx=22, pady=8)

        tk.Label(
            row,
            text=label,
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748B"
        ).pack(anchor="w")

        tk.Label(
            row,
            textvariable=variable,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(anchor="w", pady=(3, 0))

        tk.Frame(
            parent,
            bg="#E2E8F0",
            height=1
        ).pack(fill="x", padx=22, pady=5)

    # =====================================================
    # EDIT PROFILE CARD
    # =====================================================

    def create_edit_card(self, parent):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(fill="x")

        tk.Label(
            card,
            text="EDIT PERSONAL INFORMATION",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#102A43"
        ).pack(anchor="w", padx=22, pady=(20, 15))

        self.create_entry(
            card,
            "Full Name",
            self.full_name_var
        )

        self.create_entry(
            card,
            "Email Address",
            self.email_var
        )

        tk.Button(
            card,
            text="Save Changes",
            font=("Segoe UI", 10, "bold"),
            bg="#087F5B",
            fg="white",
            activebackground="#066B4C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.update_profile
        ).pack(anchor="w", padx=22, pady=(10, 22))

    # =====================================================
    # CHANGE PASSWORD CARD
    # =====================================================

    def create_password_card(self, parent):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(fill="x")

        tk.Label(
            card,
            text="CHANGE PASSWORD",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#102A43"
        ).pack(anchor="w", padx=22, pady=(20, 8))

        tk.Label(
            card,
            text="Protect your account by using a strong password.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748B"
        ).pack(anchor="w", padx=22, pady=(0, 15))

        self.create_password_entry(
            card,
            "Current Password",
            self.old_password_var
        )

        self.create_password_entry(
            card,
            "New Password",
            self.new_password_var
        )

        self.create_password_entry(
            card,
            "Confirm New Password",
            self.confirm_password_var
        )

        tk.Checkbutton(
            card,
            text="Show Passwords",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            bg="white",
            fg="#475569",
            activebackground="white",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=22, pady=8)

        tk.Button(
            card,
            text="Update Password",
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.change_password
        ).pack(anchor="w", padx=22, pady=(10, 20))

        tk.Label(
            card,
            text="Password requirements: at least 11 characters, "
                 "uppercase, lowercase, number and special character.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748B",
            wraplength=340,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 20))

    # =====================================================
    # REUSABLE ENTRY FUNCTIONS
    # =====================================================

    def create_entry(self, parent, label, variable):

        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=22, pady=(8, 5))

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg="#1E293B",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#2563EB"
        )
        entry.pack(fill="x", padx=22, ipady=9)

    def create_password_entry(self, parent, label, variable):

        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=22, pady=(8, 5))

        entry = tk.Entry(
            parent,
            textvariable=variable,
            show="*",
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg="#1E293B",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#2563EB"
        )
        entry.pack(fill="x", padx=22, ipady=9)

        if not hasattr(self, "password_entries"):
            self.password_entries = []

        self.password_entries.append(entry)

    # =====================================================
    # PROFILE FUNCTIONS
    # =====================================================

    def get_initials(self):

        name = self.current_user.get("full_name", "User").strip()

        parts = name.split()

        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()

        return name[:2].upper()

    def update_profile(self):

        full_name = self.full_name_var.get().strip()
        email = self.email_var.get().strip()

        if not full_name:
            messagebox.showerror(
                "Validation Error",
                "Full name is required.",
                parent=self
            )
            return

        if not validate_email(email):
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid email address.",
                parent=self
            )
            return

        try:

            connection = get_connection()

            try:
                connection.execute(
                    """
                    UPDATE users
                    SET full_name = ?, email = ?
                    WHERE id = ?
                    """,
                    (
                        full_name,
                        email,
                        self.current_user["id"]
                    )
                )

                connection.commit()

            finally:
                connection.close()

            self.current_user["full_name"] = full_name
            self.current_user["email"] = email

            messagebox.showinfo(
                "Success",
                "Your profile has been updated successfully.",
                parent=self
            )

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Email Already Exists",
                "This email address is already registered.",
                parent=self
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self
            )

    # =====================================================
    # PASSWORD FUNCTIONS
    # =====================================================

    def toggle_password_visibility(self):

        show_value = "" if self.show_password_var.get() else "*"

        for entry in self.password_entries:
            entry.config(show=show_value)

    def change_password(self):

        old_password = self.old_password_var.get()
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not old_password or not new_password or not confirm_password:

            messagebox.showerror(
                "Missing Information",
                "Please fill in all password fields.",
                parent=self
            )
            return

        if len(new_password) < 11:

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least 11 characters.",
                parent=self
            )
            return

        if not any(c.isupper() for c in new_password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain an uppercase letter.",
                parent=self
            )
            return

        if not any(c.islower() for c in new_password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain a lowercase letter.",
                parent=self
            )
            return

        if not any(c.isdigit() for c in new_password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain a number.",
                parent=self
            )
            return

        if not any(not c.isalnum() and not c.isspace()
                   for c in new_password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain a special character.",
                parent=self
            )
            return

        if new_password != confirm_password:

            messagebox.showerror(
                "Password Mismatch",
                "New password and confirmation do not match.",
                parent=self
            )
            return

        if old_password == new_password:

            messagebox.showerror(
                "Invalid Password",
                "New password must be different from the current password.",
                parent=self
            )
            return

        try:

            connection = get_connection()

            try:

                user = connection.execute(
                    """
                    SELECT password_hash, salt
                    FROM users
                    WHERE id = ?
                    """,
                    (self.current_user["id"],)
                ).fetchone()

                if user is None or not verify_password(
                    old_password,
                    user["password_hash"],
                    user["salt"]
                ):

                    messagebox.showerror(
                        "Incorrect Password",
                        "Your current password is incorrect.",
                        parent=self
                    )
                    return

                new_hash, new_salt = hash_password(new_password)

                connection.execute(
                    """
                    UPDATE users
                    SET password_hash = ?, salt = ?
                    WHERE id = ?
                    """,
                    (
                        new_hash,
                        new_salt,
                        self.current_user["id"]
                    )
                )

                connection.commit()

            finally:
                connection.close()

            self.old_password_var.set("")
            self.new_password_var.set("")
            self.confirm_password_var.set("")

            messagebox.showinfo(
                "Success",
                "Your password has been changed successfully.",
                parent=self
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self
            )

    # =====================================================
    # NAVIGATION
    # =====================================================

    def go_back(self):

        if self.on_back:
            self.on_back()
