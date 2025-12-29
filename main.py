from utils.data_processor import clean_sales_data
from utils.api_handler import fetch_product_info
from collections import defaultdict

FILE = "data/sales_data.txt"

rows = clean_sales_data(FILE)

sales = defaultdict(float)
region_sales = defaultdict(float)
customer_sales = defaultdict(float)

for r in rows:
    tid, date, pid, pname, qty, price, cid, region = r
    total_price = qty * price
    sales[pname] += total_price
    region_sales[region] += total_price
    customer_sales[cid] += total_price

report = []
report.append("SALES ANALYTICS REPORT")
report.append("-"*30)
report.append("Top Products:")
for k,v in sorted(sales.items(), key=lambda x:-x[1])[:5]:
    report.append(f"{k}: Rs {v:,.2f}")

report.append("\nSales by Region:")
for k,v in region_sales.items():
    report.append(f"{k}: Rs {v:,.2f}")

report.append("\nTop Customers:")
for k,v in sorted(customer_sales.items(), key=lambda x:-x[1])[:5]:
    report.append(f"{k}: Rs {v:,.2f}")

report_text = "\n".join(report)

# FORCE SAVE REPORT
with open("output/report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print("\n" + report_text)
print("\nReport saved successfully to output/report.txt")

input("Press Enter to exit...")
