"""catalog/cart — pick items on one page, see a summary on this page.   Foundations: loop, if, function

WHERE DOES "THE CART" LIVE?  In data.json, as a field on each row:  "picked": true / false.
A variable at the top of this file would NOT work — app.py reloads page files on every visit,
so nothing in a .py file survives between clicks. data.json is the only memory you have.
(One cart shared by everyone who opens the site — fine for a class project.)
"""
import storage

TITLE = "ตะกร้า"


def build():
    items = storage.load()

    picked = []
    count = 0
    subtotal = 0
    position = 0
    for item in items:
        item["no"] = position
        if item.get("picked", False):
            picked.append(item)
            count = count + item["qty"]
            subtotal = subtotal + item["qty"] * item["price"]
        position = position + 1

    discount, reason = discount_for(count, subtotal)
    return {
        "items": items, "picked": picked, "count": count, "subtotal": subtotal,
        "discount": discount, "reason": reason, "total": subtotal - discount,
    }


def discount_for(count, subtotal):
    """Return (discount_amount, reason) — a simple rule the group can change."""
    if count >= 5:
        return subtotal * 0.10, "ครบ 5 ชิ้น ลด 10%"
    if subtotal >= 1000:
        return subtotal * 0.05, "ยอดถึง 1,000 ลด 5%"
    return 0, ""


def handle(form):
    items = storage.load()
    action = form.get("action", "")
    position = form.get("no", "")

    if action == "clear":
        for item in items:
            item["picked"] = False
        storage.save(items)
        return "ล้างตะกร้าแล้ว"

    if action in ("add", "remove") and position.isdigit() and int(position) < len(items):
        item = items[int(position)]
        item["picked"] = (action == "add")
        storage.save(items)
        if action == "add":
            return "✓ หยิบ " + item["name"] + " ใส่ตะกร้า"
        return "เอา " + item["name"] + " ออกแล้ว"

    return "✗ ไม่เข้าใจคำสั่ง"
