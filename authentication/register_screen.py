
import tkinter as tk
from tkinter import messagebox

from database.db import (
    register_user,
    is_username_available,
    get_username_validation,
    get_password_validation,
    validate_email
)


class RegisterScreen(tk.Frame):

    def __init__(self, parent, on_registered, on_back):
        super().__init__(parent, bg="#071426")

        self.parent = parent
        self.on_registered = on_registered
        self.on_back = on_back

        self.password_visible = False

        self.create_interface()

    # =========================================================
    # MAIN INTERFACE
    # =========================================================

    def create_interface(self):

        main_frame = tk.Frame(self, bg="#071426")
        main_frame.pack(fill="both", expand=True)

        self.create_background(main_frame)

        # Registration card
        self.card = tk.Frame(
            main_frame,
            bg="#FFFFFF",
            highlightbackground="#14B8A6",
            highlightthickness=2
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=0.94,
            relheight=0.96
        )

        # Scrollable area inside the card
        self.card_canvas = tk.Canvas(
            self.card,
            bg="#FFFFFF",
            highlightthickness=0
        )

        self.card_scrollbar = tk.Scrollbar(
            self.card,
            orient="vertical",
            command=self.card_canvas.yview
        )

        self.card_canvas.configure(
            yscrollcommand=self.card_scrollbar.set
        )

        self.card_scrollbar.pack(side="right", fill="y")
        self.card_canvas.pack(side="left", fill="both", expand=True)

        self.form_frame = tk.Frame(
            self.card_canvas,
            bg="#FFFFFF"
        )

        self.form_window = self.card_canvas.create_window(
            (0, 0),
            window=self.form_frame,
            anchor="n"
        )

        self.form_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.card_canvas.bind(
            "<Configure>",
            self.resize_form
        )

        self.card_canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.create_form_widgets()

    # =========================================================
    # BACKGROUND DESIGN
    # =========================================================

    def create_background(self, parent):

        self.background_canvas = tk.Canvas(
            parent,
            bg="#071426",
            highlightthickness=0
        )

        self.background_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.background_canvas.bind(
            "<Configure>",
            self.draw_background
        )

    def draw_background(self, event=None):

        canvas = self.background_canvas

        canvas.delete("background")

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Decorative circles
        canvas.create_oval(
            -120, -120, 230, 230,
            fill="#102D46",
            outline="",
            tags="background"
        )

        canvas.create_oval(
            width - 220, height - 220,
            width + 120, height + 120,
            fill="#0D3445",
            outline="",
            tags="background"
        )

        canvas.create_oval(
            width - 170, 30,
            width + 70, 270,
            outline="#164E63",
            width=2,
            tags="background"
        )

        canvas.create_oval(
            30, height - 170,
            210, height + 10,
            outline="#164E63",
            width=2,
            tags="background"
        )

        # Network-style decorative lines
        points = [
            (40, 100),
            (150, 180),
            (width - 100, 100),
            (width - 180, height - 100),
            (100, height - 80)
        ]

        for i in range(len(points) - 1):

            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            canvas.create_line(
                x1, y1, x2, y2,
                fill="#164E63",
                width=1,
                tags="background"
            )

        for x, y in points:

            canvas.create_oval(
                x - 4, y - 4,
                x + 4, y + 4,
                fill="#14B8A6",
                outline="",
                tags="background"
            )

    # =========================================================
    # SCROLLING
    # =========================================================

    def update_scroll_region(self, event=None):

        self.card_canvas.configure(
            scrollregion=self.card_canvas.bbox("all")
        )

    def resize_form(self, event):

        self.card_canvas.itemconfigure(
            self.form_window,
            width=event.width
        )

    def on_mousewheel(self, event):

        if not self.winfo_ismapped():
            return

        self.card_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # =========================================================
    # REGISTRATION FORM
    # =========================================================

    def create_form_widgets(self):

        content = self.form_frame

        # Main heading
        tk.Label(
            content,
            text="CRYPTOGRAPHIC SYSTEMS",
            font=("Segoe UI", 13, "bold"),
            bg="#FFFFFF",
            fg="#087F5B"
        ).pack(pady=(22, 3))

        tk.Label(
            content,
            text="SIMULATOR",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#64748B"
        ).pack(pady=(0, 12))

        tk.Label(
            content,
            text="Create Your Account",
            font=("Segoe UI", 23, "bold"),
            bg="#FFFFFF",
            fg="#102A43"
        ).pack(pady=(0, 5))

        tk.Label(
            content,
            text="Register to access the Cryptographic Systems Simulator",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#64748B",
            wraplength=440
        ).pack(pady=(0, 18))

        # Full Name
        self.create_field(
            "Full Name",
            "Enter your full name",
            "full_name"
        )

        # Username
        self.create_field(
            "Username",
            "Choose a username",
            "username"
        )

        self.username_status = self.create_status_label()

        self.username_entry.bind(
            "<KeyRelease>",
            self.update_username_validation
        )

        # Email
        self.create_field(
            "Email Address",
            "Enter your email address",
            "email"
        )

        self.email_status = self.create_status_label()

        self.email_entry.bind(
            "<KeyRelease>",
            self.update_email_validation
        )

        # Password
        self.create_field(
            "Password",
            "Create a strong password",
            "password",
            show="*"
        )

        self.password_status = self.create_status_label()

        self.password_entry.bind(
            "<KeyRelease>",
            self.update_password_validation
        )

        # Password requirements
        self.create_password_requirements()

        # Confirm Password
        self.create_field(
            "Confirm Password",
            "Re-enter your password",
            "confirm_password",
            show="*"
        )

        self.confirm_status = self.create_status_label()

        self.confirm_password_entry.bind(
            "<KeyRelease>",
            self.update_confirm_validation
        )

        # Show passwords
        self.show_password_var = tk.BooleanVar(value=False)

        tk.Checkbutton(
            content,
            text="Show Passwords",
            variable=self.show_password_var,
            command=self.toggle_password,
            bg="#FFFFFF",
            fg="#334155",
            activebackground="#FFFFFF",
            font=("Segoe UI", 9),
            cursor="hand2"
        ).pack(anchor="w", padx=48, pady=(8, 12))

        # Create account button
        self.create_button(
            content,
            "CREATE ACCOUNT",
            self.register,
            "#087F5B"
        )

        # Clear fields button
        self.create_button(
            content,
            "CLEAR FIELDS",
            self.clear_fields,
            "#475569"
        )

        # Login section
        tk.Label(
            content,
            text="Already have an account?",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#64748B"
        ).pack(pady=(15, 3))

        tk.Button(
            content,
            text="← Back to Login Page",
            command=self.go_to_login,
            bg="#FFFFFF",
            fg="#087F5B",
            activebackground="#E6FFFA",
            activeforeground="#065F46",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            pady=8
        ).pack(pady=(0, 22))

    # =========================================================
    # FORM FIELD CREATION
    # =========================================================

    def create_field(self, label_text, placeholder, field_name, show=""):

        container = tk.Frame(
            self.form_frame,
            bg="#FFFFFF"
        )

        container.pack(
            fill="x",
            padx=45,
            pady=(5, 2)
        )

        tk.Label(
            container,
            text=label_text,
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#334155"
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            container,
            font=("Segoe UI", 10),
            bg="#F1F5F9",
            fg="#102A43",
            insertbackground="#102A43",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#14B8A6",
            show=show
        )

        entry.pack(
            fill="x",
            ipady=10
        )

        entry.insert(0, "")

        if field_name == "full_name":
            self.full_name_entry = entry

        elif field_name == "username":
            self.username_entry = entry

        elif field_name == "email":
            self.email_entry = entry

        elif field_name == "password":
            self.password_entry = entry

        elif field_name == "confirm_password":
            self.confirm_password_entry = entry

    def create_status_label(self):

        label = tk.Label(
            self.form_frame,
            text="",
            font=("Segoe UI", 8),
            bg="#FFFFFF",
            fg="#64748B"
        )

        label.pack(
            anchor="w",
            padx=48,
            pady=(1, 2)
        )

        return label

    def set_status(self, label, message, color="#64748B"):

        label.config(
            text=message,
            fg=color
        )

    # =========================================================
    # PASSWORD REQUIREMENTS
    # =========================================================

    def create_password_requirements(self):

        self.requirements_frame = tk.Frame(
            self.form_frame,
            bg="#F8FAFC",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        self.requirements_frame.pack(
            fill="x",
            padx=45,
            pady=(5, 8)
        )

        tk.Label(
            self.requirements_frame,
            text="Password Requirements",
            font=("Segoe UI", 9, "bold"),
            bg="#F8FAFC",
            fg="#334155"
        ).pack(anchor="w", padx=12, pady=(8, 4))

        self.requirement_labels = {}

        requirements = [
            ("length", "At least 11 characters"),
            ("uppercase", "At least one uppercase letter"),
            ("lowercase", "At least one lowercase letter"),
            ("number", "At least one number"),
            ("special", "At least one special character")
        ]

        for key, description in requirements:

            label = tk.Label(
                self.requirements_frame,
                text="○  " + description,
                font=("Segoe UI", 8),
                bg="#F8FAFC",
                fg="#64748B"
            )

            label.pack(
                anchor="w",
                padx=15,
                pady=2
            )

            self.requirement_labels[key] = label

        tk.Frame(
            self.requirements_frame,
            bg="#F8FAFC",
            height=6
        ).pack()

    # =========================================================
    # LIVE VALIDATION
    # =========================================================

    def update_username_validation(self, event=None):

        username = self.username_entry.get().strip()

        if not username:

            self.set_status(
                self.username_status,
                "Username is required.",
                "#DC2626"
            )
            return

        # get_username_validation returns a dictionary
        validation = get_username_validation(username)

        if not validation["length"]:

            self.set_status(
                self.username_status,
                "Username must contain 3 to 30 characters.",
                "#DC2626"
            )
            return

        if not validation["characters"]:

            self.set_status(
                self.username_status,
                "Use only letters, numbers, underscores and periods.",
                "#DC2626"
            )
            return

        if not is_username_available(username):

            self.set_status(
                self.username_status,
                "Username is already taken.",
                "#DC2626"
            )
            return

        self.set_status(
            self.username_status,
            "Username is available.",
            "#087F5B"
        )

    def update_email_validation(self, event=None):

        email = self.email_entry.get().strip()

        if not email:

            self.set_status(
                self.email_status,
                "Email address is required.",
                "#DC2626"
            )
            return

        if not validate_email(email):

            self.set_status(
                self.email_status,
                "Please enter a valid email address.",
                "#DC2626"
            )
            return

        self.set_status(
            self.email_status,
            "Email format is valid.",
            "#087F5B"
        )

    def update_password_validation(self, event=None):

        password = self.password_entry.get()

        # get_password_validation returns a dictionary
        validation = get_password_validation(password)

        checks = {
            "length": validation["length"],
            "uppercase": validation["uppercase"],
            "lowercase": validation["lowercase"],
            "number": validation["number"],
            "special": validation["special"]
        }

        for key, passed in checks.items():

            if passed:
                symbol = "✓"
                color = "#087F5B"
            else:
                symbol = "○"
                color = "#64748B"

            description = self.requirement_labels[key].cget("text")
            description = description[3:]

            self.requirement_labels[key].config(
                text=symbol + "  " + description,
                fg=color
            )

        if not password:

            self.set_status(
                self.password_status,
                "Password is required.",
                "#DC2626"
            )

        elif all(checks.values()):

            self.set_status(
                self.password_status,
                "Strong password.",
                "#087F5B"
            )

        else:

            self.set_status(
                self.password_status,
                "Password does not meet all requirements.",
                "#DC2626"
            )

        if self.confirm_password_entry.get():
            self.update_confirm_validation()

    def update_confirm_validation(self, event=None):

        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not confirm_password:

            self.set_status(
                self.confirm_status,
                "Please confirm your password.",
                "#DC2626"
            )

        elif password == confirm_password:

            self.set_status(
                self.confirm_status,
                "Passwords match.",
                "#087F5B"
            )

        else:

            self.set_status(
                self.confirm_status,
                "Passwords do not match.",
                "#DC2626"
            )

    # =========================================================
    # BUTTONS
    # =========================================================

    def create_button(self, parent, text, command, color):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#FFFFFF",
            activebackground="#065F46",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            pady=11
        )

        button.pack(
            fill="x",
            padx=45,
            pady=5
        )

        return button

    # =========================================================
    # SHOW / HIDE PASSWORD
    # =========================================================

    def toggle_password(self):

        self.password_visible = self.show_password_var.get()

        if self.password_visible:
            show_value = ""
        else:
            show_value = "*"

        self.password_entry.config(show=show_value)
        self.confirm_password_entry.config(show=show_value)

    # =========================================================
    # CLEAR FIELDS
    # =========================================================

    def clear_fields(self):

        self.full_name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

        self.set_status(self.username_status, "")
        self.set_status(self.email_status, "")
        self.set_status(self.password_status, "")
        self.set_status(self.confirm_status, "")

        self.show_password_var.set(False)
        self.toggle_password()

        self.update_password_validation()

    # =========================================================
    # REGISTER ACCOUNT
    # =========================================================

    def register(self):

        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check required fields
        if not all([
            full_name,
            username,
            email,
            password,
            confirm_password
        ]):

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all registration fields."
            )
            return

        # Validate username
        username_validation = get_username_validation(username)

        if not username_validation["length"]:

            messagebox.showerror(
                "Invalid Username",
                "Username must contain 3 to 30 characters."
            )
            return

        if not username_validation["characters"]:

            messagebox.showerror(
                "Invalid Username",
                "Use only letters, numbers, underscores and periods."
            )
            return

        if not is_username_available(username):

            messagebox.showerror(
                "Username Exists",
                "This username is already taken. Please choose another."
            )
            return

        # Validate email
        if not validate_email(email):

            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return

        # Validate password
        password_validation = get_password_validation(password)

        if not all(password_validation.values()):

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least 11 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number, and one special character."
            )
            return

        # Confirm password
        if password != confirm_password:

            messagebox.showerror(
                "Password Mismatch",
                "Your passwords do not match."
            )
            return

        # Save user to database
        try:

            success, result = register_user(
                full_name,
                username,
                email,
                password
            )

            if success:

                messagebox.showinfo(
                    "Registration Successful",
                    "Your account has been created successfully!"
                )

                self.clear_fields()
                self.on_registered()

            else:

                messagebox.showerror(
                    "Registration Failed",
                    str(result)
                )

        except Exception as error:

            messagebox.showerror(
                "Registration Error",
                f"An error occurred while creating your account:\n{error}"
            )

    # =========================================================
    # BACK TO LOGIN
    # =========================================================

    def go_to_login(self):

        self.on_back()
