import sqlite3
import math
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from domain.entities.customer import Customer
from domain.entities.product import Product
from domain.entities.supplier import Supplier
from domain.entities.sale import Sale
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

        if name == "Sales":
            self._show_sales()
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
        # Product screen uses its own vertical scroll area because the
        # product table plus both history sections can exceed the window height.
        products_canvas = tk.Canvas(
            self.content,
            highlightthickness=0,
        )
        products_scrollbar = ttk.Scrollbar(
            self.content,
            orient="vertical",
            command=products_canvas.yview,
        )
        products_content = ttk.Frame(products_canvas)

        products_window = products_canvas.create_window(
            (0, 0),
            window=products_content,
            anchor="nw",
        )

        def update_products_scrollregion(event=None) -> None:
            products_canvas.configure(
                scrollregion=products_canvas.bbox("all"),
            )

        def resize_products_content(event) -> None:
            products_canvas.itemconfigure(
                products_window,
                width=event.width,
            )

        products_content.bind(
            "<Configure>",
            update_products_scrollregion,
        )
        products_canvas.bind(
            "<Configure>",
            resize_products_content,
        )
        products_canvas.configure(
            yscrollcommand=products_scrollbar.set,
        )

        products_scrollbar.pack(
            side="right",
            fill="y",
        )
        products_canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        def products_mousewheel(event) -> None:
            products_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units",
            )

        products_canvas.bind(
            "<Enter>",
            lambda event: products_canvas.bind_all(
                "<MouseWheel>",
                products_mousewheel,
            ),
        )
        products_canvas.bind(
            "<Leave>",
            lambda event: products_canvas.unbind_all(
                "<MouseWheel>",
            ),
        )

        selected_product_id = {"value": None}
        products_cache = []
        sort_state = {
            "column": "id",
            "descending": False,
        }
        description_limit = 30

        style = ttk.Style()
        style.configure(
            "Products.Treeview.Heading",
            font=("TkDefaultFont", 10, "bold"),
        )

        top_bar = ttk.Frame(products_content)
        top_bar.pack(
            fill="x",
            pady=(0, 10),
        )

        operation_frame = ttk.LabelFrame(
            top_bar,
            text="Product Operations",
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
                search_placeholder_active["value"] = False
                search_entry.delete(0, tk.END)
                search_entry.configure(foreground="black")
                render_products()

        def restore_search_placeholder(event=None) -> None:
            if not search_entry.get().strip():
                search_placeholder_active["value"] = True
                search_entry.delete(0, tk.END)
                search_entry.insert(0, search_placeholder)
                search_entry.configure(foreground="gray")
                render_products()

        search_entry.bind(
            "<FocusIn>",
            clear_search_placeholder,
        )
        search_entry.bind(
            "<FocusOut>",
            restore_search_placeholder,
        )

        product_frame = ttk.LabelFrame(
            products_content,
            text="Products",
            padding=10,
        )
        product_frame.pack(
            fill="x",
            expand=False,
        )

        table_frame = ttk.Frame(
            product_frame,
            height=300,
        )
        table_frame.pack(
            fill="x",
            expand=False,
        )
        table_frame.pack_propagate(False)

        product_list = ttk.Treeview(
            table_frame,
            columns=(
                "id",
                "name",
                "product_code",
                "quantity",
                "price",
            ),
            show="headings",
            height=10,
            style="Products.Treeview",
        )

        for column, heading in (
            ("id", "ID"),
            ("name", "Name"),
            ("product_code", "Product Code"),
            ("quantity", "Quantity"),
            ("price", "Per Unit Price"),
        ):
            product_list.heading(
                column,
                text=heading,
                command=lambda c=column: sort_products(c),
            )
            product_list.column(
                column,
                width=1,
                anchor="center",
                stretch=True,
            )

        product_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=product_list.yview,
        )
        product_list.configure(
            yscrollcommand=product_scrollbar.set,
        )
        product_list.pack(
            side="left",
            fill="both",
            expand=True,
        )
        product_scrollbar.pack(
            side="right",
            fill="y",
        )

        def resize_product_columns(event=None) -> None:
            available_width = max(
                product_list.winfo_width() - 2,
                1,
            )
            widths = {
                "id": 0.10,
                "name": 0.27,
                "product_code": 0.25,
                "quantity": 0.16,
                "price": 0.22,
            }
            for column, ratio in widths.items():
                product_list.column(
                    column,
                    width=max(1, int(available_width * ratio)),
                )

        product_list.bind(
            "<Configure>",
            resize_product_columns,
        )

        edit_history_frame = ttk.LabelFrame(
            products_content,
            text="Edit History",
            padding=10,
        )
        edit_history_frame.pack(
            fill="x",
            pady=(10, 0),
        )

        edit_history_table_frame = ttk.Frame(
            edit_history_frame,
            height=145,
        )
        edit_history_table_frame.pack(
            fill="x",
        )
        edit_history_table_frame.pack_propagate(False)

        edit_history_list = ttk.Treeview(
            edit_history_table_frame,
            columns=(
                "product",
                "product_code",
                "changed",
                "date",
            ),
            show="headings",
            height=5,
            style="Products.Treeview",
        )

        for column, heading in (
            ("product", "Product"),
            ("product_code", "Product Code"),
            ("changed", "Changed Fields"),
            ("date", "Date / Time"),
        ):
            edit_history_list.heading(
                column,
                text=heading,
                command=lambda c=column: sort_edit_history(c),
            )
            edit_history_list.column(
                column,
                width=1,
                anchor="center",
                stretch=True,
            )

        edit_scrollbar = ttk.Scrollbar(
            edit_history_table_frame,
            orient="vertical",
            command=edit_history_list.yview,
        )
        edit_history_list.configure(
            yscrollcommand=edit_scrollbar.set,
        )
        edit_history_list.pack(
            side="left",
            fill="both",
            expand=True,
        )
        edit_scrollbar.pack(
            side="right",
            fill="y",
        )

        def resize_edit_history_columns(event=None) -> None:
            available_width = max(
                edit_history_list.winfo_width() - 2,
                1,
            )
            widths = {
                "product": 0.23,
                "product_code": 0.23,
                "changed": 0.30,
                "date": 0.24,
            }
            for column, ratio in widths.items():
                edit_history_list.column(
                    column,
                    width=max(1, int(available_width * ratio)),
                )

        edit_history_list.bind(
            "<Configure>",
            resize_edit_history_columns,
        )

        edit_history_sort_state = {
            "column": "date",
            "descending": True,
        }

        def edit_history_sort_key(row, column: str):
            if column == "product":
                return str(row[3] or "").lower()
            if column == "product_code":
                return str(row[4] or "").lower()
            if column == "changed":
                return str(row[5] or "").lower()
            return str(row[6] or "")

        def update_edit_history_headings() -> None:
            arrows = {
                "product": "",
                "product_code": "",
                "changed": "",
                "date": "",
            }
            column = edit_history_sort_state["column"]
            arrows[column] = (
                " ▼"
                if edit_history_sort_state["descending"]
                else " ▲"
            )

            edit_history_list.heading(
                "product",
                text=f"Product{arrows['product']}",
            )
            edit_history_list.heading(
                "product_code",
                text=f"Product Code{arrows['product_code']}",
            )
            edit_history_list.heading(
                "changed",
                text=f"Changed Fields{arrows['changed']}",
            )
            edit_history_list.heading(
                "date",
                text=f"Date / Time{arrows['date']}",
            )

        def sort_edit_history(column: str) -> None:
            if edit_history_sort_state["column"] == column:
                edit_history_sort_state["descending"] = (
                    not edit_history_sort_state["descending"]
                )
            else:
                edit_history_sort_state["column"] = column
                edit_history_sort_state["descending"] = False

            refresh_edit_history()

        add_delete_history_frame = ttk.LabelFrame(
            products_content,
            text="Add / Delete History",
            padding=10,
        )
        add_delete_history_frame.pack(
            fill="x",
            pady=(10, 0),
        )

        add_delete_table_frame = ttk.Frame(
            add_delete_history_frame,
            height=145,
        )
        add_delete_table_frame.pack(
            fill="x",
        )
        add_delete_table_frame.pack_propagate(False)

        add_delete_history_list = ttk.Treeview(
            add_delete_table_frame,
            columns=(
                "action",
                "product",
                "product_code",
                "date",
            ),
            show="headings",
            height=5,
            style="Products.Treeview",
        )

        for column, heading in (
            ("action", "Action"),
            ("product", "Product"),
            ("product_code", "Product Code"),
            ("date", "Date / Time"),
        ):
            add_delete_history_list.heading(
                column,
                text=heading,
                command=lambda c=column: sort_add_delete_history(c),
            )
            add_delete_history_list.column(
                column,
                width=1,
                anchor="center",
                stretch=True,
            )

        add_delete_scrollbar = ttk.Scrollbar(
            add_delete_table_frame,
            orient="vertical",
            command=add_delete_history_list.yview,
        )
        add_delete_history_list.configure(
            yscrollcommand=add_delete_scrollbar.set,
        )
        add_delete_history_list.pack(
            side="left",
            fill="both",
            expand=True,
        )
        add_delete_scrollbar.pack(
            side="right",
            fill="y",
        )

        def resize_add_delete_history_columns(event=None) -> None:
            available_width = max(
                add_delete_history_list.winfo_width() - 2,
                1,
            )
            widths = {
                "action": 0.18,
                "product": 0.30,
                "product_code": 0.27,
                "date": 0.25,
            }
            for column, ratio in widths.items():
                add_delete_history_list.column(
                    column,
                    width=max(1, int(available_width * ratio)),
                )

        add_delete_history_list.bind(
            "<Configure>",
            resize_add_delete_history_columns,
        )

        def format_created_at(value: str) -> str:
            try:
                parsed = datetime.fromisoformat(value)
                return parsed.strftime(
                    "%Y-%m-%d        %H:%M:%S",
                )
            except ValueError:
                return value.replace(
                    "T",
                    "        ",
                    1,
                )

        def clear_edit_history() -> None:
            for item in edit_history_list.get_children():
                edit_history_list.delete(item)

        def refresh_edit_history() -> None:
            clear_edit_history()

            product_id = selected_product_id["value"]
            if product_id is None:
                return

            history = list(
                self.context.product_service.get_edit_history(
                    product_id,
                )
            )
            history.sort(
                key=lambda row: edit_history_sort_key(
                    row,
                    edit_history_sort_state["column"],
                ),
                reverse=edit_history_sort_state["descending"],
            )

            if not history:
                edit_history_list.insert(
                    "",
                    "end",
                    values=(
                        "No edit done",
                        "",
                        "No edit history found for this product.",
                        "",
                    ),
                )
                update_edit_history_headings()
                return

            for row in history:
                edit_history_list.insert(
                    "",
                    "end",
                    values=(
                        row[3],
                        row[4],
                        row[5] or "",
                        format_created_at(row[6]),
                    ),
                )

            update_edit_history_headings()

        add_delete_sort_state = {
            "column": "date",
            "descending": True,
        }

        def add_delete_sort_key(row, column: str):
            if isinstance(row, dict):
                values = (
                    row.get("action", ""),
                    row.get("product_name", ""),
                    row.get("product_code", ""),
                    row.get("created_at", ""),
                )
            else:
                values = (
                    row[2],
                    row[3],
                    row[4],
                    row[6],
                )

            index = {
                "action": 0,
                "product": 1,
                "product_code": 2,
                "date": 3,
            }[column]
            return str(values[index] or "").lower()

        def update_add_delete_headings() -> None:
            arrows = {
                "action": "",
                "product": "",
                "product_code": "",
                "date": "",
            }
            column = add_delete_sort_state["column"]
            arrows[column] = (
                " ▼"
                if add_delete_sort_state["descending"]
                else " ▲"
            )

            add_delete_history_list.heading(
                "action",
                text=f"Action{arrows['action']}",
            )
            add_delete_history_list.heading(
                "product",
                text=f"Product{arrows['product']}",
            )
            add_delete_history_list.heading(
                "product_code",
                text=f"Product Code{arrows['product_code']}",
            )
            add_delete_history_list.heading(
                "date",
                text=f"Date / Time{arrows['date']}",
            )

        def sort_add_delete_history(column: str) -> None:
            if add_delete_sort_state["column"] == column:
                add_delete_sort_state["descending"] = (
                    not add_delete_sort_state["descending"]
                )
            else:
                add_delete_sort_state["column"] = column
                add_delete_sort_state["descending"] = False

            refresh_add_delete_history()

        def refresh_add_delete_history() -> None:
            for item in add_delete_history_list.get_children():
                add_delete_history_list.delete(item)

            service = self.context.product_service

            try:
                history = service.get_add_delete_history()
            except AttributeError:
                history = service.repository.get_product_history()

            def history_created_at(row):
                if isinstance(row, dict):
                    return row.get("created_at", "")
                return row[6]

            history = sorted(
                history,
                key=lambda row: add_delete_sort_key(
                    row,
                    add_delete_sort_state["column"],
                ),
                reverse=add_delete_sort_state["descending"],
            )

            for row in history:
                if isinstance(row, dict):
                    action = row.get("action", "")
                    product_name = row.get("product_name", "")
                    product_code = row.get("product_code", "")
                    created_at = row.get("created_at", "")
                else:
                    action = row[2]
                    product_name = row[3]
                    product_code = row[4]
                    created_at = row[6]

                add_delete_history_list.insert(
                    "",
                    "end",
                    values=(
                        action,
                        product_name,
                        product_code,
                        format_created_at(created_at),
                    ),
                )

            update_add_delete_headings()

        def product_sort_key(product, column: str):
            if column == "id":
                return product.id or 0
            if column == "name":
                return product.name.lower()
            if column == "product_code":
                return product.sku.lower()
            if column == "quantity":
                return product.quantity
            return product.price

        def update_product_headings() -> None:
            arrows = {
                "id": "",
                "name": "",
                "product_code": "",
                "quantity": "",
                "price": "",
            }

            column = sort_state["column"]
            arrows[column] = (
                " ▼"
                if sort_state["descending"]
                else " ▲"
            )

            product_list.heading(
                "id",
                text=f"ID{arrows['id']}",
            )
            product_list.heading(
                "name",
                text=f"Name{arrows['name']}",
            )
            product_list.heading(
                "product_code",
                text=f"Product Code{arrows['product_code']}",
            )
            product_list.heading(
                "quantity",
                text=f"Quantity{arrows['quantity']}",
            )
            product_list.heading(
                "price",
                text=f"Per Unit Price{arrows['price']}",
            )

        def render_products() -> None:
            for item in product_list.get_children():
                product_list.delete(item)

            search_text = search_var.get().strip().lower()

            if (
                search_placeholder_active["value"]
                or search_text == search_placeholder.lower()
            ):
                search_text = ""

            filtered = []

            for product in products_cache:
                if (
                    not search_text
                    or search_text in str(product.id or "").lower()
                    or search_text in product.name.lower()
                    or search_text in product.sku.lower()
                ):
                    filtered.append(product)

            filtered.sort(
                key=lambda product: product_sort_key(
                    product,
                    sort_state["column"],
                ),
                reverse=sort_state["descending"],
            )

            for product in filtered:
                product_list.insert(
                    "",
                    "end",
                    values=(
                        product.id,
                        product.name,
                        product.sku,
                        product.quantity,
                        f"₹ {product.price:,.2f}",
                    ),
                )

            update_product_headings()

        def sort_products(column: str) -> None:
            if sort_state["column"] == column:
                sort_state["descending"] = (
                    not sort_state["descending"]
                )
            else:
                sort_state["column"] = column
                sort_state["descending"] = False

            render_products()

        def load_products() -> None:
            nonlocal products_cache

            products_cache = self.context.product_service.get_products()
            render_products()
            refresh_add_delete_history()
            refresh_edit_history()

        def get_selected_product():
            selected = product_list.selection()
            if not selected:
                return None

            values = product_list.item(
                selected[0],
                "values",
            )
            if not values:
                return None

            product_id = int(values[0])

            return next(
                (
                    product
                    for product in products_cache
                    if product.id == product_id
                ),
                None,
            )

        def validate_description(value: str) -> bool:
            return len(value) <= description_limit

        def valid_product_code(value: str) -> bool:
            return bool(value) and (
                "A" <= value[0] <= "Z"
                or "a" <= value[0] <= "z"
            )

        def product_code_warning(parent) -> None:
            messagebox.showwarning(
                "Invalid Product Code",
                (
                    "Product Code must start with an alphabetic letter "
                    "(A-Z or a-z).\n\n"
                    "Examples: P001, A123, product-01"
                ),
                parent=parent,
            )

        def add_product() -> None:
            dialog = tk.Toplevel(self.root)
            dialog.title("Add Product")
            dialog.geometry("500x430")
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(
                dialog,
                text="Add Product",
                font=("TkDefaultFont", 18, "bold"),
            ).pack(
                anchor="w",
                padx=20,
                pady=(20, 15),
            )

            form = ttk.LabelFrame(
                dialog,
                text="Product Information",
                padding=15,
            )
            form.pack(
                fill="x",
                padx=20,
            )

            entries = {}
            fields = (
                ("Name", 0),
                ("Description", 1),
                ("Product Code", 2),
                ("Per Unit Price", 3),
                ("Quantity", 4),
            )

            for label, row in fields:
                ttk.Label(
                    form,
                    text=label,
                    font=("TkDefaultFont", 10, "bold"),
                ).grid(
                    row=row,
                    column=0,
                    sticky="w",
                    padx=5,
                    pady=6,
                )

                entry = ttk.Entry(
                    form,
                    width=38,
                )
                entry.grid(
                    row=row,
                    column=1,
                    sticky="ew",
                    padx=10,
                    pady=6,
                )
                entries[label] = entry

            description_validate = dialog.register(
                validate_description,
            )
            entries["Description"].configure(
                validate="key",
                validatecommand=(
                    description_validate,
                    "%P",
                ),
            )

            quantity_validate = dialog.register(
                lambda value: value == "" or value.isdigit(),
            )
            entries["Quantity"].configure(
                validate="key",
                validatecommand=(
                    quantity_validate,
                    "%P",
                ),
            )

            def submit() -> None:
                name = entries["Name"].get().strip()
                description = entries["Description"].get().strip()
                product_code = entries["Product Code"].get().strip()
                price_text = entries["Per Unit Price"].get().strip()
                quantity_text = entries["Quantity"].get().strip()

                if not name:
                    messagebox.showwarning(
                        "Invalid Product",
                        "Product name is required.",
                        parent=dialog,
                    )
                    return

                if not valid_product_code(product_code):
                    product_code_warning(dialog)
                    return

                try:
                    price = float(price_text)
                except ValueError:
                    messagebox.showwarning(
                        "Invalid Price",
                        (
                            "Per Unit Price must contain only a number "
                            "greater than or equal to zero. "
                            "Decimal values are allowed."
                        ),
                        parent=dialog,
                    )
                    return

                if not math.isfinite(price):
                    messagebox.showwarning(
                        "Invalid Price",
                        "Per Unit Price must be a valid number.",
                        parent=dialog,
                    )
                    return

                if price < 0:
                    messagebox.showwarning(
                        "Invalid Price",
                        "Per Unit Price cannot be negative.",
                        parent=dialog,
                    )
                    return

                if not quantity_text or int(quantity_text) < 1:
                    messagebox.showwarning(
                        "Invalid Quantity",
                        "Quantity must be a whole number with minimum 1.",
                        parent=dialog,
                    )
                    return

                try:
                    product = Product(
                        id=None,
                        name=name,
                        description=description or None,
                        sku=product_code,
                        price=price,
                        quantity=int(quantity_text),
                        created_at=datetime.now().isoformat(
                            timespec="seconds",
                        ),
                    )

                    confirmed = messagebox.askyesno(
                        "Confirm Add Product",
                        f"Are you sure you want to add '{name}'?",
                        parent=dialog,
                    )
                    if not confirmed:
                        return

                    self.context.product_service.add_product(product)
                    dialog.destroy()
                    load_products()

                    messagebox.showinfo(
                        "Success",
                        "Product added successfully.",
                    )
                except sqlite3.IntegrityError as exc:
                    if "UNIQUE constraint failed: products.sku" in str(exc):
                        messagebox.showwarning(
                            "Product Code Already in Use",
                            (
                                f"Product Code '{product_code}' is already "
                                "in use.\n\nPlease change the Product Code "
                                "and try again."
                            ),
                            parent=dialog,
                        )
                    else:
                        messagebox.showwarning(
                            "Unable to Add Product",
                            str(exc),
                            parent=dialog,
                        )
                except (ValueError, TypeError) as exc:
                    messagebox.showwarning(
                        "Unable to Add Product",
                        str(exc),
                        parent=dialog,
                    )

            ttk.Button(
                dialog,
                text="Confirm",
                command=submit,
            ).pack(
                fill="x",
                padx=20,
                pady=20,
            )

            entries["Name"].focus_set()

        def edit_product(
            product=None,
            parent=None,
            on_updated=None,
        ) -> None:
            if product is not None and product.id is not None:
                latest_product = next(
                    (
                        cached_product
                        for cached_product in products_cache
                        if cached_product.id == product.id
                    ),
                    None,
                )
                if latest_product is not None:
                    product = latest_product

            if product is None:
                product = get_selected_product()

            if product is None:
                messagebox.showwarning(
                    "Edit Product",
                    "Please select a product first.",
                    parent=parent,
                )
                return

            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Product")
            dialog.geometry("500x410")
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(
                dialog,
                text="Edit Product",
                font=("TkDefaultFont", 18, "bold"),
            ).pack(
                anchor="w",
                padx=20,
                pady=(20, 15),
            )

            form = ttk.LabelFrame(
                dialog,
                text="Product Information",
                padding=15,
            )
            form.pack(
                fill="x",
                padx=20,
            )

            entries = {}
            values = (
                ("Name", product.name),
                ("Description", product.description or ""),
                ("Product Code", product.sku),
                ("Per Unit Price", str(product.price)),
            )

            for row, (label, value) in enumerate(values):
                ttk.Label(
                    form,
                    text=label,
                    font=("TkDefaultFont", 10, "bold"),
                ).grid(
                    row=row,
                    column=0,
                    sticky="w",
                    padx=5,
                    pady=6,
                )

                entry = ttk.Entry(
                    form,
                    width=38,
                )
                entry.insert(0, value)
                entry.grid(
                    row=row,
                    column=1,
                    sticky="ew",
                    padx=10,
                    pady=6,
                )
                entries[label] = entry

            description_validate = dialog.register(
                validate_description,
            )
            entries["Description"].configure(
                validate="key",
                validatecommand=(
                    description_validate,
                    "%P",
                ),
            )

            ttk.Label(
                form,
                text=f"Quantity: {product.quantity}",
                font=("TkDefaultFont", 10, "bold"),
            ).grid(
                row=4,
                column=0,
                columnspan=2,
                sticky="w",
                padx=5,
                pady=(10, 2),
            )

            ttk.Label(
                form,
                text="Quantity can only be changed from Inventory.",
            ).grid(
                row=5,
                column=0,
                columnspan=2,
                sticky="w",
                padx=5,
                pady=(0, 5),
            )

            def submit() -> None:
                name = entries["Name"].get().strip()
                description = entries["Description"].get().strip()
                product_code = entries["Product Code"].get().strip()
                price_text = entries["Per Unit Price"].get().strip()

                if not name:
                    messagebox.showwarning(
                        "Invalid Product",
                        "Product name is required.",
                        parent=dialog,
                    )
                    return

                if not valid_product_code(product_code):
                    product_code_warning(dialog)
                    return

                try:
                    price = float(price_text)
                except ValueError:
                    messagebox.showwarning(
                        "Invalid Price",
                        (
                            "Per Unit Price must contain only a number "
                            "greater than or equal to zero. "
                            "Decimal values are allowed."
                        ),
                        parent=dialog,
                    )
                    return

                if not math.isfinite(price):
                    messagebox.showwarning(
                        "Invalid Price",
                        "Per Unit Price must be a valid number.",
                        parent=dialog,
                    )
                    return

                if price < 0:
                    messagebox.showwarning(
                        "Invalid Price",
                        "Per Unit Price cannot be negative.",
                        parent=dialog,
                    )
                    return

                changed_fields = []
                if name != product.name:
                    changed_fields.append("Name")
                if description != (product.description or ""):
                    changed_fields.append("Description")
                if product_code != product.sku:
                    changed_fields.append("Product Code")
                if price != product.price:
                    changed_fields.append("Per Unit Price")

                if not changed_fields:
                    messagebox.showinfo(
                        "No Changes",
                        "No product changes were made.",
                        parent=dialog,
                    )
                    return

                if not messagebox.askyesno(
                    "Confirm Edit",
                    "Are you sure you want to save these changes?",
                    parent=dialog,
                ):
                    return

                try:
                    updated = Product(
                        id=product.id,
                        name=name,
                        description=description or None,
                        sku=product_code,
                        price=price,
                        quantity=product.quantity,
                        created_at=product.created_at,
                    )

                    self.context.product_service.update_product(updated)
                    load_products()

                    if on_updated is not None:
                        on_updated(updated)

                    dialog.destroy()

                    messagebox.showinfo(
                        "Success",
                        "Product updated successfully.",
                    )
                except sqlite3.IntegrityError as exc:
                    if "UNIQUE constraint failed: products.sku" in str(exc):
                        messagebox.showwarning(
                            "Product Code Already in Use",
                            (
                                f"Product Code '{product_code}' is already "
                                "in use.\n\nPlease change the Product Code "
                                "and try again."
                            ),
                            parent=dialog,
                        )
                    else:
                        messagebox.showwarning(
                            "Unable to Edit Product",
                            str(exc),
                            parent=dialog,
                        )
                except (ValueError, TypeError) as exc:
                    messagebox.showwarning(
                        "Unable to Edit Product",
                        str(exc),
                        parent=dialog,
                    )

            ttk.Button(
                dialog,
                text="Confirm",
                command=submit,
            ).pack(
                fill="x",
                padx=20,
                pady=20,
            )

            entries["Name"].focus_set()

        def delete_product(product=None, parent=None) -> None:
            if product is None:
                product = get_selected_product()

            if product is None:
                messagebox.showwarning(
                    "Delete Product",
                    "Please select a product first.",
                    parent=parent,
                )
                return

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                (
                    f"Are you sure you want to delete "
                    f"'{product.name}'?"
                ),
                parent=parent,
            )

            if not confirmed:
                return

            try:
                self.context.product_service.delete_product(
                    product.id,
                )

                if parent is not None:
                    parent.destroy()

                selected_product_id["value"] = None
                load_products()

                messagebox.showinfo(
                    "Success",
                    "Product deleted successfully.",
                )
            except ValueError as exc:
                messagebox.showwarning(
                    "Unable to Delete Product",
                    str(exc),
                    parent=parent,
                )

        def show_product_popup(event=None) -> None:
            row_id = (
                product_list.identify_row(event.y)
                if event
                else ""
            )

            if not row_id:
                return

            product_list.selection_set(row_id)
            product_list.focus(row_id)

            values = product_list.item(
                row_id,
                "values",
            )
            if not values:
                return

            product = next(
                (
                    item
                    for item in products_cache
                    if item.id == int(values[0])
                ),
                None,
            )
            if product is None:
                return

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

            details = (
                ("Product ID", product.id),
                ("Name", product.name),
                ("Description", product.description or ""),
                ("Product Code", product.sku),
                ("Per Unit Price", f"₹ {product.price:,.2f}"),
                ("Quantity", product.quantity),
            )

            detail_value_labels = {}

            for row, (label, value) in enumerate(details):
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

                value_label = ttk.Label(
                    details_frame,
                    text=str(value),
                )
                value_label.grid(
                    row=row,
                    column=1,
                    sticky="w",
                    padx=15,
                    pady=4,
                )
                detail_value_labels[label] = value_label

            def refresh_product_popup(updated):
                detail_value_labels["Name"].config(
                    text=updated.name,
                )
                detail_value_labels["Description"].config(
                    text=updated.description or "",
                )
                detail_value_labels["Product Code"].config(
                    text=updated.sku,
                )
                detail_value_labels["Per Unit Price"].config(
                    text=f"₹ {updated.price:,.2f}",
                )
                detail_value_labels["Quantity"].config(
                    text=str(updated.quantity),
                )

            operations = ttk.LabelFrame(
                popup,
                text="Product Operations",
                padding=15,
            )
            operations.pack(
                fill="x",
                padx=20,
                pady=(0, 15),
            )

            ttk.Button(
                operations,
                text="Edit",
                command=lambda: edit_product(
                    product,
                    popup,
                    refresh_product_popup,
                ),
            ).pack(
                fill="x",
                pady=4,
            )

            ttk.Button(
                operations,
                text="Delete",
                command=lambda: delete_product(
                    product,
                    popup,
                ),
            ).pack(
                fill="x",
                pady=4,
            )

        def select_product(event=None) -> None:
            selected = product_list.selection()

            if not selected:
                selected_product_id["value"] = None
                clear_edit_history()
                return

            values = product_list.item(
                selected[0],
                "values",
            )

            if not values:
                return

            selected_product_id["value"] = int(values[0])
            refresh_edit_history()

        ttk.Button(
            operation_frame,
            text="Add Product",
            command=add_product,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            operation_frame,
            text="Edit Product",
            command=edit_product,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            operation_frame,
            text="Delete Product",
            command=delete_product,
        ).pack(
            side="left",
            padx=5,
        )

        search_var.trace_add(
            "write",
            lambda *_: render_products(),
        )
        product_list.bind(
            "<<TreeviewSelect>>",
            select_product,
        )
        product_list.bind(
            "<Double-1>",
            show_product_popup,
        )

        load_products()
        self.root.after_idle(
            self._refresh_initial_layout,
        )


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
            on_completed=None,
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
                    "Enter the new total stock quantity. Minimum is 0."
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

                current_product = next(
                    (
                        product
                        for product in products_cache
                        if product.id == product_id
                    ),
                    None,
                )
                current_quantity = (
                    current_product.quantity
                    if current_product is not None
                    else 0
                )

                if operation == "Adjust Stock":
                    if quantity == 0 and current_quantity <= 0:
                        messagebox.showwarning(
                            "No Stock Left",
                            (
                                "There is no stock left for this product. "
                                "Please add stock before setting the stock "
                                "quantity to 0."
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

                if operation == "Stock Out":
                    if current_quantity <= 0:
                        messagebox.showwarning(
                            "No Stock Left",
                            (
                                "There is no stock left for this product. "
                                "Stock Out cannot be performed."
                            ),
                            parent=dialog,
                        )
                        return

                    if quantity > current_quantity:
                        messagebox.showwarning(
                            "Insufficient Stock",
                            (
                                f"Available stock is {current_quantity}. "
                                "Please enter a quantity within the "
                                "available stock."
                            ),
                            parent=dialog,
                        )
                        return

                    if quantity == current_quantity:
                        messagebox.showwarning(
                            "Stock Out Not Allowed",
                            (
                                "Stock Out must leave at least 1 unit. "
                                "If you want to reduce the stock to 0, "
                                "use Adjust Stock instead."
                            ),
                            parent=dialog,
                        )
                        return

                confirmed = messagebox.askyesno(
                    f"Confirm {operation}",
                    f"Are you sure you want to perform {operation.lower()}?",
                    parent=dialog,
                )
                if not confirmed:
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

                            if on_completed is not None:
                                on_completed(
                                    product_id,
                                    values,
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
                text="Confirm",
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

            detail_value_labels = {}

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

                value_label = ttk.Label(
                    details_frame,
                    text=str(value),
                )
                value_label.grid(
                    row=row,
                    column=1,
                    sticky="w",
                    padx=15,
                    pady=4,
                )
                detail_value_labels[label] = value_label

            def refresh_inventory_popup(product_id, values):
                detail_value_labels["Quantity/unit"].config(
                    text=values[3],
                )
                detail_value_labels["Per Unit Price"].config(
                    text=values[4],
                )
                detail_value_labels["Total Stock Price"].config(
                    text=values[5],
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
                command=lambda: run_stock_operation(
                    "Stock In",
                    refresh_inventory_popup,
                ),
            ).pack(
                fill="x",
                pady=4,
            )

            ttk.Button(
                popup_operation_frame,
                text="Stock Out",
                command=lambda: run_stock_operation(
                    "Stock Out",
                    refresh_inventory_popup,
                ),
            ).pack(
                fill="x",
                pady=4,
            )

            ttk.Button(
                popup_operation_frame,
                text="Adjust Stock",
                command=lambda: run_stock_operation(
                    "Adjust Stock",
                    refresh_inventory_popup,
                ),
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


    def _show_sales(self) -> None:
        sales_content = ttk.Frame(self.content)
        sales_content.pack(fill="both", expand=True)

        sales_cache = []
        customer_cache = []
        payment_totals = {}
        sort_state = {
            "column": "id",
            "descending": False,
        }

        style = ttk.Style()
        style.configure(
            "Sales.Treeview.Heading",
            font=("TkDefaultFont", 10, "bold"),
        )

        top_bar = ttk.Frame(sales_content)
        top_bar.pack(
            fill="x",
            pady=(0, 10),
        )

        operation_frame = ttk.LabelFrame(
            top_bar,
            text="Sales Operations",
            padding=8,
        )
        operation_frame.pack(
            side="left",
            fill="y",
        )

        create_button = ttk.Button(
            operation_frame,
            text="Create Sale",
            command=lambda: messagebox.showinfo(
                "Sales",
                "Sale creation will be added in the next Sales topic.",
            ),
        )
        create_button.pack(
            padx=4,
            pady=2,
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
        search_placeholder = "Search by ID, Customer or Sale Date"
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
        search_entry.insert(0, search_placeholder)
        search_entry.configure(foreground="gray")

        table_frame = ttk.LabelFrame(
            sales_content,
            text="Sales",
            padding=10,
        )
        table_frame.pack(
            fill="both",
            expand=True,
        )

        table_container = ttk.Frame(table_frame)
        table_container.pack(
            fill="both",
            expand=True,
        )

        sales_list = ttk.Treeview(
            table_container,
            columns=(
                "id",
                "customer",
                "date",
                "total",
                "paid",
                "balance",
            ),
            show="headings",
            style="Sales.Treeview",
        )

        headings = (
            ("id", "ID"),
            ("customer", "Customer"),
            ("date", "Sale Date"),
            ("total", "Total Amount"),
            ("paid", "Paid Amount"),
            ("balance", "Balance"),
        )

        for column, heading in headings:
            sales_list.heading(
                column,
                text=heading,
                command=lambda c=column: sort_sales(c),
            )
            sales_list.column(
                column,
                width=1,
                anchor="center",
                stretch=True,
            )

        sales_scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=sales_list.yview,
        )
        sales_list.configure(yscrollcommand=sales_scrollbar.set)
        sales_list.pack(
            side="left",
            fill="both",
            expand=True,
        )
        sales_scrollbar.pack(
            side="right",
            fill="y",
        )

        def resize_sales_columns(event=None) -> None:
            available_width = max(sales_list.winfo_width() - 2, 1)
            widths = {
                "id": 0.10,
                "customer": 0.24,
                "date": 0.20,
                "total": 0.16,
                "paid": 0.15,
                "balance": 0.15,
            }
            for column, ratio in widths.items():
                sales_list.column(
                    column,
                    width=max(1, int(available_width * ratio)),
                )

        sales_list.bind("<Configure>", resize_sales_columns)

        def sort_sales(column: str) -> None:
            if sort_state["column"] == column:
                sort_state["descending"] = not sort_state["descending"]
            else:
                sort_state["column"] = column
                sort_state["descending"] = False
            refresh_sales()

        def update_sales_headings() -> None:
            for column, heading in headings:
                arrow = ""
                if sort_state["column"] == column:
                    arrow = " ▼" if sort_state["descending"] else " ▲"
                sales_list.heading(
                    column,
                    text=heading + arrow,
                )

        def customer_name(customer_id: int) -> str:
            customer = next(
                (item for item in customer_cache if item.id == customer_id),
                None,
            )
            if customer is None:
                return f"Customer #{customer_id}"
            return customer.name

        def refresh_sales() -> None:
            nonlocal sales_cache, customer_cache, payment_totals

            sales_cache = self.context.sale_service.get_sales()
            customer_cache = self.context.customer_service.get_customers()
            payments = self.context.sale_payment_service.get_payments()
            payment_totals = {}
            for payment in payments:
                payment_totals[payment.sale_id] = (
                    payment_totals.get(payment.sale_id, 0.0)
                    + payment.amount
                )

            query = ""
            if not search_placeholder_active["value"]:
                query = search_var.get().strip().lower()

            filtered_sales = []
            for sale in sales_cache:
                name = customer_name(sale.customer_id)
                if query:
                    searchable = (
                        str(sale.id),
                        name.lower(),
                        sale.sale_date.lower(),
                    )
                    if not any(query in value for value in searchable):
                        continue
                filtered_sales.append(sale)

            def sort_value(sale):
                paid = payment_totals.get(sale.id, 0.0)
                balance = sale.total_amount - paid
                values = {
                    "id": sale.id or 0,
                    "customer": customer_name(sale.customer_id).lower(),
                    "date": sale.sale_date,
                    "total": sale.total_amount,
                    "paid": paid,
                    "balance": balance,
                }
                return values[sort_state["column"]]

            filtered_sales.sort(
                key=sort_value,
                reverse=sort_state["descending"],
            )

            for item in sales_list.get_children():
                sales_list.delete(item)

            for sale in filtered_sales:
                paid = payment_totals.get(sale.id, 0.0)
                balance = sale.total_amount - paid
                sales_list.insert(
                    "",
                    "end",
                    values=(
                        sale.id,
                        customer_name(sale.customer_id),
                        sale.sale_date,
                        f"₹{sale.total_amount:.2f}",
                        f"₹{paid:.2f}",
                        f"₹{balance:.2f}",
                    ),
                )

            update_sales_headings()

        def clear_search_placeholder(event=None) -> None:
            if search_placeholder_active["value"]:
                search_placeholder_active["value"] = False
                search_entry.delete(0, tk.END)
                search_entry.configure(foreground="black")
            refresh_sales()

        def restore_search_placeholder(event=None) -> None:
            if not search_entry.get().strip():
                search_placeholder_active["value"] = True
                search_entry.delete(0, tk.END)
                search_entry.insert(0, search_placeholder)
                search_entry.configure(foreground="gray")
            refresh_sales()

        search_entry.bind("<FocusIn>", clear_search_placeholder)
        search_entry.bind("<FocusOut>", restore_search_placeholder)
        search_entry.bind("<KeyRelease>", lambda event: refresh_sales())

        refresh_sales()

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
