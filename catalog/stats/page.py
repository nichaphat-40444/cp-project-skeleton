"""catalog/stats — count, sum, average, max, min, and a bar chart.   Foundation: loop + accumulation"""
import storage

TITLE = "สถิติ"


def build():
    items = storage.load()

    count = 0
    total_qty = 0
    total_value = 0
    most_expensive = None
    cheapest = None

    for item in items:
        count = count + 1
        total_qty = total_qty + item["qty"]
        total_value = total_value + item["qty"] * item["price"]
        if most_expensive is None or item["price"] > most_expensive["price"]:
            most_expensive = item
        if cheapest is None or item["price"] < cheapest["price"]:
            cheapest = item

    if total_qty > 0:
        average_price = total_value / total_qty
    else:
        average_price = 0

    # value per category: a dict filled by a loop
    per_category = {}
    for item in items:
        cat = item["category"]
        value = item["qty"] * item["price"]
        if cat in per_category:
            per_category[cat] = per_category[cat] + value
        else:
            per_category[cat] = value

    # bars: width = percent of the biggest value (never pixels — real numbers get huge)
    biggest = 0
    for cat in per_category:
        if per_category[cat] > biggest:
            biggest = per_category[cat]
    bars = []
    for cat in per_category:
        percent = 0
        if biggest > 0:
            percent = int(per_category[cat] * 100 / biggest)
        bars.append({"label": cat, "value": per_category[cat], "percent": percent})

    return {
        "count": count,
        "total_qty": total_qty,
        "total_value": total_value,
        "average_price": average_price,
        "most_expensive": most_expensive,
        "cheapest": cheapest,
        "bars": bars,
    }
