import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User

class MainWindow(tk.Tk):
    def __init__(self, current_user: User, on_logout=None):
        super().__init__()
        self.current_user = current_user
        self.on_logout = on_logout

        self.title(f"Swimshop Main Window - User: {current_user.full_name}")
        self.geometry("1200x800")
        self.configure(bg="#F1F5F9")

        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        navbar = tk.Frame(self, bg="#0F172A", height=60)
        navbar.pack(fill='x', side='top')
        navbar.pack_propagate(False)

        brand_label = tk.Label(
            navbar,
            text="SwimShop POS",
            font=("Segoe UI", 14, "bold"),
            bg="#0F172A",
            fg="#F8FAFC"
        )
        brand_label.pack(side='left', padx=20)

        logout_button = tk.Button(
            navbar,
            text="Logout",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._handle_logout
        )
        logout_button.pack(side="right", padx=20, pady=12)

        role = self.current_user.role.value if hasattr(self.current_user.role, "value") else str(self.current_user.role)

        role_color = "#38BDF8" if self.current_user.role == "ADMIN" else "#4ADE80"
        user_info = f"{self.current_user.full_name} ({role})"

        user_label = tk.Label(
            navbar,
            text=user_info,
            font=("Segoe UI", 10, "bold"),
            bg="#0F172A",
            fg=role_color
        )
        user_label.pack(side="right", padx=10)


        # Main Container
        container = tk.Frame(self, bg="#F1F5F9", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#F1F5F9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[16, 8], background="#E2E8F0")
        style.map("TNotebook.Tab", background=[("selected", "#0284C7")], foreground=[("selected", "#FFFFFF")])

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.pos_tab = tk.Frame(self.notebook, bg="#FFFFFF", padx=20, pady=20)
        self.notebook.add(self.pos_tab, text="🛒 POS Checkout")
        self.pos_placeholder()

        if self.current_user.role == "ADMIN":
            self.inventory_tab = tk.Frame(self.notebook, bg="#FFFFFF", padx=20, pady=20)
            self.notebook.add(self.inventory_tab, text="📦 Inventory Management")
            self.inventory_placeholder()

    # Placeholders for POS and Inventory

    def pos_placeholder(self):
        welcome_lbl = tk.Label(
            self.pos_tab,
            text=f"Hi, {self.current_user.full_name}!",
            font=("Segoe UI", 16, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        )
        welcome_lbl.pack(anchor="w", pady=(0, 10))

        desc_lbl = tk.Label(
            self.pos_tab,
            text="Point of Sale (todo)",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#64748B"
        )
        desc_lbl.pack(anchor="w")

    def inventory_placeholder(self):
        admin_lbl = tk.Label(
            self.inventory_tab,
            text="Inventory Management",
            font=("Segoe UI", 16, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        )
        admin_lbl.pack(anchor="w", pady=(0, 10))

        desc_lbl = tk.Label(
            self.inventory_tab,
            text="Inventory Manager (todo)",
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#64748B"
        )
        desc_lbl.pack(anchor="w")

    def _handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.destroy()
            if self.on_logout:
                self.on_logout()