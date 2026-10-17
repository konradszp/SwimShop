import tkinter as tk
from tkinter import ttk, messagebox

from models.user import User
from repositories.category import CategoryRepository
from repositories.product import ProductRepository
from repositories.order import OrderRepository

from .inventory import InventoryView
from .orders import OrdersView
from .pos import POSView

class MainWindow(tk.Tk):
    def __init__(self, current_user: User, on_logout=None):
        super().__init__()
        self.current_user = current_user
        self.on_logout = on_logout
        self.category_repository = CategoryRepository()
        self.product_repository = ProductRepository()
        self.order_repository = OrderRepository()

        self.title(f"Swimshop Main Window - User: {current_user.full_name}")
        self.geometry("1200x800")
        self.minsize(950, 600)
        self.configure(bg="#F1F5F9")

        self._center_window()
        self._create_widgets()


    """ Set up application window to the middle of the screen """
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    """ LAYOUT """
    def _create_widgets(self):
        navbar = tk.Frame(self, bg="#0F172A", height=60)
        navbar.pack(fill='x', side='top')
        navbar.pack_propagate(False)

        brand_label = tk.Label(
            navbar,
            text="SwimShop",
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

        role = (
            self.current_user.role.value 
            if hasattr(self.current_user.role, "value")
            else str(self.current_user.role)
        )
        is_admin = role == "ADMIN"
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

        """ Main Container """
        container = tk.Frame(self, bg="#F1F5F9", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#F1F5F9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[16, 8], background="#E2E8F0")
        style.map("TNotebook.Tab", background=[("selected", "#0284C7")], foreground=[("selected", "#FFFFFF")])

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.pos_view = POSView(
            parent=self.notebook,
            current_user=self.current_user,
            category_repository=self.category_repository,
            product_repository=self.product_repository,
            order_repository=self.order_repository,
            on_order_created=self._refresh_orders
        )
        self.notebook.add(self.pos_view, text="🛒 POS Checkout")

        if is_admin:
            self.inventory_view = InventoryView(
                parent=self.notebook,
                product_repository=self.product_repository
            )
            self.notebook.add(self.inventory_view, text="📦 Inventory Management")

            self.orders_view = OrdersView(
                parent=self.notebook,
                order_repository=self.order_repository
            )
            self.notebook.add(self.orders_view, text="📦 Orders Management")

    """ Resize products depending on the window dimentions """
    def _on_products_resize(self, event):
        card_width = 190
        new_columns = max(1, event.width // card_width)

        if new_columns != getattr(self, "_last_calculated_columns", 3):
            self._last_calculated_columns = new_columns
            self.products_container.unbind("<Configure>")
            self._render_products()
            self.products_container.bind("<Configure>", self._on_products_resize)

    def _refresh_orders(self):
        if hasattr(self, "orders_view"):
            self.orders_view.refresh()

    """ Session management """
    def _handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.destroy()
            if self.on_logout:
                self.on_logout()