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

