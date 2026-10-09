import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User
from models.category import Category
from models.product import Product
from models.order import Order, OrderItem, OrderStatus
from repositories.category import CategoryRepository
from repositories.product import ProductRepository
from repositories.order import OrderRepository

from datetime import datetime

class CartItem:
    def __init__(self, product: Product):
        self.product = product
        self.quantity = 1

    @property
    def total_price(self) -> float:
        return self.product.price * self.quantity

class Cart:
    def __init__(self):
        self.items: dict[int, CartItem] = {}

    def add_product(self, product: Product) -> tuple[bool, str]:
        product_id = product.product_id
        if product_id in self.items:
            if self.items[product_id].quantity < product.stock_quantity:
                self.items[product_id].quantity += 1
                return True, "Increased quantity"
            return False, "Maximum available stock reached"
        else:
            if product.stock_quantity > 0:
                self.items[product_id] = CartItem(product)
                return True, "Added to cart"
            return False, "Item is out of stock"

    def update_quantity(self, product_id: int, delta: int, stock_limit: int) -> bool:
        if product_id in self.items:
            new_quantity = self.items[product_id].quantity + delta
            if new_quantity > stock_limit:
                return False
            self.items[product_id].quantity = new_quantity
            if self.items[product_id].quantity <= 0:
                del self.items[product_id]
        return True

    def clear(self):
        self.items.clear()

    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items.values())

