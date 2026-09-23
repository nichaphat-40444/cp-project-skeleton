"""catalog/form — add a row to data.json with validation, plus a delete button per row.
Foundations: if/else, function"""
import storage

TITLE = "เพิ่มรายการ"


def build():
    items = storage.load()

    # stamp each row with its real position, so the delete button sends the right one
    rows = []
    position = 0
    for item in items:
        item["no"] = position
        rows.append(item)
        position = position + 1

    return {"items": rows, "count": len(rows)}


def read_number(text):
    """Turn form text into a number, or None if it is not a normal number."""
    try:
        value = float(text)
    except ValueError:
        return None
    if value != value or value in (float("inf"), float("-inf")):   # nan / inf are not real input
        return None
    return value


def check(form):
    """Return an error message, or "" when the form is fine."""
    if form.get("name", "").strip() == "":
        return "กรุณากรอกชื่อ"
    if not form.get("qty", "").isdigit():
        return "จำนวนต้องเป็นตัวเลขจำนวนเต็ม"
    price = read_number(form.get("price", ""))
    if price is None:
        return "ราคาต้องเป็นตัวเลข"
    if price < 0:
        return "ราคาต้องไม่ติดลบ"
    return ""


def handle(form):
    items = storage.load()

    # the small delete form sends  delete=<position>
    if "delete" in form:
        position = form["delete"]
        if position.isdigit() and int(position) < len(items):
            removed = items.pop(int(position))
            storage.save(items)
            return "🗑 ลบ " + removed["name"] + " แล้ว"
        return "✗ ไม่พบรายการที่จะลบ"

    error = check(form)
    if error != "":
        return "✗ " + error          # shown as a yellow banner, nothing saved

    items.append({
        "name": form["name"].strip(),
        "category": form.get("category", ""),
        "qty": int(form["qty"]),
        "price": read_number(form["price"]),
    })
    storage.save(items)
    return "✓ เพิ่ม " + form["name"].strip() + " แล้ว"
