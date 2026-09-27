"""catalog/ranking — rows ordered by a number, top first, without sorted().   Foundation: nested loop"""
import storage

TITLE = "อันดับ"


def build():
    items = storage.load()

    # selection: repeatedly pull out the item with the highest price
    remaining = list(items)          # copy, so we can remove from it
    ranked = []
    while len(remaining) > 0:
        best = remaining[0]
        for item in remaining:
            if item["price"] > best["price"]:
                best = item
        ranked.append(best)
        remaining.remove(best)

    return {"ranked": ranked, "top": ranked[0] if ranked else None}