class MainWindow(tk.Tk):
    def __init__(self, current_user: User, on_logout=None):
        super().__init__()
        self.current_user = current_user
        self.on_logout = on_logout
        self.category_repository = CategoryRepository()
        self.product_repository = ProductRepository()
        self.order_repository = OrderRepository()
        self.cart = Cart()

        self.selected_category_id: int | None = None

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
        self.pos_tab = tk.Frame(self.notebook, bg="#FFFFFF", padx=20, pady=20)
        self.notebook.add(self.pos_tab, text="🛒 POS Checkout")
        self._build_pos()

        if is_admin:
            self.inventory_tab = tk.Frame(self.notebook, bg="#FFFFFF", padx=20, pady=20)
            self.notebook.add(self.inventory_tab, text="📦 Inventory Management")
            self._build_inventory()

    """Builds and splits container into three panels"""
    """LEFT: Category Navigation"""
    """RIGHT: Cart Summary"""
    """Middle: Search Bar and Product Container"""
    def _build_pos(self):
        pos_container = tk.Frame(self.pos_tab, bg="#F8FAFC", padx=10, pady=10)
        pos_container.pack(fill="both", expand=True)

        """ LEFT PANEL """
        self.left_panel = tk.Frame(pos_container, bg="#FFFFFF", width=180, relief="flat", highlightthickness=1, highlightbackground="#E2E8F0")
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False)

        category_title = tk.Label(self.left_panel, text="CATEGORIES", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#64748B")
        category_title.pack(anchor="w", padx=12, pady=(15, 10))
        self._render_categories()


        """ RIGHT PANEL """
        right_panel = tk.Frame(pos_container, bg="#FFFFFF", width=340, highlightthickness=1, highlightbackground="#E2E8F0")
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        cart_title = tk.Label(right_panel, text="CURRENT ORDER", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#0F172A")
        cart_title.pack(anchor="w", padx=15, pady=(15, 10))

        self.cart_scroll_frame = tk.Frame(right_panel, bg="#F8FAFC", highlightthickness=1, highlightbackground="#E2E8F0")
        self.cart_scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        summary_frame = tk.Frame(right_panel, bg="#FFFFFF", padx=15, pady=10)
        summary_frame.pack(fill="x", side="bottom")

        total_frame = tk.Frame(summary_frame, bg="#FFFFFF")
        total_frame.pack(fill="x", pady=(0, 10))

        tk.Label(total_frame, text="Total:", font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg="#0F172A").pack(side="left")
        self.total_val_label = tk.Label(total_frame, text="$0.00", font=("Segoe UI", 14, "bold"), bg="#FFFFFF", fg="#16A34A")
        self.total_val_label.pack(side="right")

        checkout_btn = tk.Button(
            summary_frame, text="Complete Checkout", font=("Segoe UI", 10, "bold"),
            bg="#16A34A", fg="white", activebackground="#15803D", activeforeground="white",
            relief="flat", cursor="hand2", command=self._handle_checkout
        )
        checkout_btn.pack(fill="x", ipady=8)


        """ MIDDLE PANEL """
        middle_panel = tk.Frame(pos_container, bg="#F8FAFC")
        middle_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        search_frame = tk.Frame(middle_panel, bg="#F8FAFC")
        search_frame.pack(fill="x", pady=(0, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._render_products())

        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, font=("Segoe UI", 10),
            bg="#FFFFFF", fg="#0F172A", relief="flat", highlightthickness=1,
            highlightbackground="#CBD5E1", highlightcolor="#0284C7"
        )
        search_entry.pack(fill="x", ipady=6)

        self.products_container = tk.Frame(middle_panel, bg="#F8FAFC")
        self.products_container.pack(fill="both", expand=True)

        self._last_calculated_columns = 3
        self.products_container.bind("<Configure>", self._on_products_resize)

        self._render_products()
        self._render_cart()

    """ Fetches Categories from the Database"""
    def _render_categories(self):
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        db_categories = self.category_repository.get_all()

        is_all_active = (self.selected_category_id is None)
        all_button = tk.Button(
            self.left_panel, text="All Items",
            font=("Segoe UI", 9, "bold" if is_all_active else "normal"),
            bg="#E0F2FE" if is_all_active else "#FFFFFF",
            fg="#0369A1" if is_all_active else "#334155",
            anchor="w", padx=12, pady=8, relief="flat", cursor="hand2",
            command=lambda: self._select_category(None)
        )
        all_button.pack(fill="x", pady=2)

        for category in db_categories:
            is_active = (category.category_id == self.selected_category_id)
            btn = tk.Button(
                self.left_panel, text=category.name,
                font=("Segoe UI", 9, "bold" if is_active else "normal"),
                bg="#E0F2FE" if is_active else "#FFFFFF",
                fg="#0369A1" if is_active else "#334155",
                anchor="w", padx=12, pady=8, relief="flat", cursor="hand2",
                command=lambda cid=category.category_id: self._select_category(cid)
            )
            btn.pack(fill="x", pady=2)

    """ Displays chosen category products """
    def _select_category(self, category_id: int | None):
        self.selected_category_id = category_id
        self._render_categories()
        self._render_products()

    """ Fetches products from the database """
    def _render_products(self):
        for widget in self.products_container.winfo_children():
            widget.destroy()

        columns_count, _ = self.products_container.grid_size()
        for c in range(columns_count):
            self.products_container.grid_columnconfigure(c, weight=0, uniform="")

        search_query = self.search_var.get().strip()

        if search_query:
            products = self.product_repository.search(search_query)
            if self.selected_category_id is not None:
                products = [p for p in products if p.category_id == self.selected_category_id]
        elif self.selected_category_id is not None:
            products = self.product_repository.get_by_category(self.selected_category_id)
        else:
            products = self.product_repository.get_all()

        if not products:
            tk.Label(self.products_container, text="No products found.", font=("Segoe UI", 11), bg="#F8FAFC", fg="#64748B").pack(pady=40)
            return

        max_columns = getattr(self, "_last_calculated_columns", 3)
        for c in range(max_columns):
            self.products_container.grid_columnconfigure(c, weight=1, uniform="card_col")

        for i, prod in enumerate(products):
            row = i // max_columns
            col = i % max_columns

            card = tk.Frame(self.products_container, bg="#FFFFFF", padx=12, pady=12, highlightthickness=1, highlightbackground="#E2E8F0")
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.products_container.grid_columnconfigure(col, weight=1)

            # Display Product Details
            title_text = f"{prod.brand} {prod.name}" if prod.brand else prod.name
            tk.Label(card, text=title_text, font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#0F172A", anchor="w").pack(fill="x")
            tk.Label(card, text=f"${prod.price:.2f}", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#0284C7", anchor="w").pack(fill="x", pady=(2, 0))

            # Stock Badge with Warning Colors
            stock_fg = "#DC2626" if prod.out_of_stock else ("#D97706" if prod.low_stock else "#64748B")
            stock_text = "Out of Stock" if prod.out_of_stock else f"Stock: {prod.stock_quantity}"
            tk.Label(card, text=stock_text, font=("Segoe UI", 8, "bold" if prod.low_stock or prod.out_of_stock else "normal"), bg="#FFFFFF", fg=stock_fg, anchor="w").pack(fill="x", pady=(0, 8))

            btn_state = "disabled" if prod.out_of_stock else "normal"
            add_btn = tk.Button(
                card, text="+ Add to Cart", font=("Segoe UI", 8, "bold"),
                bg="#0284C7" if not prod.out_of_stock else "#94A3B8",
                fg="white", activebackground="#0369A1", activeforeground="white",
                relief="flat", cursor="hand2" if not prod.out_of_stock else "arrow",
                state=btn_state,
                command=lambda p=prod: self._add_to_cart(p)
            )
            add_btn.pack(fill="x", ipady=3)

    """ CART """

    def _add_to_cart(self, product: Product):
        success, msg = self.cart.add_product(product)
        if not success:
            messagebox.showwarning("Cannot add to cart", msg)
        self._render_cart()

    """ Fetches curent Cart state """
    def _render_cart(self):
        for widget in self.cart_scroll_frame.winfo_children():
            widget.destroy()

        if not self.cart.items:
            tk.Label(self.cart_scroll_frame, text="Your cart is empty.", font=("Segoe UI", 9), bg="#F8FAFC", fg="#94A3B8").pack(pady=30)
            self.total_val_label.config(text="$0.00")
            return

        for item in self.cart.items.values():
            item_frame = tk.Frame(self.cart_scroll_frame, bg="#FFFFFF", padx=8, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
            item_frame.pack(fill="x", pady=2)

            info_frame = tk.Frame(item_frame, bg="#FFFFFF")
            info_frame.pack(side="left", fill="both", expand=True)

            item_title = f"{item.product.brand} {item.product.name}" if item.product.brand else item.product.name
            tk.Label(info_frame, text=item_title, font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#0F172A", anchor="w").pack(fill="x")
            tk.Label(info_frame, text=f"${item.product.price:.2f} x {item.quantity} = ${item.total_price:.2f}", font=("Segoe UI", 8), bg="#FFFFFF", fg="#64748B", anchor="w").pack(fill="x")

            ctrl_frame = tk.Frame(item_frame, bg="#FFFFFF")
            ctrl_frame.pack(side="right")

            minus_button = tk.Button(
                ctrl_frame, text="-", font=("Segoe UI", 9, "bold"), bg="#E2E8F0", fg="#0F172A",
                relief="flat", width=2, command=lambda pid=item.product.product_id, stock=item.product.stock_quantity: self._set_cart_quantity(pid, -1, stock)
            )
            minus_button.pack(side="left", padx=2)

            plus_button = tk.Button(
                ctrl_frame, text="+", font=("Segoe UI", 9, "bold"), bg="#E2E8F0", fg="#0F172A",
                relief="flat", width=2, command=lambda pid=item.product.product_id, stock=item.product.stock_quantity: self._set_cart_quantity(pid, 1, stock)
            )
            plus_button.pack(side="left", padx=2)

        self.total_val_label.config(text=f"${self.cart.total_amount:.2f}")

    """ Handles items quantity inside the Cart """
    def _set_cart_quantity(self, product_id: int, delta: int, stock_limit: int):
        success = self.cart.update_quantity(product_id, delta, stock_limit)
        if not success:
            messagebox.showwarning("Stock Limit", f"Cannot add more items. Maximum available stock is {stock_limit}.")
        self._render_cart()

    """ Processes order completion """
    def _handle_checkout(self):
        if not self.cart.items:
            messagebox.showwarning("Cart Empty", "Please add items to the cart before checking out.")
            return

        total = self.cart.total_amount
        confirm =  messagebox.askyesno("Confirm Transaction", f"Complete transaction for ${total:.2f}?")

        if not confirm:
            return

        order_items = []

        for cart_item in self.cart.items.values():
            order_items.append(
                OrderItem(
                    product_id=cart_item.product.product_id,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.price
                )
            )


        new_order = Order(
            customer_id=1,
            user_id=self.current_user.user_id,
            order_datetime=datetime.now(),
            total_amount=self.cart.total_amount,
            status=OrderStatus.PENDING,
            items=order_items
        )

        order_id = self.order_repository.create_order(new_order)

        if order_id:
            messagebox.showinfo("Success", f"Transaction completed!\nTotal paid: ${total:.2f}")
            self.cart.clear()
            self._render_cart()
            self._render_products()
        else:
            messagebox.showerror(
                "Database Error", 
                "Failed to record the transaction in the database. Please try again."
            )

    """ Resize products depending on the window dimentions """
    def _on_products_resize(self, event):
        card_width = 190
        new_columns = max(1, event.width // card_width)

        if new_columns != getattr(self, "_last_calculated_columns", 3):
            self._last_calculated_columns = new_columns
            self.products_container.unbind("<Configure>")
            self._render_products()
            self.products_container.bind("<Configure>", self._on_products_resize)

    """ Placeholder for inventory view """
    def _build_inventory(self):
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

    """ Session management """
    def _handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.destroy()
            if self.on_logout:
                self.on_logout()


    