import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from domain.entities.customer import Customer
from domain.entities.product import Product
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

    def show_view(self, name: str) -> None:
        for widget in self.content.winfo_children():
            widget.destroy()

        if name == "Dashboard":
            self._show_dashboard()
            return

        if name == "Products":
            self._show_products()
            return

        if name == "Customers":
            self._show_customers()
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
