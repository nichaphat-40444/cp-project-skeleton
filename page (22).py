"""catalog/search — a text box that filters the table.   Foundations: loop + if"""
import storage

TITLE = "ค้นหา"


def build(query):
    keyword = query.get("q", "").strip().lower()
    items = storage.load()

    results = []
    for item in items:
        name = item["name"].lower()
        category = item["category"].lower()
        if keyword == "" or keyword in name or keyword in category:
            results.append(item)

    return {"keyword": keyword, "results": results, "total": len(items)}
