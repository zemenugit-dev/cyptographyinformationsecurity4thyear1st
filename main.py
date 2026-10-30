
import tkinter as tk
from tkinter import messagebox

from database.db import initialize_database

from authentication.welcome_screen import WelcomeScreen
from authentication.login_screen import LoginScreen
from authentication.register_screen import RegisterScreen

from screens.home_screen import HomeScreen
from screens.cipher_screen import CipherScreen
from screens.performance_screen import PerformanceScreen
from screens.profile_screen import ProfileScreen


class CryptographyApp:

    def __init__(self, root):

        self.root = root
        self.current_user = None

        self.root.title("Cryptographic Systems Simulator")
        self.root.geometry("1200x800")
        self.root.minsize(950, 650)
        self.root.configure(bg="#F3F6FB")

        # Initialize SQLite database
        initialize_database()

        # Handle window close button
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_application
        )

        # Start with welcome screen
        self.show_welcome()

    # =====================================================
    # CLEAR CURRENT SCREEN
    # =====================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # =====================================================
    # WELCOME SCREEN
    # =====================================================

    def show_welcome(self):

        self.clear_screen()

        self.current_user = None

        screen = WelcomeScreen(
            self.root,
            on_login=self.show_login,
            on_register=self.show_register,
            on_exit=self.exit_application
        )

        screen.pack(fill="both", expand=True)

    # =====================================================
    # LOGIN SCREEN
    # =====================================================

    def show_login(self):

        self.clear_screen()

        screen = LoginScreen(
            self.root,
            on_login=self.handle_login,
            on_register=self.show_register,
            on_back=self.show_welcome
        )

        screen.pack(fill="both", expand=True)

    def handle_login(self, user):

        if not user:
            messagebox.showerror(
                "Login Error",
                "Unable to log in. Please check your credentials.",
                parent=self.root
            )
            return

        self.current_user = user

        self.show_home()

    # =====================================================
    # REGISTRATION SCREEN
    # =====================================================

    def show_register(self):

        self.clear_screen()

        screen = RegisterScreen(
            self.root,
            on_registered=self.show_login,
            on_back=self.show_login
        )

        screen.pack(fill="both", expand=True)

    # =====================================================
    # HOME DASHBOARD
    # =====================================================

    def show_home(self):

        if not self.current_user:
            self.show_login()
            return

        self.clear_screen()

        screen = HomeScreen(
            self.root,
            open_cipher_screen=self.show_ciphers,
            open_performance_screen=self.show_performance,
            current_user=self.current_user,
            on_logout=self.logout,
            on_profile=self.show_profile
        )

        screen.pack(fill="both", expand=True)

    # =====================================================
    # PROFILE SCREEN
    # =====================================================

    def show_profile(self):

        if not self.current_user:
            self.show_login()
            return

        self.clear_screen()

        screen = ProfileScreen(
            self.root,
            current_user=self.current_user,
            on_back=self.show_home
        )

        screen.pack(fill="both", expand=True)

    # =====================================================
    # ENCRYPTION AND DECRYPTION SCREEN
    # =====================================================

    def show_ciphers(self):

        self.clear_screen()

        screen = CipherScreen(
            self.root,
            show_home=self.show_home
        )

        screen.pack(fill="both", expand=True)

    # =====================================================
    # PERFORMANCE ANALYSIS SCREEN
    # =====================================================

    def show_performance(self):

        self.clear_screen()

        screen = PerformanceScreen(
            self.root,
            show_home=self.show_home
        )

        screen.pack(fill="both", expand=True)

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to log out?",
            parent=self.root
        )

        if answer:
            self.current_user = None
            self.show_login()

    # =====================================================
    # EXIT APPLICATION
    # =====================================================

    def exit_application(self):

        answer = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit the Cryptographic "
            "Systems Simulator?",
            parent=self.root
        )

        if answer:
            self.root.destroy()


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CryptographyApp(root)

    root.mainloop()
