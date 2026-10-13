import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from inventory import (
    add_product,
    view_products,
    search_product,
    update_product,
    delete_product,
    low_stock_products
)

# ---------------- COLORS ----------------
BG = "#F3F6F8"
HEADER_BG = "#263238"
HEADER_FG = "#FFFFFF"
TEXT = "#263238"
MUTED_TEXT = "#64748B"
ENTRY_BG = "#FFFFFF"
BUTTON_BG = "#0F766E"
ACTIVE_BG = "#115E59"
TABLE_BG = "#FFFFFF"
BORDER = "#D1D5DB"

root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg=BG)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg=HEADER_BG, pady=16)
header.pack(fill="x")

tk.Label(
    header,
    text="INVENTORY MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg=HEADER_BG,
    fg=HEADER_FG
).pack()

tk.Label(
    header,
    text="Manage Products | Stock | Suppliers",
    font=("Arial", 10),
    bg=HEADER_BG,
    fg="#CBD5E1"
).pack(pady=(4, 0))

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=TABLE_BG,
    foreground=TEXT,
    fieldbackground=TABLE_BG,
    rowheight=30,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=HEADER_BG,
    foreground=HEADER_FG,
    font=("Arial", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[("selected", "#CCFBF1")],
    foreground=[("selected", TEXT)]
)

style.configure("TCombobox", padding=5)

# ---------------- FORM ----------------
form = tk.Frame(root, bg=BG, padx=20, pady=15)
form.pack(fill="x")

entries = {}

fields = [
    ("Product Name", "product_name"),
    ("Category", "category"),
    ("Quantity", "quantity"),
    ("Price", "price"),
    ("Supplier", "supplier"),
    ("Low Stock Limit", "low_stock_limit")
]

for i, (label_text, key) in enumerate(fields):
    row = i // 3
    col = (i % 3) * 2

    tk.Label(
        form,
        text=label_text,
        bg=BG,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).grid(row=row * 2, column=col, sticky="w", padx=8, pady=(5, 2))

    entry = tk.Entry(
        form,
        bg=ENTRY_BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BUTTON_BG,
        font=("Arial", 10)
    )
    entry.grid(
        row=row * 2 + 1,
        column=col,
        sticky="ew",
        padx=8,
        pady=(0, 10),
        ipady=6
    )
    entries[key] = entry

for col in (1, 3, 5):
    form.grid_columnconfigure(col, weight=1)

# ---------------- TABLE ----------------
table_frame = tk.Frame(root, bg=BG, padx=20, pady=5)
table_frame.pack(fill="both", expand=True)

