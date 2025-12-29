import os
import sys

from utils.file_handler import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

from utils.data_processor import generate_sales_report


def main():
    print("=" * 50)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 50)

    try:
        # [1/10] Reading sales data
        print("\n[1/10] Reading sales data...")
        lines = []
        with open("data/sales_data.txt", "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                if line.strip():
                    lines.append(line.strip().split("|"))

        print(f"✓ Successfully read {len(lines)} transactions")

        # [2/10] Parsing and cleaning data
        print("\n[2/10] Parsing and cleaning data...")
        transactions = []
        invalid = 0

        for row in lines:
            try:
                if len(row) != 8:
                    invalid += 1
                    continue

                transactions.append({
                    "TransactionID": row[0],
                    "Date": row[1],
                    "ProductID": row[2],
                    "ProductName": row[3],
                    "Quantity": int(row[4].replace(",", "")),
                    "UnitPrice": float(row[5].replace(",", "")),
                    "CustomerID": row[6],
                    "Region": row[7]
                })
            except:
                invalid += 1

        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Filter info
        print("\n[3/10] Filter Options:")
        regions = set(t["Region"] for t in transactions)
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]

        print("Regions:", ", ".join(sorted(regions)))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        if input("Do you want to filter data? (y/n): ").lower() == "y":
            r = input("Enter region: ")
            transactions = [t for t in transactions if t["Region"] == r]
            print(f"Filtered records: {len(transactions)}")

        # [4/10] Validation summary
        print("\n[4/10] Validating transactions...")
        print(f"Valid: {len(transactions)} | Invalid: {invalid}")

        # [5/10] Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(transactions)
        region_wise_sales(transactions)
        top_selling_products(transactions, 5)
        customer_analysis(transactions)
        daily_sales_trend(transactions)
        find_peak_sales_day(transactions)
        low_performing_products(transactions, 5)
        print("✓ Analysis completed")

        # [6/10] API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrichment
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(transactions, product_mapping)
        success = sum(1 for e in enriched_data if e["API_Match"])
        print(f"✓ Enriched {success}/{len(enriched_data)} records")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data)

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        os.makedirs("output", exist_ok=True)
        generate_sales_report(transactions, enriched_data)

        # [10/10] Complete
        print("\n[10/10] Process Complete!")
        print("=" * 50)

    except Exception as e:
        print("\n❌ ERROR:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
