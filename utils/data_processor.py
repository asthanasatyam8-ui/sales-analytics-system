import codecs

def clean_sales_data(file_path):
    raw = codecs.open(file_path, "r", encoding="latin1", errors="ignore").read().strip().split("\n")
    total = len(raw) - 1
    invalid = 0
    valid_rows = []

    for line in raw[1:]:
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) != 8:
            invalid += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        if not tid.startswith("T"):
            invalid += 1
            continue

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
            if qty <= 0 or price <= 0 or not cid or not region:
                invalid += 1
                continue
        except:
            invalid += 1
            continue

        pname = pname.replace(",", "")
        valid_rows.append([tid, date, pid, pname, qty, price, cid, region])

    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid_rows)}")
    return valid_rows
from collections import defaultdict
from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    total_revenue = 0
    total_transactions = len(transactions)
    region_stats = defaultdict(lambda: {"revenue": 0, "count": 0})
    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0})
    customer_stats = defaultdict(lambda: {"spent": 0, "count": 0})
    daily_stats = defaultdict(lambda: {"revenue": 0, "tx": 0, "customers": set()})

    enriched_success = 0
    enriched_fail = 0

    dates = []

    for tx, etx in zip(transactions, enriched_transactions):
        revenue = tx["Quantity"] * tx["UnitPrice"]
        total_revenue += revenue

        region = tx["Region"]
        product = tx["ProductName"]
        customer = tx["CustomerID"]
        date = tx["Date"]

        region_stats[region]["revenue"] += revenue
        region_stats[region]["count"] += 1

        product_stats[product]["qty"] += tx["Quantity"]
        product_stats[product]["revenue"] += revenue

        customer_stats[customer]["spent"] += revenue
        customer_stats[customer]["count"] += 1

        daily_stats[date]["revenue"] += revenue
        daily_stats[date]["tx"] += 1
        daily_stats[date]["customers"].add(customer)

        dates.append(date)

        if etx.get("API_Match"):
            enriched_success += 1
        else:
            enriched_fail += 1

    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    best_day = max(daily_stats.items(), key=lambda x: x[1]["revenue"])[0]
    worst_day = min(daily_stats.items(), key=lambda x: x[1]["revenue"])[0]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Records Processed: {total_transactions}\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {min(dates)} to {max(dates)}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        f.write("Region | Revenue | Transactions\n")
        for r, v in sorted(region_stats.items(), key=lambda x: x[1]["revenue"], reverse=True):
            f.write(f"{r} | ₹{v['revenue']:,.2f} | {v['count']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        for i, (p, v) in enumerate(sorted(product_stats.items(), key=lambda x: x[1]["revenue"], reverse=True)[:5], 1):
            f.write(f"{i}. {p} | Qty: {v['qty']} | Revenue: ₹{v['revenue']:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        for i, (c, v) in enumerate(sorted(customer_stats.items(), key=lambda x: x[1]["spent"], reverse=True)[:5], 1):
            f.write(f"{i}. {c} | Spent: ₹{v['spent']:,.2f} | Orders: {v['count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        f.write("Date | Revenue | Transactions | Customers\n")
        for d, v in sorted(daily_stats.items()):
            f.write(f"{d} | ₹{v['revenue']:,.2f} | {v['tx']} | {len(v['customers'])}\n")
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Best Selling Day: {best_day}\n")
        f.write(f"Lowest Performing Day: {worst_day}\n\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Products Enriched: {enriched_success}\n")
        f.write(f"Failed Enrichments: {enriched_fail}\n")
        f.write(f"Success Rate: {(enriched_success / total_transactions) * 100:.2f}%\n")

    print("✅ Sales report generated successfully")

