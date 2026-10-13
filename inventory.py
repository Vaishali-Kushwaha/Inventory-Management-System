from database import get_connection


# Add Product
def add_product(name, category, quantity, price, supplier,
                low_stock_limit=5):
    conn = get_connection()

    if conn is None:
        print("Database connection failed.")
        return False

    cursor = None

    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO products
            (product_name, category, quantity, price,
             supplier, low_stock_limit)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name, category, quantity, price,
            supplier, low_stock_limit
        )

        cursor.execute(query, values)
        conn.commit()

        print("Product added successfully!")
        return True

    except Exception as e:
        print("Error adding product:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# View All Products
def view_products():
    conn = get_connection()

    if conn is None:
        print("Database connection failed.")
        return []

    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        if not products:
            print("No products found.")
        else:
            print("\n--- All Products ---")
            for product in products:
                print(product)

        return products

    except Exception as e:
        print("Error viewing products:", e)
        return []

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# Search Product
def search_product(product_id):
    conn = get_connection()

    if conn is None:
        print("Database connection failed.")
        return None

    cursor = None

    try:
        cursor = conn.cursor()

        query = """
            SELECT * FROM products
            WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        if product:
            print("Product found:", product)
        else:
            print("Product not found.")

        return product

    except Exception as e:
        print("Error searching product:", e)
        return None

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# Update Product
def update_product(product_id, name, category, quantity,
                   price, supplier, low_stock_limit=5):
    conn = get_connection()

    if conn is None:
        print("Database connection failed.")
        return False

    cursor = None

    try:
        cursor = conn.cursor()

        query = """
            UPDATE products
            SET product_name = %s,
                category = %s,
                quantity = %s,
                price = %s,
                supplier = %s,
                low_stock_limit = %s
            WHERE product_id = %s
        """

        values = (
            name, category, quantity, price,
            supplier, low_stock_limit, product_id
        )

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            print("Product updated successfully!")
            return True

        print("Product not found.")
        return False

    except Exception as e:
        print("Error updating product:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# Delete Product
def delete_product(product_id):
    conn = get_connection()

    if conn is None:
        print("Database connection failed.")
        return False

    cursor = None

    try:
        cursor = conn.cursor()

        query = """
            DELETE FROM products
            WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Product deleted successfully!")
            return True

        print("Product not found.")
        return False

    except Exception as e:
        print("Error deleting product:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# Low Stock Products
def low_stock_products():
    conn = get_connection()

    if conn is None:
        print("Database connection failed.")
        return []

    cursor = None

    try:
        cursor = conn.cursor()

        query = """
            SELECT * FROM products
            WHERE quantity <= low_stock_limit
        """

        cursor.execute(query)
        products = cursor.fetchall()

        print("\n--- Low Stock Products ---")

        if not products:
            print("No low-stock products found.")
        else:
            for product in products:
                print(product)

        return products

    except Exception as e:
        print("Error checking stock:", e)
        return []

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()