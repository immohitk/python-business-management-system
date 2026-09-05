from presentation.cli.products import handle_products

from presentation.cli.inventory import handle_inventory

from presentation.cli.sales import handle_sales

def display_menu() -> None:
    print("========================================")
    print("   Python Business Management System")
    print("========================================")
    print()
    print("1. Products")
    print("2. Inventory")
    print("3. Sales")
    print("4. Customers")
    print("5. Suppliers")
    print("0. Exit")
    print()


def handle_choice(choice: str) -> bool:
    if choice == "0":
        print("Exiting application...")
        return False

    if choice == "1":
        handle_products()
        return True

    if choice == "2":
        handle_inventory()
        return True

    if choice == "3":
        handle_sales()
        return True

    if choice in {"4", "5"}:
        print(f"You selected: {choice}")
        return True

    print("Invalid choice. Please select a valid option.")
    return True


def run() -> None:
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if not handle_choice(choice):
            break
