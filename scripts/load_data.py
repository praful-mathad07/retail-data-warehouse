
import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Locate the project and data folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Load database credentials from .env.
load_dotenv(PROJECT_DIR / ".env")


def get_connection():
    """Connect to PostgreSQL."""
    password = os.getenv("DB_PASSWORD")

    if not password or password == "YOUR_POSTGRES_PASSWORD":
        raise ValueError(
            "Set your actual PostgreSQL password in the .env file."
        )

    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "retail_dw"),
        user=os.getenv("DB_USER", "postgres"),
        password=password,
    )


def read_csv(filename):
    """Read a CSV file and return a list of dictionaries."""
    file_path = DATA_DIR / filename

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


def load_sales(conn):
    """Validate sales and insert new transactions."""
    sales = read_csv("sales.csv")
    inserted = 0
    skipped = 0

    with conn.cursor() as cur:
        for sale in sales:
            try:
                order_id = sale["order_id"].strip()
                product_name = sale["product_name"].strip()
                customer_name = sale["customer_name"].strip()
                full_date = sale["full_date"].strip()
                quantity = int(sale["quantity"])

                if not order_id:
                    raise ValueError("Order ID is missing")

                if quantity <= 0:
                    raise ValueError("Quantity must be positive")

                # Find the product.
                cur.execute(
                    """
                    SELECT product_id, unit_price, unit_cost
                    FROM dim_product
                    WHERE product_name = %s
                    """,
                    (product_name,),
                )
                product = cur.fetchone()

                # Find the customer.
                cur.execute(
                    """
                    SELECT customer_id
                    FROM dim_customer
                    WHERE customer_name = %s
                    """,
                    (customer_name,),
                )
                customer = cur.fetchone()

                # Find the date.
                cur.execute(
                    """
                    SELECT date_key
                    FROM dim_date
                    WHERE full_date = %s
                    """,
                    (full_date,),
                )
                date = cur.fetchone()

                if not product:
                    raise ValueError(
                        f"Unknown product: {product_name}"
                    )

                if not customer:
                    raise ValueError(
                        f"Unknown customer: {customer_name}"
                    )

                if not date:
                    raise ValueError(
                        f"Unknown date: {full_date}"
                    )

                # Insert the transaction.
                # This requires order_id to be UNIQUE in PostgreSQL.
                cur.execute(
                    """
                    INSERT INTO fact_sales (
                        order_id,
                        date_key,
                        product_id,
                        customer_id,
                        quantity,
                        unit_price,
                        unit_cost
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (order_id) DO NOTHING
                    RETURNING sales_id
                    """,
                    (
                        order_id,
                        date[0],
                        product[0],
                        customer[0],
                        quantity,
                        product[1],
                        product[2],
                    ),
                )

                if cur.fetchone():
                    inserted += 1
                else:
                    skipped += 1
                    print(f"Skipped duplicate order: {order_id}")

            except (ValueError, KeyError) as error:
                skipped += 1
                print(
                    f"Skipped {sale.get('order_id', 'unknown')}: "
                    f"{error}"
                )

    return inserted, skipped


def main():
    try:
        with get_connection() as conn:
            inserted, skipped = load_sales(conn)

        print("Pipeline completed successfully.")
        print(f"New sales inserted: {inserted}")
        print(f"Rows skipped: {skipped}")

    except (psycopg.Error, OSError, ValueError) as error:
        print(f"Pipeline failed: {error}")
        raise


if __name__ == "__main__":
    main()
