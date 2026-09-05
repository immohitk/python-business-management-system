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

    if choice in {"1", "2", "3", "4", "5"}:
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
