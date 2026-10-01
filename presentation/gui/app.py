import tkinter as tk
from tkinter import ttk

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
            card.pack(side="left", fill="both", expand=True, padx=5)

            value_label = ttk.Label(
                card,
                text=str(value),
                font=("TkDefaultFont", 16, "bold"),
            )
            value_label.pack()


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