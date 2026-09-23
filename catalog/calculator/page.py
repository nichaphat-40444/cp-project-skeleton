"""catalog/calculator — numbers in (from the URL), a loop, a table out.   Foundations: loop, if, function
Example: how the stock value grows if we add N items per month at a price that rises R % per year."""
import storage

TITLE = "คำนวณ"


def read_number(text, default):
    """Number from the URL text, or the default when empty/garbage."""
    try:
        value = float(text)
    except ValueError:
        return default
    if value != value:                    # nan
        return default
    return value


def build(query):
    # inputs come from <form method="get"> → ?monthly=…&rate=…&months=…
    monthly = read_number(query.get("monthly", ""), 1000)     # baht added per month
    rate = read_number(query.get("rate", ""), 5)              # yearly growth in %
    months = int(read_number(query.get("months", ""), 12))
    notice = ""
    if months < 1:
        months = 1
    if months > 120:
        months = 120
        notice = "จำกัดไว้ที่ 120 เดือน"

    # starting value = what is in data.json today
    start = 0
    for item in storage.load():
        start = start + item["qty"] * item["price"]

    # the loop: month by month
    rows = []
    balance = start
    added = 0
    month = 1
    while month <= months:
        balance = balance + balance * rate / 100 / 12   # growth for this month
        balance = balance + monthly                      # then we add
        added = added + monthly
        rows.append({"month": month, "added": added, "balance": balance})
        month = month + 1

    # column heights as percent of the final balance (for the chart)
    biggest = rows[-1]["balance"] if rows else 1
    for r in rows:
        r["percent"] = int(r["balance"] * 100 / biggest)

    return {
        "monthly": monthly, "rate": rate, "months": months,
        "start": start, "rows": rows, "final": rows[-1]["balance"] if rows else start,
        "growth": rows[-1]["balance"] - start - added if rows else 0,
        "notice": notice,
    }
