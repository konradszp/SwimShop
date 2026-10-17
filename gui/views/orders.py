import tkinter as tk
from tkinter import ttk

class OrdersView(tk.Frame):
    def __init__(self, parent, order_repository):
        super().__init__(parent, bg="#FFFFFF", padx=20, pady=20)   # parent must be positional
        self.order_repository = order_repository
        self._build_orders()
        self.refresh()

    """ Orders View """
    def _build_orders(self):
        
        orders_container = tk.Frame(self, bg="#F8FAFC", padx=10, pady=10)
        orders_container.pack(fill="both", expand=True)

        top_bar = tk.Frame(orders_container, bg="#F8FAFC")
        top_bar.pack(fill="x", pady=(0,10))

        refresh_button = tk.Button(
            top_bar, text="🔄 Refresh Orders", font=("Segoe UI", 9, "bold"),
            bg="#0284C7", fg="white", activebackground="#0369A1", activeforeground="white",
            relief="flat", cursor="hand2", command=self._render_orders
        )
        refresh_button.pack(side="left", ipady=4, ipadx=10)

        table_frame = tk.Frame(orders_container, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E2E8F0")
        table_frame.pack(fill="both", expand=True)

        """ Orders Table Style """
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Orders.Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Orders.Treeview.Heading",
            background="#0F172A",
            foreground="#F8FAFC",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 6)
        )
        style.map(
            "Orders.Treeview",
            background=[("selected", "#0284C7")],
            foreground=[("selected", "#FFFFFF")]
        )
        style.map(
            "Orders.Treeview.Heading",
            background=[("active", "#1E293B")]
        )

        # --- Treeview ---
        columns = ("order_id", "date", "customer_id", "user_id", "total", "status")
        self.orders_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Orders.Treeview"
        )

        self.orders_tree.heading("order_id", text="Order ID")
        self.orders_tree.heading("date", text="Date & Time")
        self.orders_tree.heading("customer_id", text="Customer Name")
        self.orders_tree.heading("user_id", text="Cashier ID")
        self.orders_tree.heading("total", text="Total Amount")
        self.orders_tree.heading("status", text="Status")

        self.orders_tree.column("order_id", width=90, anchor="center")
        self.orders_tree.column("date", width=190, anchor="w")
        self.orders_tree.column("customer_id", width=110, anchor="center")
        self.orders_tree.column("user_id", width=110, anchor="center")
        self.orders_tree.column("total", width=130, anchor="e")
        self.orders_tree.column("status", width=120, anchor="center")

        # Row tags
        self.orders_tree.tag_configure("odd", background="#F8FAFC")
        self.orders_tree.tag_configure("even", background="#FFFFFF")
        self.orders_tree.tag_configure("completed", foreground="#166534")
        self.orders_tree.tag_configure("cancelled", foreground="#991B1B")
        self.orders_tree.tag_configure("pending", foreground="#92400E")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)

        self.orders_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._render_orders()

    def _render_orders(self):
        if not hasattr(self, "orders_tree"):
            return

        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)

        orders = self.order_repository.get_all()
        if not orders:
            return
        
        for index, order in enumerate(orders):
            status_key = order.status.value.lower()
            row_tag = "even" if index % 2 == 0 else "odd"

            self.orders_tree.insert(
                "",
                "end",
                values=(
                    order.order_id,
                    order.order_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    order.customer_name,
                    order.user_id,
                    f"${order.total_amount:.2f}",
                    order.status.value.capitalize()
                ),
                tags=(row_tag, status_key)
            )


    def refresh(self):
        """Public method so MainWindow / POSView can trigger a refresh."""
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)

        orders = self.order_repository.get_all()
        if not orders:
            return

        for index, order in enumerate(orders):
            status_key = order.status.value.lower()
            row_tag = "even" if index % 2 == 0 else "odd"

            self.orders_tree.insert(
                "",
                "end",
                values=(
                    order.order_id,
                    order.order_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    order.customer_name,
                    order.user_id,
                    f"${order.total_amount:.2f}",
                    order.status.value.capitalize()
                ),
                tags=(row_tag, status_key)
            )