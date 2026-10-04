import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from domain.entities.customer import Customer
from domain.entities.product import Product
from domain.entities.supplier import Supplier
from presentation.cli.context import CLIContext


class GUIApplication:
    def __init__(self, root: tk.Tk, context: CLIContext) -> None:
        self.root = root
        self.context = context
        self.root.title("Python Business Management System")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)

        self._build_layout()
        self.show_view("Dashboard")
        self.root.after_idle(self._refresh_initial_layout)

    def _build_layout(self) -> None:
        self.sidebar = ttk.Frame(self.root, padding=10)
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self.root, padding=20)
        self.content.pack(side="right", fill="both", expand=True)

        navigation_items = [
            "Dashboard",
            "Products",
            "Inventory",
            "Sales",
            "Customers",
            "Suppliers",
            "Invoices",
            "Reports",
        ]

        for item in navigation_items:
            button = ttk.Button(
                self.sidebar,
                text=item,
                command=lambda name=item: self.show_view(name),
                width=18,
            )
            button.pack(fill="x", pady=3)

    def _refresh_initial_layout(self) -> None:
        self.root.update_idletasks()
        self.content.update_idletasks()

    def show_view(self, name: str) -> None:
        for widget in self.content.winfo_children():
            widget.destroy()

        if name == "Dashboard":
            self._show_dashboard()
            return

        if name == "Products":
            self._show_products()
            return

        if name == "Inventory":
            self._show_inventory()
            self.root.after_idle(self._refresh_initial_layout)
            return

        if name == "Customers":
            self._show_customers()
            return

        if name == "Suppliers":
            self._show_suppliers()
            return

        title = ttk.Label(
            self.content,
            text=name,
            font=("TkDefaultFont", 20, "bold"),
        )
        title.pack(anchor="w", pady=(0, 10))

        description = ttk.Label(
            self.content,
            text=f"{name} screen",
        )
        description.pack(anchor="w")

    def _show_dashboard(self) -> None:
        title = ttk.Label(
            self.content,
            text="Dashboard",
            font=("TkDefaultFont", 20, "bold"),
        )
        title.pack(anchor="w", pady=(0, 20))

        summary = self.context.reporting_service.get_business_summary()
        sales_total = self.context.reporting_service.get_sales_total()

        cards = ttk.Frame(self.content)
        cards.pack(fill="x")

        metrics = [
            ("Products", summary["product_count"]),
            ("Customers", summary["customer_count"]),
            ("Suppliers", summary["supplier_count"]),
            ("Sales", summary["sale_count"]),
            ("Invoices", summary["invoice_count"]),
            ("Total Sales", f"{sales_total:.2f}"),
        ]

        for label, value in metrics:
            card = ttk.LabelFrame(cards, text=label, padding=15)
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5,
            )

            value_label = ttk.Label(
                card,
                text=str(value),
                font=("TkDefaultFont", 16, "bold"),
            )
            value_label.pack()

    def _show_products(self) -> None:
        title = ttk.Label(
            self.content,
            text="Products",
            font=("TkDefaultFont", 20, "bold"),
        )
        title.pack(anchor="w", pady=(0, 15))

        form = ttk.LabelFrame(
            self.content,
            text="Add Product",
            padding=10,
        )
        form.pack(fill="x", pady=(0, 15))

        ttk.Label(
            form,
            text="Name",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        name_entry = ttk.Entry(form, width=25)
        name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Description",
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        description_entry = ttk.Entry(form, width=25)
        description_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="SKU",
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        sku_entry = ttk.Entry(form, width=25)
        sku_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Price",
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        price_entry = ttk.Entry(form, width=25)
        price_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Quantity",
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        quantity_entry = ttk.Entry(form, width=25)
        quantity_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
        )

        button_frame = ttk.Frame(form)
        button_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="e",
        )

        product_list = ttk.Treeview(
            self.content,
            columns=(
                "id",
                "name",
                "description",
                "sku",
                "price",
                "quantity",
            ),
            show="headings",
            height=12,
        )

        product_list.heading("id", text="ID")
        product_list.heading("name", text="Name")
        product_list.heading("description", text="Description")
        product_list.heading("sku", text="SKU")
        product_list.heading("price", text="Price")
        product_list.heading("quantity", text="Quantity")

        product_list.column(
            "id",
            width=60,
            anchor="center",
            stretch=False,
        )

        product_list.column(
            "name",
            width=180,
            anchor="w",
        )

        product_list.column(
            "description",
            width=260,
            anchor="w",
        )

        product_list.column(
            "sku",
            width=130,
            anchor="w",
        )

        product_list.column(
            "price",
            width=120,
            anchor="w",
        )

        product_list.column(
            "quantity",
            width=100,
            anchor="center",
        )

        product_list.pack(
            fill="both",
            expand=True,
            pady=(5, 0),
        )

        def load_products() -> None:
            for item in product_list.get_children():
                product_list.delete(item)

            products = self.context.product_service.get_products()

            for product in products:
                product_list.insert(
                    "",
                    "end",
                    values=(
                        product.id,
                        product.name,
                        product.description or "",
                        product.sku,
                        f"{product.price:.2f}",
                        product.quantity,
                    ),
                )

        def clear_form() -> None:
            name_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)
            sku_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)

        def add_product() -> None:
            try:
                product = Product(
                    id=None,
                    name=name_entry.get(),
                    description=description_entry.get() or None,
                    sku=sku_entry.get(),
                    price=float(price_entry.get()),
                    quantity=int(quantity_entry.get()),
                    created_at=datetime.now().isoformat(
                        timespec="seconds"
                    ),
                )

                self.context.product_service.add_product(product)
                clear_form()
                load_products()

                messagebox.showinfo(
                    "Success",
                    "Product added successfully.",
                )

            except (ValueError, TypeError) as exc:
                messagebox.showerror(
                    "Invalid Input",
                    str(exc),
                )

        def delete_product() -> None:
            selected = product_list.selection()

            if not selected:
                messagebox.showwarning(
                    "Delete Product",
                    "Select a product first.",
                )
                return

            values = product_list.item(
                selected[0],
                "values",
            )

            product_id = int(values[0])

            self.context.product_service.delete_product(product_id)
            load_products()

            messagebox.showinfo(
                "Success",
                "Product deleted successfully.",
            )

        ttk.Button(
            button_frame,
            text="Add Product",
            command=add_product,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_product,
        ).pack(
            side="left",
            padx=5,
        )

        load_products()

    def _show_inventory(self) -> None:
        selected_product_id = {"value": None}
        selected_product_name = {"value": None}

        products_cache = []
        stock_sort_state = {
            "column": "id",
            "descending": False,
        }
        history_sort_state = {
            "column": "created_at",
            "descending": True,
        }
        current_movements = []

        # -----------------------------
        # Common heading style
        # -----------------------------

        tree_heading_style = ttk.Style()
        tree_heading_style.configure(
            "Inventory.Treeview.Heading",
            font=("TkDefaultFont", 10, "bold"),
        )
        # -----------------------------
        # Top Bar
        # Stock Operations = LEFT
        # Search = RIGHT
        # -----------------------------

        top_bar = ttk.Frame(self.content)
        top_bar.pack(
            fill="x",
            pady=(0, 10),
        )

        operation_frame = ttk.LabelFrame(
            top_bar,
            text="Stock Operations",
            padding=8,
        )
        operation_frame.pack(
            side="left",
            fill="y",
        )

        search_frame = ttk.LabelFrame(
            top_bar,
            text="Search",
            padding=8,
        )
        search_frame.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(10, 0),
        )

        search_var = tk.StringVar()
        search_placeholder = "Search by ID, Product Name or Product Code"
        search_placeholder_active = {"value": True}

        search_entry = ttk.Entry(
            search_frame,
            textvariable=search_var,
        )
        search_entry.pack(
            side="right",
            fill="x",
            expand=True,
        )

        search_entry.insert(
            0,
            search_placeholder,
        )
        search_entry.configure(
            foreground="gray",
        )

        def clear_search_placeholder(event=None) -> None:
            if search_placeholder_active["value"]:
                search_entry.delete(0, tk.END)
                search_entry.configure(foreground="black")
                search_placeholder_active["value"] = False

        def restore_search_placeholder(event=None) -> None:
            if not search_entry.get().strip():
                search_entry.insert(0, search_placeholder)
                search_entry.configure(foreground="gray")
                search_placeholder_active["value"] = True

        search_entry.bind(
            "<FocusIn>",
            clear_search_placeholder,
        )
        search_entry.bind(
            "<FocusOut>",
            restore_search_placeholder,
        )

        # -----------------------------
        # Inventory Table
        # Fixed-height frame keeps the
        # scrollbar clearly visible.
        # -----------------------------

        inventory_frame = ttk.LabelFrame(
            self.content,
            text="Inventory",
            padding=10,
        )
        inventory_frame.pack(
            fill="x",
            expand=False,
        )

        stock_table_frame = ttk.Frame(
            inventory_frame,
            height=300,
        )
        stock_table_frame.pack(
            fill="x",
            expand=False,
        )
        stock_table_frame.pack_propagate(False)

        stock_list = ttk.Treeview(
            stock_table_frame,
            columns=(
                "id",
                "name",
                "product_code",
                "quantity",
                "unit_price",
                "total_stock_price",
            ),
            show="headings",
            height=10,
            style="Inventory.Treeview",
        )

        stock_list.heading(
            "id",
            text="ID",
            command=lambda: sort_stock("id"),
        )
        stock_list.heading(
            "name",
            text="Product",
            command=lambda: sort_stock("name"),
        )
        stock_list.heading(
            "product_code",
            text="Product Code",
            command=lambda: sort_stock("product_code"),
        )
        stock_list.heading(
            "quantity",
            text="Quantity/unit",
            command=lambda: sort_stock("quantity"),
        )
        stock_list.heading(
            "unit_price",
            text="Per Unit Price",
            command=lambda: sort_stock("unit_price"),
        )
        stock_list.heading(
            "total_stock_price",
            text="Total Stock Price",
            command=lambda: sort_stock("total_stock_price"),
        )

        stock_list.column(
            "id",
            width=70,
            anchor="center",
            stretch=False,
        )
        stock_list.column(
            "name",
            width=220,
            anchor="center",
        )
        stock_list.column(
            "product_code",
            width=180,
            anchor="center",
        )
        stock_list.column(
            "quantity",
            width=140,
            anchor="center",
        )
        stock_list.column(
            "unit_price",
            width=150,
            anchor="center",
        )
        stock_list.column(
            "total_stock_price",
            width=170,
            anchor="center",
        )

        def resize_stock_columns(event=None) -> None:
            available_width = max(stock_list.winfo_width() - 2, 1)
            widths = {
                "id": 0.08,
                "name": 0.22,
                "product_code": 0.18,
                "quantity": 0.13,
                "unit_price": 0.17,
                "total_stock_price": 0.22,
            }
            for column, ratio in widths.items():
                stock_list.column(
                    column,
                    width=max(1, int(available_width * ratio)),
                )

        stock_list.bind("<Configure>", resize_stock_columns)

        stock_scrollbar = ttk.Scrollbar(
            stock_table_frame,
            orient="vertical",
            command=stock_list.yview,
        )

        stock_list.configure(
            yscrollcommand=stock_scrollbar.set,
        )

        stock_list.pack(
            side="left",
            fill="both",
            expand=True,
        )

        stock_scrollbar.pack(
            side="right",
            fill="y",
        )

        # -----------------------------
        # Movement History
        # -----------------------------

        history_frame = ttk.LabelFrame(
            self.content,
            text="Movement History",
            padding=10,
        )
        history_frame.pack(
            fill="x",
            pady=(10, 0),
        )

        history_selection_label = ttk.Label(
            history_frame,
            text="Select a product to view movement history.",
        )
        history_selection_label.pack(
            anchor="w",
            pady=(0, 5),
        )

        history_table_frame = ttk.Frame(
            history_frame,
            height=150,
        )
        history_table_frame.pack(
            fill="x",
            expand=False,
        )
        history_table_frame.pack_propagate(False)

        history_list = ttk.Treeview(
            history_table_frame,
            columns=(
                "type",
                "quantity",
                "resulting_stock",
                "created_at",
            ),
            show="headings",
            height=5,
            style="Inventory.Treeview",
        )

        history_list.heading(
            "type",
            text="Type",
            command=lambda: sort_history("type"),
        )
        history_list.heading(
            "quantity",
            text="Quantity",
            command=lambda: sort_history("quantity"),
        )
        history_list.heading(
            "resulting_stock",
            text="Resulting Stock",
            command=lambda: sort_history("resulting_stock"),
        )
        history_list.heading(
            "created_at",
            text="Created At",
            command=lambda: sort_history("created_at"),
        )

        history_list.column(
            "type",
            width=110,
            anchor="center",
        )
        history_list.column(
            "quantity",
            width=110,
            anchor="center",
        )
        history_list.column(
            "resulting_stock",
            width=140,
            anchor="center",
        )
        history_list.column(
            "created_at",
            width=280,
            anchor="center",
        )

        def resize_history_columns(event=None) -> None:
            available_width = max(history_list.winfo_width() - 2, 1)
            widths = {
                "type": 0.20,
                "quantity": 0.20,
                "resulting_stock": 0.25,
                "created_at": 0.35,
            }
            for column, ratio in widths.items():
                history_list.column(
                    column,
                    width=max(1, int(available_width * ratio)),
                )

        history_list.bind("<Configure>", resize_history_columns)

        history_scrollbar = ttk.Scrollbar(
            history_table_frame,
            orient="vertical",
            command=history_list.yview,
        )

        history_list.configure(
            yscrollcommand=history_scrollbar.set,
        )

        history_list.pack(
            side="left",
            fill="both",
            expand=True,
        )

        history_scrollbar.pack(
            side="right",
            fill="y",
        )

        def format_created_at(value: str) -> str:
            try:
                parsed = datetime.fromisoformat(value)
                return parsed.strftime(
                    "%Y-%m-%d        %H:%M:%S"
                )
            except ValueError:
                return value.replace(
                    "T",
                    "        ",
                    1,
                )

        def clear_history() -> None:
            for item in history_list.get_children():
                history_list.delete(item)

        def history_sort_key(
            movement,
            column: str,
        ):
            if column == "type":
                return movement.movement_type.value

            if column == "quantity":
                return movement.quantity

            if column == "resulting_stock":
                return movement.resulting_stock

            return movement.created_at

        def update_history_headings() -> None:
            arrows = {
                "type": "",
                "quantity": "",
                "resulting_stock": "",
                "created_at": "",
            }

            arrows[
                history_sort_state["column"]
            ] = (
                " ▼"
                if history_sort_state["descending"]
                else " ▲"
            )

            history_list.heading(
                "type",
                text=f"Type{arrows['type']}",
            )
            history_list.heading(
                "quantity",
                text=f"Quantity{arrows['quantity']}",
            )
            history_list.heading(
                "resulting_stock",
                text=(
                    "Resulting Stock"
                    f"{arrows['resulting_stock']}"
                ),
            )
            history_list.heading(
                "created_at",
                text=(
                    "Created At"
                    f"{arrows['created_at']}"
                ),
            )

        def render_history() -> None:
            clear_history()

            sorted_movements = sorted(
                current_movements,
                key=lambda movement: history_sort_key(
                    movement,
                    history_sort_state["column"],
                ),
                reverse=history_sort_state["descending"],
            )

            for movement in sorted_movements:
                history_list.insert(
                    "",
                    "end",
                    values=(
                        movement.movement_type.value,
                        movement.quantity,
                        movement.resulting_stock,
                        format_created_at(
                            movement.created_at
                        ),
                    ),
                )

            update_history_headings()

        def sort_history(column: str) -> None:
            if history_sort_state["column"] == column:
                history_sort_state["descending"] = (
                    not history_sort_state["descending"]
                )
            else:
                history_sort_state["column"] = column
                history_sort_state["descending"] = False

            render_history()

        def load_history(
            product_id: int,
            product_name: str,
        ) -> None:
            nonlocal current_movements

            current_movements = list(
                self.context.inventory_service.get_movement_history(
                    product_id
                )
            )

            history_sort_state["column"] = "created_at"
            history_sort_state["descending"] = True

            history_selection_label.config(
                text=f"Movement history for : {product_name}"
            )

            if not current_movements:
                clear_history()

                history_selection_label.config(
                    text=(
                        f"Movement history for : {product_name} — "
                        "No movement history found for this product."
                    )
                )

                update_history_headings()
                return

            render_history()

        # -----------------------------
        # Inventory Sorting
        # -----------------------------

        def stock_sort_key(
            product,
            column: str,
        ):
            if column == "id":
                return product.id or 0

            if column == "name":
                return product.name.lower()

            if column == "product_code":
                return product.sku.lower()

            if column == "quantity":
                return product.quantity

            if column == "unit_price":
                return product.price

            return product.price * product.quantity

        def update_stock_headings() -> None:
            arrows = {
                "id": "",
                "name": "",
                "product_code": "",
                "quantity": "",
                "unit_price": "",
                "total_stock_price": "",
            }

            arrows[
                stock_sort_state["column"]
            ] = (
                " ▼"
                if stock_sort_state["descending"]
                else " ▲"
            )

            stock_list.heading(
                "id",
                text=f"ID{arrows['id']}",
            )
            stock_list.heading(
                "name",
                text=f"Product{arrows['name']}",
            )
            stock_list.heading(
                "product_code",
                text=(
                    "Product Code"
                    f"{arrows['product_code']}"
                ),
            )
            stock_list.heading(
                "quantity",
                text=(
                    "Quantity/unit"
                    f"{arrows['quantity']}"
                ),
            )
            stock_list.heading(
                "unit_price",
                text=(
                    "Per Unit Price"
                    f"{arrows['unit_price']}"
                ),
            )
            stock_list.heading(
                "total_stock_price",
                text=(
                    "Total Stock Price"
                    f"{arrows['total_stock_price']}"
                ),
            )

        def sort_stock(column: str) -> None:
            if stock_sort_state["column"] == column:
                stock_sort_state["descending"] = (
                    not stock_sort_state["descending"]
                )
            else:
                stock_sort_state["column"] = column
                stock_sort_state["descending"] = False

            render_stock()

        def render_stock() -> None:
            for item in stock_list.get_children():
                stock_list.delete(item)

            search_text = search_var.get().strip().lower()

            if (
                search_placeholder_active["value"]
                or search_text == search_placeholder.lower()
            ):
                search_text = ""

            filtered_products = []

            for product in products_cache:
                product_id = str(
                    product.id or ""
                ).lower()
                product_name = product.name.lower()
                product_code = product.sku.lower()

                if (
                    not search_text
                    or search_text in product_id
                    or search_text in product_name
                    or search_text in product_code
                ):
                    filtered_products.append(product)

            filtered_products.sort(
                key=lambda product: stock_sort_key(
                    product,
                    stock_sort_state["column"],
                ),
                reverse=stock_sort_state["descending"],
            )

            for product in filtered_products:
                total_stock_price = (
                    product.price * product.quantity
                )

                stock_list.insert(
                    "",
                    "end",
                    values=(
                        product.id,
                        product.name,
                        product.sku,
                        product.quantity,
                        f"₹ {product.price:,.2f}",
                        f"₹ {total_stock_price:,.2f}",
                    ),
                )

            update_stock_headings()

        def load_stock() -> None:
            nonlocal products_cache

            products_cache = (
                self.context.inventory_service.get_stock()
            )

            render_stock()

            selected_product_id["value"] = None
            selected_product_name["value"] = None

            clear_history()

            history_selection_label.config(
                text="Select a product to view movement history."
            )

        # -----------------------------
        # Product Selection
        # -----------------------------

        def select_product(event=None) -> None:
            selected = stock_list.selection()

            if not selected:
                selected_product_id["value"] = None
                selected_product_name["value"] = None

                clear_history()

                history_selection_label.config(
                    text="Select a product to view movement history."
                )
                return

            values = stock_list.item(
                selected[0],
                "values",
            )

            selected_product_id["value"] = int(
                values[0]
            )
            selected_product_name["value"] = values[1]

            load_history(
                selected_product_id["value"],
                selected_product_name["value"],
            )

        # -----------------------------
        # Stock Operation Dialog
        # -----------------------------

        def run_stock_operation(
            operation: str,
        ) -> None:
            if selected_product_id["value"] is None:
                messagebox.showwarning(
                    "Select Product",
                    (
                        "Please select a product before "
                        "using a stock operation."
                    ),
                )
                return

            product_id = selected_product_id["value"]
            product_name = selected_product_name["value"]

            dialog = tk.Toplevel(self.root)
            dialog.title(operation)
            dialog.geometry("430x250")
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(
                dialog,
                text=operation,
                font=("TkDefaultFont", 16, "bold"),
            ).pack(
                anchor="w",
                padx=20,
                pady=(20, 5),
            )

            ttk.Label(
                dialog,
                text=f"Product: {product_name}",
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 15),
            )

            if operation == "Adjust Stock":
                field_label = "New Stock Quantity"
                help_text = (
                    "Enter the new total stock quantity."
                )
            else:
                field_label = "Quantity"
                help_text = (
                    "Enter a whole number greater than zero."
                )

            ttk.Label(
                dialog,
                text=field_label,
            ).pack(
                anchor="w",
                padx=20,
            )

            quantity_var = tk.StringVar()

            def validate_quantity(value: str) -> bool:
                return value == "" or value.isdigit()

            validate_command = dialog.register(
                validate_quantity
            )

            quantity_entry = ttk.Entry(
                dialog,
                textvariable=quantity_var,
                validate="key",
                validatecommand=(
                    validate_command,
                    "%P",
                ),
            )

            quantity_entry.pack(
                fill="x",
                padx=20,
                pady=(5, 5),
            )

            ttk.Label(
                dialog,
                text=help_text,
            ).pack(
                anchor="w",
                padx=20,
            )

            def submit() -> None:
                raw_quantity = quantity_var.get().strip()

                if not raw_quantity:
                    messagebox.showwarning(
                        "Quantity Required",
                        "Please enter a quantity.",
                        parent=dialog,
                    )
                    quantity_entry.focus_set()
                    return

                quantity = int(raw_quantity)

                if operation == "Adjust Stock":
                    if quantity < 0:
                        messagebox.showwarning(
                            "Invalid Quantity",
                            (
                                "New stock quantity "
                                "cannot be negative."
                            ),
                            parent=dialog,
                        )
                        return

                elif quantity <= 0:
                    messagebox.showwarning(
                        "Invalid Quantity",
                        "Quantity must be greater than zero.",
                        parent=dialog,
                    )
                    return

                try:
                    created_at = datetime.now().isoformat(
                        timespec="seconds"
                    )

                    if operation == "Stock In":
                        self.context.inventory_service.stock_in(
                            product_id,
                            quantity,
                            created_at,
                        )

                    elif operation == "Stock Out":
                        self.context.inventory_service.stock_out(
                            product_id,
                            quantity,
                            created_at,
                        )

                    else:
                        self.context.inventory_service.adjust_stock(
                            product_id,
                            quantity,
                            created_at,
                        )

                    dialog.destroy()

                    load_stock()

                    for item in stock_list.get_children():
                        values = stock_list.item(
                            item,
                            "values",
                        )

                        if int(values[0]) == product_id:
                            stock_list.selection_set(item)
                            stock_list.focus(item)
                            stock_list.see(item)

                            selected_product_id[
                                "value"
                            ] = product_id

                            selected_product_name[
                                "value"
                            ] = values[1]

                            load_history(
                                product_id,
                                values[1],
                            )

                            break

                    messagebox.showinfo(
                        "Success",
                        (
                            f"{operation} "
                            "completed successfully."
                        ),
                    )

                except ValueError as exc:
                    messagebox.showwarning(
                        "Unable to Complete Operation",
                        str(exc),
                        parent=dialog,
                    )

            button_frame = ttk.Frame(dialog)
            button_frame.pack(
                fill="x",
                padx=20,
                pady=20,
            )

            ttk.Button(
                button_frame,
                text="Save",
                command=submit,
            ).pack(
                side="left",
                padx=(0, 8),
            )

            ttk.Button(
                button_frame,
                text="Cancel",
                command=dialog.destroy,
            ).pack(
                side="left",
            )

            quantity_entry.focus_set()

        def stock_in() -> None:
            run_stock_operation("Stock In")

        def stock_out() -> None:
            run_stock_operation("Stock Out")

        def adjust_stock() -> None:
            run_stock_operation("Adjust Stock")

        # -----------------------------
        # Main Screen Operations
        # -----------------------------

        ttk.Button(
            operation_frame,
            text="Stock In",
            command=stock_in,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            operation_frame,
            text="Stock Out",
            command=stock_out,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            operation_frame,
            text="Adjust Stock",
            command=adjust_stock,
        ).pack(
            side="left",
            padx=5,
        )

        # -----------------------------
        # Double Click Product Popup
        # -----------------------------

        def show_product_popup(event=None) -> None:
            row_id = (
                stock_list.identify_row(event.y)
                if event
                else ""
            )

            if not row_id:
                return

            stock_list.selection_set(row_id)
            stock_list.focus(row_id)

            values = stock_list.item(
                row_id,
                "values",
            )

            if not values:
                return

            product_id = values[0]
            product_name = values[1]
            product_code = values[2]
            quantity = values[3]
            unit_price = values[4]
            total_stock_price = values[5]

            popup = tk.Toplevel(self.root)
            popup.title("Product Details")
            popup.geometry("540x470")
            popup.minsize(540, 470)
            popup.resizable(False, False)
            popup.transient(self.root)
            popup.grab_set()

            ttk.Label(
                popup,
                text="Product Details",
                font=("TkDefaultFont", 18, "bold"),
            ).pack(
                anchor="w",
                padx=20,
                pady=(20, 15),
            )

            details_frame = ttk.LabelFrame(
                popup,
                text="Product Information",
                padding=15,
            )
            details_frame.pack(
                fill="x",
                padx=20,
                pady=(0, 15),
            )

            details = [
                ("Product ID", product_id),
                ("Product", product_name),
                ("Product Code", product_code),
                ("Quantity/unit", quantity),
                ("Per Unit Price", unit_price),
                ("Total Stock Price", total_stock_price),
            ]

            for row, (label, value) in enumerate(
                details
            ):
                ttk.Label(
                    details_frame,
                    text=f"{label}:",
                    font=("TkDefaultFont", 10, "bold"),
                ).grid(
                    row=row,
                    column=0,
                    sticky="w",
                    padx=5,
                    pady=4,
                )

                ttk.Label(
                    details_frame,
                    text=str(value),
                ).grid(
                    row=row,
                    column=1,
                    sticky="w",
                    padx=15,
                    pady=4,
                )

            popup_operation_frame = ttk.LabelFrame(
                popup,
                text="Stock Operations",
                padding=15,
            )
            popup_operation_frame.pack(
                fill="x",
                padx=20,
                pady=(0, 15),
            )

            ttk.Button(
                popup_operation_frame,
                text="Stock In",
                command=stock_in,
            ).pack(
                fill="x",
                pady=4,
            )

            ttk.Button(
                popup_operation_frame,
                text="Stock Out",
                command=stock_out,
            ).pack(
                fill="x",
                pady=4,
            )

            ttk.Button(
                popup_operation_frame,
                text="Adjust Stock",
                command=adjust_stock,
            ).pack(
                fill="x",
                pady=4,
            )

        search_var.trace_add(
            "write",
            lambda *_: render_stock(),
        )

        stock_list.bind(
            "<<TreeviewSelect>>",
            select_product,
        )

        stock_list.bind(
            "<Double-1>",
            show_product_popup,
        )

        load_stock()


    def _show_customers(self) -> None:
        title = ttk.Label(
            self.content,
            text="Customers",
            font=("TkDefaultFont", 20, "bold"),
        )
        title.pack(anchor="w", pady=(0, 15))

        form = ttk.LabelFrame(
            self.content,
            text="Add Customer",
            padding=10,
        )
        form.pack(fill="x", pady=(0, 15))

        ttk.Label(
            form,
            text="Name",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        name_entry = ttk.Entry(form, width=25)
        name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Phone",
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        phone_entry = ttk.Entry(form, width=25)
        phone_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Email",
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        email_entry = ttk.Entry(form, width=25)
        email_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Address",
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        address_entry = ttk.Entry(form, width=25)
        address_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
        )

        button_frame = ttk.Frame(form)
        button_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="e",
        )

        customer_list = ttk.Treeview(
            self.content,
            columns=(
                "id",
                "name",
                "phone",
                "email",
                "address",
            ),
            show="headings",
            height=12,
        )

        customer_list.heading("id", text="ID")
        customer_list.heading("name", text="Name")
        customer_list.heading("phone", text="Phone")
        customer_list.heading("email", text="Email")
        customer_list.heading("address", text="Address")

        customer_list.column(
            "id",
            width=60,
            anchor="center",
            stretch=False,
        )

        customer_list.column(
            "name",
            width=180,
            anchor="w",
        )

        customer_list.column(
            "phone",
            width=140,
            anchor="w",
        )

        customer_list.column(
            "email",
            width=220,
            anchor="w",
        )

        customer_list.column(
            "address",
            width=260,
            anchor="w",
        )

        customer_list.pack(
            fill="both",
            expand=True,
            pady=(5, 0),
        )

        def load_customers() -> None:
            for item in customer_list.get_children():
                customer_list.delete(item)

            customers = self.context.customer_service.get_customers()

            for customer in customers:
                customer_list.insert(
                    "",
                    "end",
                    values=(
                        customer.id,
                        customer.name,
                        customer.phone or "",
                        customer.email or "",
                        customer.address or "",
                    ),
                )

        def clear_form() -> None:
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)

        def add_customer() -> None:
            try:
                customer = Customer(
                    id=None,
                    name=name_entry.get(),
                    phone=phone_entry.get() or None,
                    email=email_entry.get() or None,
                    address=address_entry.get() or None,
                    created_at=datetime.now().isoformat(
                        timespec="seconds"
                    ),
                )

                self.context.customer_service.add_customer(customer)
                clear_form()
                load_customers()

                messagebox.showinfo(
                    "Success",
                    "Customer added successfully.",
                )

            except (ValueError, TypeError) as exc:
                messagebox.showerror(
                    "Invalid Input",
                    str(exc),
                )

        def delete_customer() -> None:
            selected = customer_list.selection()

            if not selected:
                messagebox.showwarning(
                    "Delete Customer",
                    "Select a customer first.",
                )
                return

            values = customer_list.item(
                selected[0],
                "values",
            )

            customer_id = int(values[0])

            self.context.customer_service.delete_customer(customer_id)
            load_customers()

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully.",
            )

        ttk.Button(
            button_frame,
            text="Add Customer",
            command=add_customer,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_customer,
        ).pack(
            side="left",
            padx=5,
        )

        load_customers()

    def _show_suppliers(self) -> None:
        title = ttk.Label(
            self.content,
            text="Suppliers",
            font=("TkDefaultFont", 20, "bold"),
        )
        title.pack(anchor="w", pady=(0, 15))

        form = ttk.LabelFrame(
            self.content,
            text="Add Supplier",
            padding=10,
        )
        form.pack(fill="x", pady=(0, 15))

        ttk.Label(
            form,
            text="Name",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        name_entry = ttk.Entry(form, width=25)
        name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Phone",
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        phone_entry = ttk.Entry(form, width=25)
        phone_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Email",
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )

        email_entry = ttk.Entry(form, width=25)
        email_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Address",
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        address_entry = ttk.Entry(form, width=25)
        address_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
        )

        button_frame = ttk.Frame(form)
        button_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="e",
        )

        supplier_list = ttk.Treeview(
            self.content,
            columns=(
                "id",
                "name",
                "phone",
                "email",
                "address",
            ),
            show="headings",
            height=12,
        )

        supplier_list.heading("id", text="ID")
        supplier_list.heading("name", text="Name")
        supplier_list.heading("phone", text="Phone")
        supplier_list.heading("email", text="Email")
        supplier_list.heading("address", text="Address")

        supplier_list.column(
            "id",
            width=60,
            anchor="center",
            stretch=False,
        )

        supplier_list.column(
            "name",
            width=180,
            anchor="w",
        )

        supplier_list.column(
            "phone",
            width=140,
            anchor="w",
        )

        supplier_list.column(
            "email",
            width=220,
            anchor="w",
        )

        supplier_list.column(
            "address",
            width=260,
            anchor="w",
        )

        supplier_list.pack(
            fill="both",
            expand=True,
            pady=(5, 0),
        )

        def load_suppliers() -> None:
            for item in supplier_list.get_children():
                supplier_list.delete(item)

            suppliers = self.context.supplier_service.get_suppliers()

            for supplier in suppliers:
                supplier_list.insert(
                    "",
                    "end",
                    values=(
                        supplier.id,
                        supplier.name,
                        supplier.phone or "",
                        supplier.email or "",
                        supplier.address or "",
                    ),
                )

        def clear_form() -> None:
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)

        def add_supplier() -> None:
            try:
                supplier = Supplier(
                    id=None,
                    name=name_entry.get(),
                    phone=phone_entry.get() or None,
                    email=email_entry.get() or None,
                    address=address_entry.get() or None,
                    created_at=datetime.now().isoformat(
                        timespec="seconds"
                    ),
                )

                self.context.supplier_service.add_supplier(supplier)
                clear_form()
                load_suppliers()

                messagebox.showinfo(
                    "Success",
                    "Supplier added successfully.",
                )

            except (ValueError, TypeError) as exc:
                messagebox.showerror(
                    "Invalid Input",
                    str(exc),
                )

        def delete_supplier() -> None:
            selected = supplier_list.selection()

            if not selected:
                messagebox.showwarning(
                    "Delete Supplier",
                    "Select a supplier first.",
                )
                return

            values = supplier_list.item(
                selected[0],
                "values",
            )

            supplier_id = int(values[0])

            self.context.supplier_service.delete_supplier(supplier_id)
            load_suppliers()

            messagebox.showinfo(
                "Success",
                "Supplier deleted successfully.",
            )

        ttk.Button(
            button_frame,
            text="Add Supplier",
            command=add_supplier,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_supplier,
        ).pack(
            side="left",
            padx=5,
        )

        load_suppliers()


def main() -> None:
    context = CLIContext()
    root = tk.Tk()

    try:
        GUIApplication(root, context)
        root.mainloop()
    finally:
        context.close()


if __name__ == "__main__":
    main()
