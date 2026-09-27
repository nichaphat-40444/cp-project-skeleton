"""catalog/list — a table of everything in data.json.   Foundation: loop"""
import storage

TITLE = "รายการทั้งหมด"


def build():
    items = storage.load()

    # walk the list once to count and to add a running number
    numbered = []
    number = 1
    for item in items:
        item["no"] = number
        numbered.append(item)
        number = number + 1

    return {"items": numbered, "count": len(numbered)}
