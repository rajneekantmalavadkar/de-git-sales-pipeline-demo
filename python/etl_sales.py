
# python/etl_sales.py (Complete Listing)

import csv
import os
import sys
from datetime import datetime


PIPELINE_NAME = "Daily Sales Aggregator"
INPUT_FILE = os.path.join("data", "sales.csv")


def extract_sales_data(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Input file {file_path} does not exist.")
        sys.exit(1)

    records = []

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            records.append(row)

    print(
        f"[INFO] Successfully extracted "
        f"{len(records)} records from {file_path}"
    )

    return records


def transform_sales_data(records):
    transformed = []
    total_revenue = 0.0

    for row in records:
        try:
            tx_id = row["transaction_id"]
            cust_id = row["customer_id"]
            category = row["product_category"]
            amount = float(row["amount"])
            tx_date = row["transaction_date"]

            if amount <= 0:
                print(
                    f"[WARN] Skipping invalid transaction amount: "
                    f"{amount} for ID {tx_id}"
                )
                continue

            total_revenue += amount

            transformed.append(
                {
                    "transaction_id": tx_id,
                    "customer_id": cust_id,
                    "category": category,
                    "net_amount": amount,
                    "transaction_date": tx_date,
                    "etl_processed_at": datetime.now().isoformat(),
                }
            )

        except (ValueError, KeyError) as e:
            print(f"[ERROR] Data parsing error in row {row}: {e}")

    print(
        f"[INFO] Transformed {len(transformed)} valid records. "
        f"Total Net Sales: ${total_revenue:,.2f}"
    )

    return transformed


if __name__ == "__main__":
    print(f"=== Starting ETL Pipeline: {PIPELINE_NAME} ===")

    raw_data = extract_sales_data(INPUT_FILE)

    clean_data = transform_sales_data(raw_data)

    print("=== Pipeline Execution Completed Successfully ===")

