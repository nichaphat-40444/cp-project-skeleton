"""catalog/detail — one row, chosen with ?i=, shown through your class.   Foundation: class"""
import models
import storage

TITLE = "รายละเอียด"


def build(query):
    items = storage.load()
    if len(items) == 0:
        return {"item": None, "index": 0, "count": 0}

    # ?i=2 in the URL → index 2 ; missing or nonsense → 0
    index = 0
    if "i" in query and query["i"].isdigit():
        index = int(query["i"])
    if index >= len(items):
        index = len(items) - 1

    row = items[index]
    item = models.Item(row["name"], row["price"])       # build an object from the row

    return {
        "item": row,
        "sentence": item.describe(),                     # the class does the talking
        "index": index,
        "prev": index - 1 if index > 0 else None,
        "next": index + 1 if index < len(items) - 1 else None,
        "count": len(items),
    }
