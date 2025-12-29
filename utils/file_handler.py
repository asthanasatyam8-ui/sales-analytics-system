# TASK 2.1 — SALES SUMMARY CALCULATOR

def calculate_total_revenue(transactions):
    total = 0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total


def region_wise_sales(transactions):
    result = {}
    total_sales = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in result:
            result[region] = {"total_sales": 0, "transaction_count": 0}

        result[region]["total_sales"] += amount
        result[region]["transaction_count"] += 1

    for r in result:
        result[r]["percentage"] = (result[r]["total_sales"] / total_sales) * 100 if total_sales else 0

    result = dict(sorted(result.items(), key=lambda x: -x[1]["total_sales"]))
    return result


def top_selling_products(transactions, n=5):
    result = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        amount = qty * t["UnitPrice"]

        if name not in result:
            result[name] = {"TotalQuantity": 0, "TotalRevenue": 0}

        result[name]["TotalQuantity"] += qty
        result[name]["TotalRevenue"] += amount

    sorted_products = sorted(result.items(), key=lambda x: -x[1]["TotalQuantity"])
    final = []
    for i in sorted_products[:n]:
        final.append((i[0], i[1]["TotalQuantity"], i[1]["TotalRevenue"]))
    return final


def customer_analysis(transactions):
    result = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]
        name = t["ProductName"]

        if cid not in result:
            result[cid] = {"total_spent": 0, "purchase_count": 0, "products": []}

        result[cid]["total_spent"] += amount
        result[cid]["purchase_count"] += 1
        if name not in result[cid]["products"]:
            result[cid]["products"].append(name)

    for c in result:
        result[c]["avg_order_value"] = result[c]["total_spent"] / result[c]["purchase_count"] if result[c]["purchase_count"] else 0

    result = dict(sorted(result.items(), key=lambda x: -x[1]["total_spent"]))
    return result


# TASK 2.2 — DATE BASED ANALYSIS

def daily_sales_trend(transactions):
    result = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]
        cid = t["CustomerID"]

        if date not in result:
            result[date] = {"revenue": 0, "transaction_count": 0, "unique_customers": set()}

        result[date]["revenue"] += amount
        result[date]["transaction_count"] += 1
        result[date]["unique_customers"].add(cid)

    for d in result:
        result[d]["unique_customers"] = len(result[d]["unique_customers"])

    result = dict(sorted(result.items()))
    return result


def find_peak_sales_day(transactions):
    trend = daily_sales_trend(transactions)
    peak_date = None
    peak_revenue = 0
    peak_tx = 0

    for d in trend:
        if trend[d]["revenue"] > peak_revenue:
            peak_revenue = trend[d]["revenue"]
            peak_date = d
            peak_tx = trend[d]["transaction_count"]

    return (peak_date, peak_revenue, peak_tx)


# TASK 2.3 — PRODUCT PERFORMANCE

def low_performing_products(transactions, threshold=10):
    result = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        amount = qty * t["UnitPrice"]

        if name not in result:
            result[name] = {"TotalQuantity": 0, "TotalRevenue": 0}

        result[name]["TotalQuantity"] += qty
        result[name]["TotalRevenue"] += amount

    sorted_products = sorted(result.items(), key=lambda x: x[1]["TotalQuantity"])
    final = []
    for i in sorted_products:
        if i[1]["TotalQuantity"] < threshold:
            final.append((i[0], i[1]["TotalQuantity"], i[1]["TotalRevenue"]))

    return final
