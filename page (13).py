"""catalog/gallery — pictures from static/img/ with captions, plus an upload form.   Foundations: loop, if"""
import storage

TITLE = "แกลเลอรี"


def build():
    items = storage.load()

    cards = []
    for item in items:
        # a row may say "image": "multimeter.jpg" → static/img/multimeter.jpg
        if item.get("image", "") != "":
            picture = "img/" + item["image"]
        else:
            picture = "img/placeholder.svg"
        cards.append({"name": item["name"], "caption": item["category"], "picture": picture})

    return {"cards": cards}


def handle(form):
    # the form has enctype="multipart/form-data" and <input type="file" name="photo">
    # app.py saves the file into static/img/ and gives us the saved file name in form["photo"]
    name = form.get("name", "").strip()
    photo = form.get("photo", "")
    if name == "":
        return "✗ กรุณากรอกชื่อ"
    if photo == "":
        return "✗ กรุณาเลือกรูป (png / jpg / gif / webp / svg)"

    items = storage.load()
    items.append({"name": name, "category": form.get("category", "photo"), "qty": 1, "price": 0, "image": photo})
    storage.save(items)
    return "✓ เพิ่มรูป " + name + " แล้ว"
