import tkinter as tk
from tkinter import messagebox
from repositories.user import UserRepository

class LoginWindow(tk.Tk):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.title("SwimShop POS - Authentication")
        self.geometry("760x640")
        self.resizable(False, False)
        self.configure(bg="#0F172A")
        self.user_repo = UserRepository()
        self.on_login_success = on_login_success

        self.__create_widgets()
        self.__center_window()

    def __center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def __create_widgets(self):
        card = tk.Frame(self, bg="#FFFFFF", padx=40, pady=45)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420)

        # Brand Icon / Wave Logo Accent
        brand_icon = tk.Label(
            card,
            text="🌊",
            font=("Segoe UI Emoji", 32),
            bg="#FFFFFF",
            fg="#0284C7"
        )
        brand_icon.pack(pady=(0, 5))

        title = tk.Label(
            card,
            text="SwimShop POS",
            font=("Segoe UI", 20, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        )
        title.pack()

        subtitle = tk.Label(
            card,
            text="Point of Sale System Login",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#64748B"
        )
        subtitle.pack(pady=(2, 24))

        # Error Label
        self.error_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#EF4444"
        )
        self.error_label.pack(pady=(0, 10))

        # Username input field
        username_lbl = tk.Label(
            card,
            text="USERNAME",
            font=("Segoe UI", 8, "bold"),
            bg="#FFFFFF",
            fg="#475569",
            anchor="w"
        )
        username_lbl.pack(fill="x")

        self.username_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#0F172A",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            highlightcolor="#0EA5E9"  # Focus border color
        )
        self.username_entry.pack(fill="x", ipady=8, pady=(4, 16))
        self.username_entry.focus()
        self.username_entry.bind("<Key>", lambda e: self._clear_error())

        # Password input field
        password_lbl = tk.Label(
            card,
            text="PASSWORD",
            font=("Segoe UI", 8, "bold"),
            bg="#FFFFFF",
            fg="#475569",
            anchor="w"
        )
        password_lbl.pack(fill="x")

        # Container for Password Input + Eye Toggle Button
        pwd_frame = tk.Frame(card, bg="#F8FAFC", highlightthickness=1, highlightbackground="#CBD5E1")
        pwd_frame.pack(fill="x", pady=(4, 24))

        self.password_entry = tk.Entry(
            pwd_frame,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#0F172A",
            show="•",
            relief="flat",
            bd=0
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=8)
        self.password_entry.bind("<Key>", lambda e: self._clear_error())

        # Show/Hide Password Toggle Button
        self.show_password = False
        self.toggle_btn = tk.Button(
            pwd_frame,
            text="👁",
            font=("Segoe UI Emoji", 10),
            bg="#F8FAFC",
            fg="#64748B",
            activebackground="#F8FAFC",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._toggle_password_visibility
        )
        self.toggle_btn.pack(side="right", padx=8)

        # Enter key triggers login
        self.bind("<Return>", lambda event: self._handle_login())

        # Login Button
        self.login_btn = tk.Button(
            card,
            text="Sign In to POS",
            font=("Segoe UI", 10, "bold"),
            bg="#0284C7",
            fg="white",
            activebackground="#0369A1",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._handle_login
        )
        self.login_btn.pack(fill="x", ipady=10)

        # Button Hover
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#0369A1"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#0284C7"))

    def _toggle_password_visibility(self):
        if self.show_password:
            self.password_entry.config(show="•")
            self.show_password = False
        else:
            self.password_entry.config(show="")
            self.show_password = True

    def _clear_error(self):
        self.error_label.config(text="")

    def _handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.config(text="Username and password are required to continue.")
            return

        user = self.user_repo.authenticate(username, password)

        if user:
            self.destroy()
            if self.on_login_success:
                self.on_login_success(user)
        else:
            self.error_label.config(text="Invalid username or password.")
            self.password_entry.delete(0, tk.END)