columns = (
    "id", "product_name", "category",
    "quantity", "price", "supplier", "low_stock_limit"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

headings = {
    "id": "ID",
    "product_name": "Product Name",
    "category": "Category",
    "quantity": "Quantity",
    "price": "Price",
    "supplier": "Supplier",
    "low_stock_limit": "Low Stock Limit"
}

widths = {
    "id": 50,
    "product_name": 180,
    "category": 120,
    "quantity": 90,
    "price": 90,
    "supplier": 160,
    "low_stock_limit": 120
}

for col in columns:
    tree.heading(col, text=headings[col])
    tree.column(col, width=widths[col], minwidth=50, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical", command=tree.yview
)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tree.tag_configure("odd", background="#FFFFFF")
tree.tag_configure("even", background="#F1F5F9")

# ---------------- HELPERS ----------------
def get_selected_id():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Product", "Please select a product from the table.")
        return None

    values = tree.item(selected[0], "values")
    return values[0]


def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    tree.selection_remove(tree.selection())


def refresh_table(rows=None):
    try:
        if rows is None:
            rows = view_products()

        tree.delete(*tree.get_children())

        if rows:
            for index, row in enumerate(rows):
                tag = "even" if index % 2 == 0 else "odd"
                tree.insert("", tk.END, values=tuple(row), tags=(tag,))

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


def select_row(event):
    selected = tree.selection()
    if not selected:
        return

    values = tree.item(selected[0], "values")
    if len(values) < 7:
        return

    keys = [
        "product_name", "category", "quantity",
        "price", "supplier", "low_stock_limit"
    ]

    for key, value in zip(keys, values[1:7]):
        entries[key].delete(0, tk.END)
        entries[key].insert(0, str(value))


tree.bind("<<TreeviewSelect>>", select_row)


# ---------------- BUTTON ACTIONS ----------------
def add_action():
    try:
        name = entries["product_name"].get().strip()
        category = entries["category"].get().strip()
        quantity = entries["quantity"].get().strip()
        price = entries["price"].get().strip()
        supplier = entries["supplier"].get().strip()
        limit = entries["low_stock_limit"].get().strip()

        if not all([name, category, quantity, price, supplier, limit]):
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        quantity_value = int(quantity)
        price_value = float(price)
        limit_value = int(limit)

        if quantity_value < 0 or price_value < 0 or limit_value < 0:
            messagebox.showwarning("Invalid Data", "Quantity, price and limit cannot be negative.")
            return

        add_product(name, category, quantity_value, price_value, supplier, limit_value)
        messagebox.showinfo("Success", "Product added successfully!")
        clear_fields()
        refresh_table()

    except ValueError:
        messagebox.showerror("Invalid Input", "Quantity and limit must be whole numbers; price must be numeric.")
    except Exception as error:
        messagebox.showerror("Error", str(error))


def view_action():
    refresh_table()


def search_action():
    product_id = simpledialog.askinteger("Search Product", "Enter Product ID:")
    if product_id is None:
        return

    try:
        result = search_product(product_id)
        tree.delete(*tree.get_children())

        if result:
            if isinstance(result, (list, tuple)) and result and isinstance(result[0], (list, tuple)):
                rows = result
            else:
                rows = [result]

            for index, row in enumerate(rows):
                tree.insert("", tk.END, values=tuple(row), tags=("even",))
        else:
            messagebox.showinfo("Not Found", "No product found with this ID.")

    except Exception as error:
        messagebox.showerror("Error", str(error))


def update_action():
    product_id = get_selected_id()
    if product_id is None:
        return

    try:
        name = entries["product_name"].get().strip()
        category = entries["category"].get().strip()
        quantity = entries["quantity"].get().strip()
        price = entries["price"].get().strip()
        supplier = entries["supplier"].get().strip()
        limit = entries["low_stock_limit"].get().strip()

        if not all([name, category, quantity, price, supplier, limit]):
            messagebox.showwarning("Missing Data", "Select a product and fill all fields.")
            return

        quantity_value = int(quantity)
        price_value = float(price)
        limit_value = int(limit)

        if quantity_value < 0 or price_value < 0 or limit_value < 0:
            messagebox.showwarning("Invalid Data", "Values cannot be negative.")
            return

        update_product(
            int(product_id), name, category,
            quantity_value, price_value, supplier, limit_value
        )
        messagebox.showinfo("Success", "Product updated successfully!")
        clear_fields()
        refresh_table()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
    except Exception as error:
        messagebox.showerror("Error", str(error))


def delete_action():
    product_id = get_selected_id()
    if product_id is None:
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
        return

    try:
        delete_product(int(product_id))
        messagebox.showinfo("Success", "Product deleted successfully!")
        clear_fields()
        refresh_table()

    except Exception as error:
        messagebox.showerror("Error", str(error))


def low_stock_action():
    try:
        rows = low_stock_products()
        tree.delete(*tree.get_children())

        if rows:
            for index, row in enumerate(rows):
                tree.insert(
                    "", tk.END, values=tuple(row),
                    tags=("even" if index % 2 == 0 else "odd",)
                )
        else:
            messagebox.showinfo("Low Stock", "No low-stock products found.")

    except Exception as error:
        messagebox.showerror("Error", str(error))


# ---------------- BUTTONS ----------------
button_frame = tk.Frame(root, bg=BG, padx=20, pady=12)
button_frame.pack(fill="x")

buttons = [
    ("Add Product", add_action),
    ("View All", view_action),
    ("Search", search_action),
    ("Update", update_action),
    ("Delete", delete_action),
    ("Low Stock", low_stock_action),
    ("Clear", clear_fields)
]

for label, command in buttons:
    tk.Button(
        button_frame,
        text=label,
        command=command,
        bg=BUTTON_BG,
        fg="white",
        activebackground=ACTIVE_BG,
        activeforeground="white",
        font=("Arial", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=8
    ).pack(side="left", padx=5, pady=4)

# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Inventory Management System | Developed using Python & MySQL",
    bg=HEADER_BG,
    fg=HEADER_FG,
    font=("Arial", 9),
    pady=9
)
footer.pack(fill="x", side="bottom")

# ---------------- START APP ----------------
refresh_table()
root.mainloop()