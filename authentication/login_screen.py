
import tkinter as tk
from tkinter import messagebox

from database.db import (
    authenticate_user,
    get_username_validation,
    validate_email
)


# ============================================================
# LOGIN SCREEN
# ============================================================

class LoginScreen(tk.Frame):

    def __init__(self, parent, on_login, on_register, on_back):

        super().__init__(parent, bg="#071426")

        self.on_login = on_login
        self.on_register = on_register
        self.on_back = on_back

        self.show_password = tk.BooleanVar(value=False)

        self.create_widgets()

    # ========================================================
    # DECORATIVE BACKGROUND — GUI ONLY
    # ========================================================

    def create_background(self):

        self.background_canvas = tk.Canvas(
            self,
            bg="#071426",
            highlightthickness=0
        )

        self.background_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        def draw_background(event=None):

            canvas = self.background_canvas
            canvas.delete("background")

            width = max(canvas.winfo_width(), 1)
            height = max(canvas.winfo_height(), 1)

            # Dark blue gradient
            colors = [
                "#071426",
                "#0A1D35",
                "#102C49",
                "#123B50"
            ]

            for i in range(100):

                y1 = int(i * height / 100)
                y2 = int((i + 1) * height / 100) + 1

                color_index = min(
                    int(i / 25),
                    len(colors) - 1
                )

                canvas.create_rectangle(
                    0, y1, width, y2,
                    fill=colors[color_index],
                    outline="",
                    tags="background"
                )

            # Decorative circles
            circles = [
                (80, 100, 230, "#123B58"),
                (width - 180, 80, 280, "#103D4B"),
                (width - 100, height - 100, 250, "#123B58"),
                (100, height - 80, 190, "#102C49")
            ]

            for x, y, radius, color in circles:

                canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=color,
                    outline="",
                    tags="background"
                )

            # Decorative network lines
            points = [
                (0, height * 0.25),
                (width * 0.18, height * 0.12),
                (width * 0.35, height * 0.30),
                (width * 0.72, height * 0.12),
                (width, height * 0.32),
                (width * 0.12, height * 0.85),
                (width * 0.45, height * 0.72),
                (width * 0.85, height * 0.88)
            ]

            for i in range(len(points) - 1):

                canvas.create_line(
                    points[i][0],
                    points[i][1],
                    points[i + 1][0],
                    points[i + 1][1],
                    fill="#24516A",
                    width=1,
                    tags="background"
                )

            # Small decorative dots
            for x, y in points:

                canvas.create_oval(
                    x - 3, y - 3,
                    x + 3, y + 3,
                    fill="#35B8A0",
                    outline="",
                    tags="background"
                )

        self.background_canvas.bind(
            "<Configure>",
            draw_background
        )

    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def create_widgets(self):

        # Create background first
        self.create_background()

        # Login card
        card = tk.Frame(
            self.background_canvas,
            bg="white",
            highlightbackground="#DCE3EC",
            highlightthickness=1
        )

        # Display card above background
        self.card_window = self.background_canvas.create_window(
            0,
            0,
            window=card,
            width=470,
            height=550
        )

        def center_card(event=None):

            self.background_canvas.coords(
                self.card_window,
                self.background_canvas.winfo_width() / 2,
                self.background_canvas.winfo_height() / 2
            )

        self.background_canvas.bind(
            "<Configure>",
            lambda event: (
                self.background_canvas.after_idle(
                    lambda: center_card(event)
                )
            )
        )

        # Application title
        tk.Label(
            card,
            text="CRYPTOGRAPHIC SYSTEMS",
            font=("Arial", 19, "bold"),
            fg="#17365D",
            bg="white"
        ).pack(pady=(32, 5))

        tk.Label(
            card,
            text="SIMULATOR",
            font=("Arial", 16, "bold"),
            fg="#16804A",
            bg="white"
        ).pack(pady=(0, 10))

        tk.Label(
            card,
            text="Welcome Back!",
            font=("Arial", 21, "bold"),
            fg="#263445",
            bg="white"
        ).pack(pady=(5, 5))

        tk.Label(
            card,
            text="Log in to continue to your simulator",
            font=("Arial", 10),
            fg="#788595",
            bg="white"
        ).pack(pady=(0, 20))

        # ====================================================
        # USERNAME OR EMAIL
        # ====================================================

        tk.Label(
            card,
            text="Username or Email",
            font=("Arial", 10, "bold"),
            fg="#344054",
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=45)

        self.username_entry = tk.Entry(
            card,
            font=("Arial", 12),
            bg="#F7F9FC",
            fg="#263445",
            relief="solid",
            bd=1
        )

        self.username_entry.pack(
            fill="x",
            padx=45,
            ipady=8,
            pady=(6, 2)
        )

        self.username_status = tk.Label(
            card,
            text="Enter your username or registered email.",
            font=("Arial", 8),
            fg="#788595",
            bg="white",
            anchor="w"
        )

        self.username_status.pack(
            fill="x",
            padx=45,
            pady=(0, 8)
        )

        # ====================================================
        # PASSWORD
        # ====================================================

        tk.Label(
            card,
            text="Password",
            font=("Arial", 10, "bold"),
            fg="#344054",
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=45)

        self.password_entry = tk.Entry(
            card,
            font=("Arial", 12),
            bg="#F7F9FC",
            fg="#263445",
            relief="solid",
            bd=1,
            show="*"
        )

        self.password_entry.pack(
            fill="x",
            padx=45,
            ipady=8,
            pady=(6, 2)
        )

        self.password_status = tk.Label(
            card,
            text="",
            font=("Arial", 8),
            fg="#DC2626",
            bg="white",
            anchor="w"
        )

        self.password_status.pack(
            fill="x",
            padx=45,
            pady=(0, 5)
        )

        # ====================================================
        # SHOW / HIDE PASSWORD
        # ====================================================

        self.show_password_check = tk.Checkbutton(
            card,
            text="Show password",
            variable=self.show_password,
            command=self.toggle_password,
            font=("Arial", 9),
            fg="#526174",
            bg="white",
            activebackground="white",
            selectcolor="white",
            cursor="hand2"
        )

        self.show_password_check.pack(
            anchor="w",
            padx=43,
            pady=(0, 8)
        )

        # ====================================================
        # LOGIN BUTTON
        # ====================================================

        self.login_button = tk.Button(
            card,
            text="LOGIN",
            command=self.login,
            font=("Arial", 11, "bold"),
            bg="#16804A",
            fg="white",
            activebackground="#10663A",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        self.login_button.pack(
            fill="x",
            padx=45,
            ipady=9,
            pady=(0, 9)
        )

        # ====================================================
        # CLEAR BUTTON
        # ====================================================

        tk.Button(
            card,
            text="CLEAR FIELDS",
            command=self.clear_fields,
            font=("Arial", 9, "bold"),
            bg="#E9EEF5",
            fg="#344054",
            activebackground="#DCE3EC",
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=45,
            ipady=7,
            pady=(0, 8)
        )

        # ====================================================
        # REGISTER LINK
        # ====================================================

        bottom_frame = tk.Frame(
            card,
            bg="white"
        )

        bottom_frame.pack(pady=4)

        tk.Label(
            bottom_frame,
            text="Don't have an account?",
            font=("Arial", 9),
            fg="#667085",
            bg="white"
        ).pack(side="left")

        tk.Button(
            bottom_frame,
            text="Register",
            command=self.on_register,
            font=("Arial", 9, "bold"),
            fg="#16804A",
            bg="white",
            activebackground="white",
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=4)

        # ====================================================
        # BACK TO WELCOME
        # ====================================================

        tk.Button(
            card,
            text="← Back to Welcome",
            command=self.go_back,
            font=("Arial", 9),
            fg="#526174",
            bg="white",
            activebackground="white",
            relief="flat",
            cursor="hand2"
        ).pack(pady=(7, 0))

        # ====================================================
        # LIVE VALIDATION EVENTS
        # ====================================================

        self.username_entry.bind(
            "<KeyRelease>",
            self.update_username_validation
        )

        self.password_entry.bind(
            "<KeyRelease>",
            self.update_password_validation
        )

        self.username_entry.focus_set()

        # Press Enter to log in
        self.bind_all(
            "<Return>",
            self.handle_enter
        )

    # ========================================================
    # LIVE USERNAME OR EMAIL VALIDATION
    # ========================================================

    def update_username_validation(self, event=None):

        username = self.username_entry.get().strip()

        if not username:

            self.username_status.config(
                text="✗ Username or email is required.",
                fg="#DC2626"
            )

            return

        if validate_email(username):

            self.username_status.config(
                text="✓ Valid email address format.",
                fg="#15803D"
            )

            return

        validation = get_username_validation(username)

        if not validation["length"]:

            self.username_status.config(
                text="✗ Username must contain 3 to 30 characters.",
                fg="#DC2626"
            )

            return

        if not validation["characters"]:

            self.username_status.config(
                text="✗ Use letters, numbers, dots and underscores only.",
                fg="#DC2626"
            )

            return

        self.username_status.config(
            text="✓ Valid username format.",
            fg="#15803D"
        )

    # ========================================================
    # LIVE PASSWORD ENTRY FEEDBACK
    # ========================================================

    def update_password_validation(self, event=None):

        password = self.password_entry.get()

        if not password:

            self.password_status.config(
                text="✗ Please enter your password.",
                fg="#DC2626"
            )

        else:

            self.password_status.config(
                text="✓ Password entered. Credentials will be verified.",
                fg="#15803D"
            )

    # ========================================================
    # SHOW / HIDE PASSWORD
    # ========================================================

    def toggle_password(self):

        if self.show_password.get():

            self.password_entry.config(show="")

        else:

            self.password_entry.config(show="*")

    # ========================================================
    # CLEAR FIELDS
    # ========================================================

    def clear_fields(self):

        self.username_entry.delete(0, tk.END)

        self.password_entry.delete(0, tk.END)

        self.username_status.config(
            text="Enter your username or registered email.",
            fg="#788595"
        )

        self.password_status.config(text="")

        self.username_entry.focus_set()

    # ========================================================
    # ENTER KEY HANDLER
    # ========================================================

    def handle_enter(self, event=None):

        self.login()

        return "break"

    # ========================================================
    # LOGIN PROCESS
    # ========================================================

    def login(self):

        username = self.username_entry.get().strip()

        # Do not strip the password.
        # Password spaces may be significant.
        password = self.password_entry.get()

        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter your username/email and password.",
                parent=self
            )

            return

        self.update_username_validation()

        username_validation = get_username_validation(username)

        valid_username = all(username_validation.values())

        valid_email = validate_email(username)

        if not valid_username and not valid_email:

            messagebox.showerror(
                "Invalid Username or Email",
                "Please enter a valid username or email address.",
                parent=self
            )

            self.username_entry.focus_set()

            return

        # Verify account and password
        try:

            user = authenticate_user(
                username,
                password
            )

        except Exception as error:

            messagebox.showerror(
                "Authentication Error",
                (
                    "An error occurred while checking your account.\n\n"
                    f"Details: {error}"
                ),
                parent=self
            )

            return

        # Invalid credentials
        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid username/email or password.\nPlease try again.",
                parent=self
            )

            self.password_entry.delete(0, tk.END)

            self.password_status.config(text="")

            self.password_entry.focus_set()

            return

        # Successful authentication
        self.unbind_all("<Return>")

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {user['full_name']}!",
            parent=self
        )

        self.on_login(user)

    # ========================================================
    # BACK TO WELCOME
    # ========================================================

    def go_back(self):

        self.unbind_all("<Return>")

        self.on_back()
