from inventory import (
    add_product,
    view_products,
    search_product,
    update_product,
    delete_product,
    low_stock_products
)


def main():
    while True:
        print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Low Stock Products")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Product name: ")
            category = input("Category: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            supplier = input("Supplier: ")
            limit = int(input("Low stock limit: "))

            add_product(
                name, category, quantity,
                price, supplier, limit
            )

        elif choice == "2":
            view_products()

        elif choice == "3":
            product_id = int(input("Enter product ID: "))
            search_product(product_id)

        elif choice == "4":
            product_id = int(input("Enter product ID: "))
            name = input("New product name: ")
            category = input("New category: ")
            quantity = int(input("New quantity: "))
            price = float(input("New price: "))
            supplier = input("New supplier: ")
            limit = int(input("New low stock limit: "))

            update_product(
                product_id, name, category,
                quantity, price, supplier, limit
            )

        elif choice == "5":
            product_id = int(input("Enter product ID to delete: "))
            confirm = input("Are you sure? (yes/no): ")

            if confirm.lower() == "yes":
                delete_product(product_id)

        elif choice == "6":
            low_stock_products()

        elif choice == "7":
            print("Thank you for using Inventory Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()