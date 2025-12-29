import requests

def fetch_product_info(product_id):
    return {"product_id": product_id, "api_data": "Mock API response"}

import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns a list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("✅ Products fetched successfully")
        return data.get("products", [])
    except Exception as e:
        print("❌ Failed to fetch products:", e)
        return []
def create_product_mapping(api_products):
    """
    Creates a mapping of product ID to product info
    """
    mapping = {}

    for product in api_products:
        mapping[product["id"]] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return mapping
def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for tx in transactions:
        new_tx = tx.copy()

        try:
            # Extract number from ProductID (P101 → 101)
            product_id = int(tx["ProductID"][1:])

            if product_id in product_mapping:
                product = product_mapping[product_id]
                new_tx["API_Category"] = product["category"]
                new_tx["API_Brand"] = product["brand"]
                new_tx["API_Rating"] = product["rating"]
                new_tx["API_Match"] = True
            else:
                new_tx["API_Category"] = None
                new_tx["API_Brand"] = None
                new_tx["API_Rating"] = None
                new_tx["API_Match"] = False

        except Exception:
            new_tx["API_Category"] = None
            new_tx["API_Brand"] = None
            new_tx["API_Rating"] = None
            new_tx["API_Match"] = False

        enriched.append(new_tx)

    return enriched
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    if not enriched_transactions:
        return

    headers = enriched_transactions[0].keys()

    with open(filename, "w") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = []
            for h in headers:
                value = tx[h]
                row.append("" if value is None else str(value))
            f.write("|".join(row) + "\n")

    print("✅ Enriched sales data saved to file")
