import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
    
class InventoryView(tk.Frame):
    def __init__(self, parent, product_repository):
        super().__init__(parent, bg="#FFFFFF", padx=20, pady=20)   # parent must be positional
        self.product_repository = product_repository
        self._build_inventory()
        self._render_inventory()

    """ Inventory View """
    def _build_inventory(self):
        inventory_container = tk.Frame(self, bg="#F8FAFC", padx=10, pady=10)
        inventory_container.pack(fill="both", expand=True)

        top_bar = tk.Frame(inventory_container, bg="#F8FAFC")
        top_bar.pack(fill="x", pady=(0,10))

        refresh_button = tk.Button(
            top_bar, text="🔄 Refresh Inventory", font=("Segoe UI", 9, "bold"),
            bg="#0284C7", fg="white", activebackground="#0369A1", activeforeground="white",
            relief="flat", cursor="hand2", command=self._render_inventory
        )
        refresh_button.pack(side="left", ipady=4, ipadx=10, padx=(0, 10))

        self.import_btn = tk.Button(
            top_bar, text="📁 Import Delivery CSV", font=("Segoe UI", 9, "bold"),
            bg="#0284C7", fg="white", activebackground="#0369A1", activeforeground="white",
            relief="flat", cursor="hand2", command=self._handle_csv_import
        )
        self.import_btn.pack(side="left", ipady=4, ipadx=10, padx=(10, 10))

        table_frame = tk.Frame(inventory_container, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E2E8F0")
        table_frame.pack(fill="both", expand=True)

        """ Inventory Table Style """
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Inventory.Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=32,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Inventory.Treeview.Heading",
            background="#0F172A",
            foreground="#F8FAFC",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 6)
        )
        style.map(
            "Inventory.Treeview",
            background=[("selected", "#0284C7")],
            foreground=[("selected", "#FFFFFF")]
        )
        style.map(
            "Inventory.Treeview.Heading",
            background=[("active", "#1E293B")]
        )

        columns = ("product_id", "category_id", "name", "brand", "price", "cost_price", 
                    "stock_quantity", "min_stock_level", "size", "description"
        )
        self.inventory_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Inventory.Treeview"
        )

        self.inventory_tree.heading("product_id", text="Product ID")
        self.inventory_tree.heading("category_id", text="Category")
        self.inventory_tree.heading("name", text="Name")
        self.inventory_tree.heading("brand", text="Brand")
        self.inventory_tree.heading("price", text="Price")
        self.inventory_tree.heading("cost_price", text="Cost Price")
        self.inventory_tree.heading("stock_quantity", text="Qty")
        self.inventory_tree.heading("min_stock_level", text="Min Qty")
        self.inventory_tree.heading("size", text="Size")
        self.inventory_tree.heading("description", text="Product Description")

        self.inventory_tree.column("product_id", width=90, anchor="center")
        self.inventory_tree.column("category_id", width=90, anchor="center")
        self.inventory_tree.column("name", width=200, anchor="center")
        self.inventory_tree.column("brand", width=120, anchor="center")
        self.inventory_tree.column("price", width=120, anchor="e")
        self.inventory_tree.column("cost_price", width=120, anchor="e")
        self.inventory_tree.column("stock_quantity", width=90, anchor="e")
        self.inventory_tree.column("min_stock_level", width=90, anchor="e")
        self.inventory_tree.column("size", width=90, anchor="center")
        self.inventory_tree.column("description", width=300, anchor="w")

        self.inventory_tree.tag_configure("odd", background="#F8FAFC")
        self.inventory_tree.tag_configure("even", background="#FFFFFF")
        self.inventory_tree.tag_configure("low_stock", background="#ffcccc", foreground="#990000")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        self.inventory_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._render_inventory()

    """ Fetches Products from the database """
    def _render_inventory(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        products = self.product_repository.get_all()
        for index, product in enumerate(products):
            stock = product.stock_quantity
            min_stock = product.min_stock_level

            is_low_stock = stock <= min_stock

            row_tag = "even" if index % 2 == 0 else "odd"

            if is_low_stock:
                row_tags = ("low_stock",)
            else:
                row_tags = ()

            self.inventory_tree.insert("", "end", values=(
                product.product_id,
                product.category_name,
                product.name,
                product.brand,
                product.price,
                product.cost_price,
                stock,
                min_stock,
                product.size,
                product.description
            ),
            tags=(row_tag,row_tags)
            )



    """ Handles delivery report and updates stock """
    """ So far CSV files only """
    def _handle_csv_import(self):
        """ Open a window to select the CSV file """
        file_path = filedialog.askopenfilename(
            title="Select Delivery CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    product_id = int(row['product_id'])
                    quantity = int(row['quantity'])
                    self.product_repository.update_stock(product_id, quantity_delta=quantity)
                    count += 1
            
            if count == 0:
                messagebox.showwarning("Empty File", "The selected CSV file contains no data.")
                return

            messagebox.showinfo("Success", f"Successfully imported deliveries for {count} products!")
            self._render_inventory()

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to process CSV file:\n{str(e)}")


    